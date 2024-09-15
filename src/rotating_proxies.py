"""Module to rotate proxies."""

import asyncio
import json
from dataclasses import dataclass, field
from typing import Set

import aiohttp
import requests

from src.constants import CommonConstants, PlayerLinksConstants


@dataclass
class RotatingProxies:
    """Class to rotate proxies when making requests to the API."""

    path: str
    proxies_list: Set[str] = field(init=False)
    working_proxies: Set[str] = field(init=True, default_factory=set)

    def __post_init__(self):  # noqa: D105
        self.proxies_list = set(
            open(self.path, "r", encoding="utf-8").read().strip().split("\n")
        )

    def test_proxies(self, url: str) -> None:
        """Test proxies on a url.

        Parameters
        ----------
        url : str
            Url where to test proxies on.
        """
        for proxy in self.proxies_list:
            session = requests.Session()
            response: requests.Response = session.get(
                url, proxies={"http": f"http://{proxy}"}, timeout=3
            )

            if response.status_code == CommonConstants.status_code_ok:
                self.working_proxies.add(proxy)
            else:
                print(f"{proxy} failed!")

    def test_proxies2(self, url: str):
        """Docstring."""
        for proxy in self.proxies_list:
            try:
                r = requests.get(
                    url,
                    proxies={
                        "http": proxy,
                        "https": proxy,
                    },
                    timeout=3,
                )

                if r.status_code == 200:
                    self.working_proxies.add(proxy)
            except:
                pass

    # async def multi_test_proxies(self, url: str) -> None:
    #     pass


if __name__ == "__main__":
    rotator = RotatingProxies(path="data/proxy_list.txt")
    rotator.test_proxies2(url=PlayerLinksConstants.fantacalcio_link)
    print(rotator.working_proxies)
    print("\n\n\n")
    print(len(rotator.working_proxies))
    # with open("data/player_links.json", "w", encoding="utf-8") as file:
    #     json.dump(rotator.working_proxies, file, indent=4)
