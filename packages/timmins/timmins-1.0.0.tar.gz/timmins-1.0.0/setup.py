from setuptools import find_packages
from setuptools import setup

setup(
    name="timmins",
    version="1.0.0",
    description="Python packaging using setup.py",
    author="Mohammad Mahfooz Alam",
    author_email="mahfooz.iiitian@gmail.com",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "hello-world = timmins:hello_world",
        ]
    },
)
