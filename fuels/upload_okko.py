from datetime import datetime

import db.database as db
import pandas as pd

MAPPING_OKKO_FUELTYPE = {
    "Бензин А-92": db.FuelType.A92,
    "Бензин А-95": db.FuelType.A95,
    "Газ нафтовий скраплений": db.FuelType.GAS,
    "Дизельне паливо": db.FuelType.DP
}


def main():
    df = pd.read_excel("data/АЗС-2022 (1).xlsx")
    df.rename({
        'Підрозділ': 'name',
        'Точна адреса': 'address',
    }, axis=1, inplace=True)
    df['company'] = 'okko'
    df['coordinates'] = 'POINT(' + df['GPS Широта'].astype(str) + ' ' + df['GPS Довгота'].astype(str) + ')'
    del df['GPS Довгота'], df['GPS Широта']

    db.Base.metadata.drop_all(bind=db.engine)
    db.Base.metadata.create_all(db.engine)

    for row in df.itertuples(index=False):
        station = db.Station()
        station.name = row.name
        station.company = row.company
        station.address = row.address
        station.coordinates = row.coordinates

        station.commit()

        lst_statuses = []
        for col, fuel_type in MAPPING_OKKO_FUELTYPE.items():
            status = db.Status()
            status.station_id = station.id
            status.date = datetime.now()
            status.fuel_type = fuel_type
            status.is_avail = True
            lst_statuses.append(status)
        db.session.add_all(lst_statuses)
        db.session.commit()

if __name__ == '__main__':
    main()
