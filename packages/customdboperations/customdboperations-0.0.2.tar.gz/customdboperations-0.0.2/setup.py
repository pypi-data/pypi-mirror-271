import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_discription = f.read()

__version__ = '0.0.2'

REPO_NAME = "mongoDB_connector"
AUTHOR_USER_NAME = "TapanKheni10"
PKG_NAME = "customdboperations"
AUTHOR_EMAIL = "tapankheni10304@gmail.com"

setuptools.setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for connecting with database",
    long_description=long_discription,
    long_discription_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
    },
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src")
)