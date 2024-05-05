from setuptools import setup, find_packages

setup(
    name="fpb",
    version="0.1",
    packages=find_packages(),
    author_email="2831926323@qq.com",
    author="Alex",
    install_requires=[
        "aiohttp",
        "psutil",
        "inflection"
    ],
)
