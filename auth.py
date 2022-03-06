mport aiohttp
import asyncio
from .const import *

class GetToken():
    async def login(mail, phone):
        async with aiohttp.ClientSession() as session:
            LOGIN_HEADERS.update({
                    "Email": mail,
                    "PhoneNumber": phone,
                })

            # Retrieve login token
            async with session.post(UTE_API_URL + "/v1/token", headers=APP_HEADERS, json=LOGIN_HEADERS) as response:
                authToken = "Bearer " + await response.text()
                APP_HEADERS.update({"Authorization": authToken})

                # Check authentication
                async with session.get(UTE_API_URL + "/v1/accounts", headers=APP_HEADERS) as account_info:
                    if (account_info.status == 401):
                        response.status = 401
                return response
