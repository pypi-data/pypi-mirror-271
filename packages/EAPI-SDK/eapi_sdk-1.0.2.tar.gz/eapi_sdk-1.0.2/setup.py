from setuptools import setup

setup(
    name='EAPI_SDK',
    version='1.0.2',
    description='A Python SDK to interact with the EAPI Platform',
    packages=['eapisdk'],
    install_requires=[
        'requests>=2.25.1',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)