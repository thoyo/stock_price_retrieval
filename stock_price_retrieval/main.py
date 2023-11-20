import yfinance as yf
from influxdb import InfluxDBClient
import datetime
import json
import time
import os
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logging.info("Starting program")

INFLUX_PORT = 8086
INFLUX_DATABASE = "stock"
if os.environ.get("AM_I_IN_A_DOCKER_CONTAINER", False):
    INFLUX_HOST = "influxdb_mt"
else:
    INFLUX_HOST = "0.0.0.0"

INFLUXDBCLIENT = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT, database=INFLUX_DATABASE)

STOCKS = json.loads(open("config.json").read())


def main():
    for stock in STOCKS:
        now = datetime.datetime.now()

        start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = now

        intraday_data = yf.download(stock, start=start_time, end=end_time, interval='1m')

        latest_data_point = intraday_data.tail(1)["High"].iloc[0]
        point_out = {
            "measurement": "prices",
            "fields": {"price": latest_data_point},
            "tags": {"stock": stock},
            "time": now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        INFLUXDBCLIENT.write_points([point_out])


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logging.error(e, exc_info=True)
        time.sleep(3600)
