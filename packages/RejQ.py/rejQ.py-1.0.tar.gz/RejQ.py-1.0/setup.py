from setuptools import setup, find_packages
from platform import system

with open("README.md", "r") as file:
	long_description = file.read()

link = 'https://github.com/TheeeWhiteDeath'
ver = '1.0'
setup(
	name = "RejQ.py",
	version = ver,
	url = "https://github.com/TheeeWhiteDeath",
	download_url = link,
	license = "MIT",
	author = "rejQ",
	author_email = "rejq1akk@gmail.com",
	description = "Library powered by rejQ",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	keywords = [
		"rejQ.py",
		"rejQ",
		"rejQ-py",
		"rejQ-bot",
		"api",
		"python",
		"python3",
		"python3.x",
		"rejQ",
		"official",
		"async",
		"sync",
		"rejQ"
	],
	install_requires=[
    "requests>=2.0.0",
    "selenium>=3.0.0",
    "faker>=8.0.0",
    "beautifulsoup4>=4.0.0",
    "aiogram>=2.0.0"
],
	packages = find_packages()
)
