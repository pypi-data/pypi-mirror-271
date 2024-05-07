from cht.observation_stations.observation_stations import StationSource
from noaa_coops import Station

class Source(StationSource):
    def __init__(self):
        pass

    def list_stations(self):
        pass

    def get_meta_data(self, id):
        pass

    def get_data(self, station_id, tstart, tstop,
                 varname="water_level",
                 units = "SI",
                 datum = "MSL"):

                t0_string = tstart.strftime("%Y%m%d")
                t1_string = tstop.strftime("%Y%m%d")

                if varname == "water_level":
                    product = varname
                if units == "SI":
                    units = "metric"

                station = Station(id=station_id)
                df = station.get_data(begin_date=t0_string,
                                      end_date=t1_string,
                                      product=product,
                                      datum=datum,
                                      units=units,
                                      time_zone="gmt")
                return df[product]
