from etncanedge_files.listing import get_first_timestamp, get_log_files
from etncanedge_files.support.LocalFileSystem import LocalFileSystem
from etncanedge_files.support.RelativeFileSystem import RelativeFileSystem
import etncanedge_files.config as config

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
