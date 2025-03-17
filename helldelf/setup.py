from setuptools import setup, find_packages

setup(
    name="helldelf",
    version="2.2.1",
    packages=find_packages(),
    install_requires=[
        "asyncio>=3.4.3",
    ],
    python_requires=">=3.7",
)