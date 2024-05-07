from cht.observation_stations.observation_stations import StationSource
from NDBC.NDBC import DataBuoy
import cht.misc.xmlkit as xml

class Source(StationSource):
    def __init__(self):
        self.db = DataBuoy()

    def get_active_stations(self):
        url = "https://www.ndbc.noaa.gov/activestations.xml"
        obj = xml.xml2obj(url)
        station_list = []
        for station in obj.station:
            station_list.append({"name": station.name,
                                 "id": station.id,
                                 "lon": float(station.lon),
                                 "lat": float(station.lat)})
        self.active_stations = station_list    
        return station_list

    def get_meta_data(self, id):
        self.db.set_station_id(id)
        try:
            meta_data = self.db.station_info
        except:
            meta_data = None
        return meta_data

    def get_data(self, id, variable=None):
        pass
