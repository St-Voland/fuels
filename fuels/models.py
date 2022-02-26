import enum

class EFuelType(enum):
    a92 = 0
    a95 = 1

class Location:
    # From
    # classtelegram.Location(longitude, latitude, horizontal_accuracy=None, live_period=None, heading=None, proximity_alert_radius=None, **_kwargs)
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

class FuelsInfo:
    def __init__(self, info):

        foo_info = {
            EFuelType.a92: 50,
            EFuelType.a95: 100
        }

        self.update_info(foo_info)

    def get_info(self):
        return self.info

    def update_info(self, info):
        self.info = info
    
    def partial_update(self, fuel_type, fuel_value):
        self.info[fuel_type] = fuel_value

class FuelStation:
    def __init__(self, location, fuel_info):
        self.location = location
        self.fuel_info = fuel_info

