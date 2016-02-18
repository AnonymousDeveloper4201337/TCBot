# -*- coding: utf-8 -*-
"""
Created on May 20, 2014

@author: Diana
"""
import msilib

import requests
from cx_Freeze import Executable, setup

import Inno

base = None

GUID = msilib.gen_uuid()

# FOFF
# noinspection PyPep8
shortcut_table = [
    ("DesktopShortcut",  # Shortcut
     "DesktopFolder",  # Directory_
     "Trade Currency Bot",  # Name
     "TARGETDIR",  # Component_
     "[TARGETDIR]TCBot.exe",  # Target
     None,  # Arguments
     None,  # Description
     None,  # Hotkey
     None,  # Icon
     None,  # IconIndex
     None,  # ShowCmd
     'TARGETDIR'  # WkDir
    ),
    ("StartupShortcut",  # Shortcut
     "StartupFolder",  # Directory_
     "Trade Currency Bot",  # Name
     "TARGETDIR",  # Component_
     "[TARGETDIR]TCBot.exe",  # Target
     None,  # Arguments
     None,  # Description
     None,  # Hotkey
     None,  # Icon
     None,  # IconIndex
     None,  # ShowCmd
     'TARGETDIR'  # WkDir
    ),
    ("UninstallShortcut",  # Shortcut
     "DesktopFolder",  # Directory_
     "Uninstall TCBot",  # Name
     "TARGETDIR",  # Component_
     "[SystemFolder]msiexec.exe",  # Target
     "/x " + GUID,  # Arguments
     'Test',  # Description
     None,  # Hotkey
     None,  # Icon
     None,  # IconIndex
     True,  # ShowCmd
     'SystemFolder'  # WkDir
    )
]
# FON

msi_data = {"Shortcut": shortcut_table}

build_exe_options = {
    "include_files": [(requests.certs.where(), 'cacert.pem'), 'TCIcon.ico'],
    'includes': ['lxml.etree', 'lxml._elementpath', 'gzip', ], 'packages': ['os', 'RbxAPI', ], 'include_msvcr': True
}

bdist_msi_options = {
    'upgrade_code': '{B8086972-1305-4CE4-854D-F050B99DC05C}', 'data': msi_data, 'product_code': GUID
}

app = Executable("Main.py", targetName='TCBot.exe', icon="TCicon.ico", )

ver = '3.0'
# FOFF
setup(name="Trade Currency Bot", author='Diana',
      author_email='CrazyKilla15@gmail.com',
      version=ver,
      description="Iaz3's Trade Currency Bot for Roblox",
      options={
          "build_exe": build_exe_options,
          'bdist_msi': bdist_msi_options
               },
      executables=[app])
# FON
# print('Setup Completed: ' + time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime()))
