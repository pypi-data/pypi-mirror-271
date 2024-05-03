import aiohttp

from hacktegic._internal.config import ConfigManager
from hacktegic._internal.credentials import Credentials
from hacktegic.cloud.resources.networks import Networks


class NetworksAPIClient:
    def __init__(self, credentials: Credentials, config_manager: ConfigManager) -> None:
        self.credentials = credentials
        self.config_manager = config_manager

    async def create(self, network: dict) -> Networks:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/projects/{project_id}/networks"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.post(url, headers=headers, json=network) as response:
                return Networks(**(await response.json()))

    async def list(self) -> list[Networks]:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/projects/{project_id}/networks"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.get(url, headers=headers) as response:
                return [Networks(**i) for i in (await response.json())]

    async def describe(self, network_id: str) -> Networks:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/networks/{network_id}"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.get(url, headers=headers) as response:
                return Networks(**(await response.json()))

    async def update(self, network_id: str, network: dict) -> bool:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/networks/{network_id}"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.put(url, headers=headers, json=network) as response:
                return response.status == 200

    async def delete(self, network_id: str) -> bool:
        async with aiohttp.ClientSession() as session:
            base_url = self.config_manager.config["api_base_url"]
            project_id = self.config_manager.config["project_id"]
            url = f"{base_url}v1/networks/{network_id}"
            headers = {"Authorization": f"Bearer {self.credentials.access_token}"}
            async with session.delete(url, headers=headers) as response:
                return response.status == 200
