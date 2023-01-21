from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="tweet_replies",
    version="0.1",
    description="A script that extracts replies with links from a specified Tweet",
    url="https://github.com/arun279/tweet_replies",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "tweet_replies = tweet_replies:main",
        ],
    },
)
