"""
`pyitc` for interacting with the Intelchain blockchain
"""
import sys
import warnings

__version__ = "0.1.1"

if sys.version_info.major < 3:
    warnings.simplefilter( "always", DeprecationWarning )
    warnings.warn(
        DeprecationWarning(
            "`pyitc` does not support Python 2. Please use Python 3."
        )
    )
    warnings.resetwarnings()

if sys.platform.startswith( "win32" ) or sys.platform.startswith( "cygwin" ):
    warnings.simplefilter( "always", ImportWarning )
    warnings.warn(
        ImportWarning( "`pyitc` does not work on Windows or Cygwin." )
    )
    warnings.resetwarnings()
