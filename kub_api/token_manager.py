import yaml
import os

from datetime import datetime

from aiohttp import ClientSession


class TokenManager:
    def __init__(self, username=None, password=None):
        """Initialize the Token Manager."""
        self.username = username
        self.password = password
        self.access_token = None
        self.access_expires = None
        self.access_aquired = None
        self.cache_location = os.path.join(os.getcwd(), "kub.yaml")

    async def fetch_access_token(self):
        try:
            with open(self.cache_location) as file:
                token_info = yaml.full_load(file)            

            if token_info:
                self.access_token = token_info["access_token"]
                self.access_expires = token_info["access_expires"]
                self.access_aquired = token_info["access_aquired"]

                if not await self.is_token_valid():
                    await self.refresh_access_token()
                    return

            if not token_info:
                await self.refresh_access_token()
                return

        except (FileNotFoundError, TypeError):
            await self.refresh_access_token()

    async def save_access_token(self):
        with open(self.cache_location, "w") as file:
            yaml.dump(
                {
                    "access_token": self.access_token,
                    "access_expires": self.access_expires,
                    "access_aquired": self.access_aquired,
                },
                file,
            )
        
    async def is_token_valid(self):
        if await self.is_token_expired():
            return False
        return True

    async def is_token_expired(self):
        if not self.access_expires or not self.access_aquired:
            return True
        if datetime.utcnow() >= self.access_expires:
            return True
        return False

    async def is_refresh_token_valid(self):
        return await self.is_token_expired

    async def refresh_access_token(self):
        """Get a token."""
        websession = ClientSession()
        headers = {}

        data = {
            'session': {
                'username': self.username,
                'password': self.password,
                'expirationDate': None,
                'user': None,
            },
        }
        resp = await websession.request(
            "post",
            "https://www.kub.org/api/auth/v1/sessions",
            json=data,
            headers=headers,
        )
        json_res = await resp.json()

        self.access_aquired = datetime.utcnow()
        
        access_expires = datetime.fromisoformat(json_res.get("session")[0].get("expirationDate")).replace(tzinfo=None)
        for cookie in websession.cookie_jar:
            if cookie.key == "access_token":
                self.access_token = cookie.value
        self.access_expires = access_expires
        await self.save_access_token()
