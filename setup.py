from setuptools import setup, find_packages

setup(
    name="WitnessChangme",
    version="0.0.1",
    author="KcanCurly",
    description="A script to find default credentials on websites and take picture after login.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KcanCurly/WitnessChangme",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "DumpSMBShare=src.main:main",  
        ],
    },
)