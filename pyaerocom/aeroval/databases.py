import configparser
from pathlib import Path

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class Influx:
    def __init__(self, config_file: str | Path, config_setup: str = "default") -> None:
        self.config_file = config_file
        if self.config_file == "":
            raise ValueError(f"Config location {self.config_file} cannot be empty")

        self.config_setup = config_setup

        self.client = InfluxDBClient.from_config_file(self.config_file)

    def _write_test(self, bucket: str) -> None:

        write_api = self.client.write_api(write_options=SYNCHRONOUS)

        query_api = self.client.query_api()

        p = Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)

        write_api.write(bucket=bucket, record=p)


if __name__ == "__main__":
    file = "/lustre/storeB/project/fou/kl/emep/People/danielh/projects/pyaerocom/aeroval/config/config_files/testing/influx/influx.ini"
    bucket = "test"
    influx = Influx(file)
    influx._write_test(bucket)
