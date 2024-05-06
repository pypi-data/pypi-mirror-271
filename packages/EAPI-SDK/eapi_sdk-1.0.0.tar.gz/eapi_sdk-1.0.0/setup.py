from setuptools import setup

setup(
    name='EAPI_SDK',
    version='1.0.0',
    description='A Python SDK to interact with the EAPI Platform',
    packages=['eapi-sdk'],
    install_requires=[
        'requests>=2.25.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)