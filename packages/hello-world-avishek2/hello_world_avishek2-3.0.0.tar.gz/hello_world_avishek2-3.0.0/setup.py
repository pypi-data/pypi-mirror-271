from setuptools import setup, find_packages
setup(
    name="hello-world-avishek2",
    version="3.0.0",
    packages=find_packages(),
    install_requires=[
        #Add dependencies
    ],
    entry_points={
        "console_scripts": [
            #"hello_hello = hello_hello:hello",
        ],
    }
)