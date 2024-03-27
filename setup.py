# from setuptools import setup
from cx_Freeze import setup, Executable
import sys


# Specify the main script and create an executable
main_script = 'Binance_App_I.py'
executables = [Executable(main_script)]

# Additional options
build_options = {
    'include_files': [],  # Add any additional files or data your script depends on
    'packages': ['webdriver_manager','bs4','PyQt5','selenium'],       # Add any additional packages your script requires
}

# Create the setup configuration
setup(
    name='Binance_App_I',
    version='1.0',
    description='Eziline Software House',
    options={'build_exe': build_options},
    executables=executables
)

# APP = ['Binance_App_I.py']
# DATA_FILES = ['icon.png']
# OPTIONS = {'argv_emulation': True, 'packages':['webdriver_manager','bs4','PyQt5','selenium',]}

# setup(
#    app=APP,
#    version="0.1",
#    author="Muhammad Muzamil Khan",
#    data_files=DATA_FILES,
#    options={'py2app':OPTIONS},
#    setup_requires=['py2app'],
#    # packages=find_packages(),
#    classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: Eziline License",
#         "Operating System :: MacOS",
#     ],
#    python_requires='>=3.6',

# )

# setup(

#     packages=find_packages(),
#     install_requires=[
#         "PyQt5",
#         "selenium",
#         "webdriver_manager",
#         "beautifulsoup4",
#         "pync"
#     ],
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )
