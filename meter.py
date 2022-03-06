import aiohttp
import asyncio
from time import sleep
from datetime import datetime

from .const import *

class UteMeter:
    def __init__(self, vendor, mtrId, apparent_power, monthly_consumption):
        self.vendor = vendor
        self.mtrId = mtrId
        self.apparent_power = apparent_power
        self.monthly_consumption = monthly_consumption

class MeterError(Exception):
    """Exception raised for errors when the meter fails to get a measurement."""

    def __init__(self, meter_message):
        self.meter_message = meter_message
        super().__init__(self.meter_message)

async def measures(account):

    connector = aiohttp.TCPConnector(force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:

        # Get account services information
        async with session.get(UTE_API_URL + "/v1/accounts/" + str(account.accountServicePointId), headers=APP_HEADERS) as service_info:
            service_data = await service_info.json()
            meter_vendor = service_data["data"]["meterInfo"]["amiType"]
            meter_id = service_data["data"]["meterInfo"]["mtrId"]

        # Request instant measure to meter
        body_measure = {
            "AccountServicePointId": account.accountServicePointId
        }

        async with session.post(UTE_API_URL + "/v1/device/readingRequest", headers=APP_HEADERS, json=body_measure) as measurement_request:
            measure_post = await measurement_request.text()

        # Read instant power measure (UTE APP retries the GET every 5 seconds until it get's a measure, so we do the same here setting 20 max retries for caution)
        measure = {}
        measure["success"] = "False"

        retries = 0

        while (str(measure["success"]) == "False" and retries < 20):
            sleep(5)
            async with session.get(UTE_API_URL + "/v1/device/" + str(account.accountServicePointId) + "/lastReading/30", headers=APP_HEADERS) as measurement:
                measure = await measurement.json()

                if (str(measure["success"]) == "True"):
                    # Handle exceptions for meter measuraments errors, status 1 means successful measurement, other codes are for errors
                    if (str(measure["data"]["status"]) != "1"):
                        raise MeterError(measure["data"]["statusText"])
                        break

                    else:
                        voltage = measure["data"]["readings"][0]["valor"]
                        intensity = measure["data"]["readings"][1]["valor"]
                        meter_apparent_power = float(voltage) * float(intensity)

                retries+= 1

        # Get current month power consumption
        async with session.get(UTE_API_URL + "/v2/device/" + str(account.accountServicePointId) + "/curvefromtodate/D/" + datetime.today().strftime("%Y-%m") + "-01/" + datetime.today().strftime("%Y-%m-%d"), headers=APP_HEADERS) as daily_measurements:
            daily_measures = await daily_measurements.json()

        total_power = 0
        for i in daily_measures["data"]:
            if i["magnitudeVO"] == "IMPORT_ACTIVE_ENERGY":
                total_power += i["value"]
        meter_monthly_consumption = total_power

        meter_data = UteMeter(meter_vendor, meter_id, meter_apparent_power, meter_monthly_consumption)

    return meter_data
