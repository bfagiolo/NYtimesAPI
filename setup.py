
from setuptools import setup

APP = ['mainNYtimes.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': None,  # You can add your .icns file here if you want a custom icon
    'includes': [
        'tkinter',
        'requests',
        'dateutil',
        'matplotlib.pyplot',
        'sqlite3',
        'unittest',
        'collections',
    ],
    'packages': ['matplotlib', 'requests', 'dateutil'],
    'plist': {
        'CFBundleName': 'NYTimes Article Finder',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'CFBundleIdentifier': 'com.yourname.nytfinder',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
