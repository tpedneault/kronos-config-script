from scripts.utils import *

import os
import subprocess
import sys
import urllib.request
import ssl
import xml.etree.ElementTree as ET
from shutil import copyfile

ssl._create_default_https_context = ssl._create_unverified_context

# Script will download the MSYS2 from this url.
msys2_url = "https://repo.msys2.org/distrib/x86_64/msys2-x86_64-20210725.exe"
msys2_path = "C:\\msys64\\"

dependencies = ["mingw-w64-x86_64-toolchain mingw-w64-x86_64-make", "mingw-w64-x86_64-cmake mingw-w64-x86_64-openocd", "mingw-w64-x86_64-arm-none-eabi-gcc",
                "mingw-w64-x86_64-arm-none-eabi-gdb", "mingw-w64-x86_64-arm-none-eabi-binutils"]

def windows_dependencies():
    cwarn(f"If MSYS2 is already installed, it must be installed at {msys2_path} for the configurations to work.")
    cwarn("Otherwise, you will need to change the paths in the CLion configuration.")

    # Check is msys64 exists already.
    if not os.path.isdir(msys2_path):
        # Fetch the msys2 installer.
        if not os.path.isfile("msys2.exe"):
            cout("Downloading MSYS2 installer...")
            urllib.request.urlretrieve(msys2_url, "msys2.exe")

        # Run the silent install for msys2
        cout("Installing MSYS2...")
        path = os.path.abspath(os.curdir + "\\scripts\\windows\\silent_msys.js")
        installer_exe_path = os.path.abspath(os.path.join(os.curdir, 'msys2.exe')).replace(" ", "` ")
        subprocess.call(f"powershell.exe {installer_exe_path} --platform minimal --script {path.replace(' ', '` ')} InstallDir={msys2_path.replace(' ', '` ')}")

    cout("Updating MSYS2 packages...")
    subprocess.call(f"{msys2_path}usr\\bin\\bash -lc \"pacman --noconfirm -Syuu\"")

    cout("Installing Kronos dependencies...")
    formatted_dependencies = ' '.join(["{}"]*len(dependencies)).format(*dependencies)
    # TODO: store dependencies in a list instead of hardcoding them for easier modifications.
    subprocess.call(
        f"{msys2_path}usr\\bin\\bash -lc \"pacman --noconfirm -S {formatted_dependencies}\"")

    """
    
    if not os.path.isdir("..\\.idea"):
        cerr("Script directory is not a subdirectory of a CLion project. Exiting...")
        exit(1)

    cout("Adding MINGW toolchain to CLion")

    jetbrains_directory = os.listdir(os.getenv("APPDATA") + "\\JetBrains")
    clion_installations = [x for x in jetbrains_directory if 'CLion' in x]

    cout(clion_installations)

    # TODO: Change files in home of currently logged in user instead.
    #       If user a does not have admin privileges, and uses user b's account to run changes. Script will change files in b instead of a's home directory.
    if len(clion_installations) > 1:
        # TODO: Allow user to select which installation to use.
        cwarn("Found multiple CLion installations, using most recent one...")
    elif len(clion_installations) == 0:
        cerr("No CLion installations were found. Exiting...")
        exit(1)

    clion_dir = os.path.join(os.getenv("APPDATA"), "JetBrains", clion_installations[0])

    # Do CLion specific configuration changes.
    # TODO: Instead of replacing the whole .xml file, add the needed tags to the existing file (if any) to prevent overriding existing configurations.
    copyfile(os.path.join(os.curdir, "templates", "toolchains.xml"),
             os.path.join(clion_dir, "options", "windows", "toolchains.xml"))
    copyfile(os.path.join(os.curdir, "templates", "embedded-support.xml"),
             os.path.join(clion_dir, "options", "windows", "embedded-support.xml"))

    # Do project specific configuration changes.
    project_dir = os.path.abspath(os.path.join(os.curdir, "..", ".idea"))

    # Find path to the sam_gcc.cmake file
    sam_gcc_path = os.path.abspath(os.path.join(project_dir, "..", "lib", "build", "sam_gcc.cmake"))
    if not os.path.isfile(sam_gcc_path):
        # if that file doesn't exist, probably running have orthus-fsw opened instead of kronos
        sam_gcc_path = os.path.abspath(os.path.join(project_dir, "..", "kronos", "lib", "build", "sam_gcc.cmake"))

    # check if the CMakeSettings node exists. If not create it,
    workspace_xml = ET.parse(os.path.join(project_dir, "workspace.xml"))
    found_c_make_settings = False
    for node in workspace_xml.getroot():
        if node.attrib['name'] == 'CMakeSettings':
            # TODO: Check if the configurations already exist before writing them.
            cout("Inserting CMakeSettings configurations...")
            found_c_make_settings = True
            debug_config = ET.fromstring(
                f'<configuration PROFILE_NAME="Debug-KRONOS" ENABLED="true" CONFIG_NAME="Debug" TOOLCHAIN_NAME="MinGW" GENERATION_OPTIONS="-DCMAKE_TOOLCHAIN_FILE=&quot;{sam_gcc_path}&quot;" />')
            release_config = ET.fromstring(
                f'<configuration PROFILE_NAME="Release-KRONOS" ENABLED="true" CONFIG_NAME="Release" TOOLCHAIN_NAME="MinGW" GENERATION_OPTIONS="-DCMAKE_TOOLCHAIN_FILE=&quot;{sam_gcc_path}&quot;" />')
            node[0].append(debug_config)
            node[0].append(release_config)
            cout(node[0][2].attrib)

    # CMakeSettings node doesn't exist, create it.
    if not found_c_make_settings:
        cout("Configuration file did not CMakeSettings node, creating it...")
        cmake_settings = ET.fromstring(f'''
        <component name="CMakeSettings">
            <configurations>
                <configuration PROFILE_NAME="Debug-KRONOS" ENABLED="true" CONFIG_NAME="Debug" TOOLCHAIN_NAME="MinGW" GENERATION_OPTIONS="-DCMAKE_TOOLCHAIN_FILE=&quot;{sam_gcc_path}&quot;" />
                <configuration PROFILE_NAME="Release-KRONOS" ENABLED="true" CONFIG_NAME="Release" TOOLCHAIN_NAME="MinGW" GENERATION_OPTIONS="-DCMAKE_TOOLCHAIN_FILE=&quot;{sam_gcc_path}&quot;" />
            </configurations>
        </component>
        ''')
        workspace_xml.getroot().insert(2, cmake_settings)

    # TODO: It still works, but for some reason when writing the formatting of the file is messed up. (CLion doesn't care and still reads it just fine)
    workspace_xml.write(os.path.join(project_dir, "workspace.xml"))

    # TODO: Add Run Configurations...
    cout("[NOT IMPLEMENTED] Adding Run Configurations")
    cout("Done!")
    
    """
    
