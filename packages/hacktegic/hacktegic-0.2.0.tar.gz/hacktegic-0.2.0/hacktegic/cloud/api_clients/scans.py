import aiohttp

from hacktegic._internal.config import ConfigManager
from hacktegic._internal.credentials import Credentials
from hacktegic.cloud.resources.scans import Scans


class ScansAPIClient:
    def __init__(self, credentials: Credentials, config_manager: ConfigManager) -> None:
        self.credentials = credentials
        self.config_manager = config_manager

    async def list(self) -> list[Scans]:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/projects/{project_id}/scans"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.get(url, headers=headers) as response:
                return [Scans(**i) for i in (await response.json())]

    async def describe(self, scan_id: str) -> Scans:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/scans/{scan_id}"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.get(url, headers=headers) as response:
                return Scans(**(await response.json()))

    async def delete(self, scan_id: str) -> bool:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/scans/{scan_id}"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}

            try:
                async with session.delete(url, headers=headers) as response:
                    response.raise_for_status()
                    return response.status == 200
            except aiohttp.ClientResponseError as cre:
                print(f"HTTP error occurred: {cre.status}, message='{cre.message}', url={cre.request_info.url}")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False