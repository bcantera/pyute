import aiohttp
import asyncio
from time import sleep
from datetime import datetime

from .const import *

async def main():

    services_data = {}
    meter = {}

    async with aiohttp.ClientSession() as session:

        # Get account information
        async with session.get(UTE_API_URL + "/v1/accounts", headers=APP_HEADERS) as account_info:
            account_data = await account_info.json()
            
            # Iterate if a customer has more than one account
            for service in account_data["data"]:

                # Get account services information
                async with session.get(UTE_API_URL + "/v1/accounts/" + str(service["accountServicePointId"]), headers=APP_HEADERS) as service_info:
                    services_data[service["accountServicePointId"]] = await service_info.json()

        # Request instant measure to meter
        body_measure = {
            "AccountServicePointId": service["accountServicePointId"]
        }
        async with session.post(UTE_API_URL + "/v1/device/readingRequest", headers=APP_HEADERS, json=body_measure) as measurement_request:
            measure_post = await measurement_request.text()

        # Read instant power measure (UTE APP retries the GET until it get's a measure, so we do the same here setting 10 max retries for caution)
        measure = {}
        measure["success"] = "False"
        retries = 0

        while (str(measure["success"]) == "False" and retries < 10):
            async with session.get(UTE_API_URL + "/v1/device/" + str(service["accountServicePointId"]) + "/lastReading/30", headers=APP_HEADERS) as measurement:
                sleep(3)
                measure = await measurement.json()
                retries+= 1

        success = measure["success"]
        voltage = measure["data"]["readings"][0]["valor"]
        intensity = measure["data"]["readings"][1]["valor"]
        meter["wattage"] = float(voltage) * float(intensity)

        # Get current month power consumption
        async with session.get(UTE_API_URL + "/v2/device/" + str(service["accountServicePointId"]) + "/curvefromtodate/D/" + datetime.today().strftime("%Y-%m") + "-01/" + datetime.today().strftime("%Y-%m-%d"), headers=APP_HEADERS) as daily_measurements:
            daily_measures = await daily_measurements.json()

        total_power = 0
        for i in daily_measures["data"]:
            if i["magnitudeVO"] == "IMPORT_ACTIVE_ENERGY":
                total_power += i["value"]
        meter["current_month_power"] = total_power

    return meter
