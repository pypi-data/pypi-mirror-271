import argparse
import os

from bioblend import galaxy
from bioblend.galaxy.tools.inputs import inputs

class Galaxy:
    def __init__(self):
        args = self._parse_args()
        self._connect_to_galaxy(args)

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--galaxy-url", help="URL of the Galaxy server")
        parser.add_argument("--galaxy-key", help="API key for accessing the Galaxy server")
        parser.add_argument("--galaxy-history-id", help="Default Galaxy history ID to use")
        args, unknown = parser.parse_known_args()
        return args

    def _connect_to_galaxy(self, args):
        self.galaxy_url = args.galaxy_url or os.getenv("GALAXY_URL")
        self.galaxy_api_key = args.galaxy_key or os.getenv("GALAXY_API_KEY")
        self.galaxy_instance = galaxy.GalaxyInstance(url=self.galaxy_url, key=self.galaxy_api_key)
    
    # Additional methods from your provided code...

class SharedGalaxy:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = Galaxy()
        return cls._instance
