from .benchmark import (bench_cpu,info_plat)
from .communicate.tcpsocket import (server,client)
# Version of the node-specs package
import tomli
def get_version():
    with open('pyproject.toml', 'rb') as file:
        project_data = tomli.load(file)
        return project_data['project']['version']

__version__ = get_version()

