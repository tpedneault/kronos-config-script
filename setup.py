import platform

from scripts.windows import *
from scripts.darwin import *
from scripts.linux import *
from scripts.utils import *

# Check if the script was started from an elevated prompt.
import ctypes
import os

os_platform = platform.system()

try:
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

if not is_admin:
    cerr("Script must be started with administrative privileges (otherwise can't install MSYS2).")
    exit(1)

#cwarn("Before running this script, make sure that you have opened the project once in CLion (to ensure that all the config files are generated)")
cwarn("Current user must have administrative privileges (for MSYS2 installation), otherwise script will not work.")
cout("This script will automatically install all dependencies for the Kronos framework.")
#cout("Before you begin, ensure that the directory containing this script is at the root of the project (kronos or orthus-fsw)")
#cout("It is HIGHLY RECOMMENDED that you create a backup of your current CLion and project configuration.")

cout("Detected operating system: " + os_platform)

is_continue = yes_or_no("Do you wish to continue?")
if not is_continue:
    cout("Exiting...")
    exit(0)

if os_platform == "Linux":
    linux_dependencies()
elif os_platform == "Darwin":
    darwin_dependencies()
elif os_platform == "Windows":
    windows_dependencies()
