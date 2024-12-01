from setuptools import setup, find_packages

# Function to parse requirements.txt
def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="witnesschangeme",
    version="0.0.1",
    description="Witnesschangeme - A tool to test website logins using Selenium and pyautogui.",
    author="KcanCurly",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    url="https://github.com/KcanCurly/witnesschangeme",
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
            "witnesschangeme=witnesschangeme.main:main",
        ],
    },
)