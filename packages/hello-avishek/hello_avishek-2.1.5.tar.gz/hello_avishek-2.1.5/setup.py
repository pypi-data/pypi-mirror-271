from setuptools import setup, find_packages
setup(
    name="hello-avishek",
    version="2.1.5",
    packages=find_packages(),
    install_requires=[
        #Add dependencies
    ],
    entry_points={
        "console_scripts": [
            "hello_hello = hello_hello:hello",
        ],
    }
)