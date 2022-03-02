from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import numpy as np

class PharmaciesInfo:
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        self.SCOPES = ['https://www.googleapis.com/auth/documents.readonly','https://www.googleapis.com/auth/spreadsheets.readonly']

        # The ID and range of a sample spreadsheet.
        self.SAMPLE_SPREADSHEET_ID = '1NZUUEhlp8wFOiatDmIlB7fCwJ6pUCtNtA1sEZJdYBgA'
        self.SAMPLE_RANGE_NAME = 'Sheet1!A2:H'
        self.saved_hash = ""
        self.is_cached = False

        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_api_credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.update()
    
    def download_data(self):
        try:
            service = build('sheets', 'v4', credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
            result = sheet.values().get(spreadsheetId=self.SAMPLE_SPREADSHEET_ID,
                                        range=self.SAMPLE_RANGE_NAME).execute()

            hashed_val = hash(str(result["values"]))
            return True, hashed_val, result

        except HttpError as err:
            print(err)

        return False, None, None

    def update(self):
        download_res, hashed_val, result = self.download_data()

        if not download_res:
            print("download issues, use saved value")
            return self.pharmacies_info
        
        if self.saved_hash == hashed_val:
            print("used hashed value")
            return self.pharmacies_info

        self.pharmacies_info = []
        values = result.get('values', [])

        if not values:
            print("Smth goes wrong, no data found!!!")
            return self.pharmacies_info

        for row in values:
            if len(row) > 2:
                name, address, latitude, longitude = row[0], row[1], row[-2], row[-1]
            else:
                continue

            if name and address and latitude and longitude:
                try:
                    latitude_val = float(latitude)
                    longitude_val = float(longitude)
                except:
                    print(f"<{name}> with address <{address}>: Incorrect latitude or longitude")
                    continue
            else:
                continue
            
            self.pharmacies_info.append((name, address, np.array([latitude_val, longitude_val]))) # not sure that precision will be ok

        self.saved_hash = hashed_val        
        self._update_cache()

        return self.pharmacies_info

    def get(self):
        if self.is_cached:
            return self.cache
        else:
            return self.update()

    def _update_cache(self):
        from copy import deepcopy
        import time
        self.is_cached = False
        time.sleep(1) # ugly, but ok
        self.cache = deepcopy(self.pharmacies_info)
        self.is_cached = True

if __name__ == '__main__':
    ph = PharmaciesInfo()
    res = ph.get()
    # main()