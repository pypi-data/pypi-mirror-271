"Comprehensive toolbox with all of the utils and tools used in various TGC projects."
# Import logger functions
from .downloaders import download_file as download_file
from .downloaders import download_video_as_wav as download_video_as_wav
from .downloaders import download_video_as_wav as download_youtube
from .downloaders import download_vosk_model as download_vosk_model
from .ffmpeg import *
from .logger import JacobsAmazingLogger as TGCLogger
from .logger import JacobsAmazingLoggerFormatter as TGCLoggerFormatter
from .logger import JacobsAmazingResultsLogger as TGCResultsLogger
from .logger import log_result as log_result
from .logger import log_result as TGCLogResult
from .logger import setup_custom_logger as TGCLoggerSetup
from .operations import *
from .settings import Settings as Settings
from .vosk import transcribe_vosk as transcribe_vosk

# Importing Settings class

# Importing downloaders
# Import vosk utils
# Importing ffmpeg utils
# Importing operations

# Importing recorder. Be warned that recorder function is just for testing here and is not robust at all.
try:
    from .recorder import *
except ImportError:
    pass

# Importing sound utils
from .sound import is_chunk_ready as is_chunk_ready
from .sound import bytes_to_wav as bytes_to_wav
from .sound import resample_audio as resample_audio

# Import wrappers
from .wrapper import custom_formatwarning as custom_formatwarning
from .wrapper import experimental_feature as experimental_feature

# Import timing utils
from .timing import TimingMiddleware as TimingMiddleware
from .timing import log_time as log_time

# Import server utils
from .wait_run import is_server_up as is_server_up
from .wait_run import wait_for_server as wait_for_server

# Import version
from .meta import __version__ as __version__
from .meta import __author__ as __author__
from .meta import __provider__ as __provider__
