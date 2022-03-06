import aiohttp
import asyncio

from .const import *

# Account object definition
class UteAccount:
    def __init__(self, accountServicePointId, accountId, name, servicePointAddress):
        self.accountServicePointId = accountServicePointId
        self.accountId = accountId
        self.name = name
        self.servicePointAddress = servicePointAddress

# Since a user of the app can have more than one UTE service registered (account), we get them with a method
async def get_user_accounts():
    user_accounts = []
    async with aiohttp.ClientSession() as session:

        # Get account information
        async with session.get(UTE_API_URL + "/v1/accounts", headers=APP_HEADERS) as account_info:
            account_data = await account_info.json()

            # Iterate if a customer has more than one account
            for service in account_data["data"]:
                user_accounts.append(UteAccount(service["accountServicePointId"], service["accountId"], service["name"], service["servicePointAddress"]))

    return user_accounts
