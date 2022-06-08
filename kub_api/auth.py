from kub_api.abstract_auth import AbstractAuth
from aiohttp import ClientSession


class Auth(AbstractAuth):
    def __init__(self, websession: ClientSession, host: str, token_manager):
        """Initialize the auth."""
        super().__init__(websession, host)
        self.token_manager = token_manager

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if await self.token_manager.is_token_valid():
            return self.token_manager.access_token

        await self.token_manager.fetch_access_token()
        await self.token_manager.save_access_token()

        return self.token_manager.access_token
