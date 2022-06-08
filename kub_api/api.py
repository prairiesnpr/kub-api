from kub_api.auth import Auth


class KUBAPI:
    """Class to communicate with the Ameritrade API."""

    def __init__(self, auth: Auth):
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth

    async def async_get_session_data(self):
        """Return session data"""
        resp = await self.auth.request("get", f"auth/v1/sessions/current")
        resp.raise_for_status()
        return await resp.json()

    async def async_get_account_details(self, account_id=None):
        """Return session data"""
        resp = await self.auth.request("get", f"cis/v1/accounts/{account_id}", params={"include": "all"})
        resp.raise_for_status()
        return await resp.json()

    async def async_get_usage_data(self, person_id=None, service_point_id=None, start_date=None, end_date=None, utility_type=None):
        """Return usage data"""
        params = {
            "endDate": end_date.isoformat(),
            "personId": person_id,
            "servicePointId": service_point_id,
            "startDate": start_date.isoformat(),
            "utilityType": utility_type

        }
        resp = await self.auth.request("get", f"ami/v1/usage-values", params=params)
        resp.raise_for_status()
        return await resp.json()

    async def async_get_weather_data(self, start_date=None, end_date=None):
        """Return weather data"""
        params = {
            "endDate": int(end_date.timestamp() * 1000),
            "startDate": int(start_date.timestamp() * 1000),

        }
        resp = await self.auth.request("get", f"ami/v1/weather-days", params=params)
        resp.raise_for_status()
        return await resp.json()
