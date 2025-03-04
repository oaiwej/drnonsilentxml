from setuptools import setup, find_packages

# requirements.txtから依存関係を読み込む
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="drnonsilentxml",
    version="0.1.0",
    description="A tool to generate XML timelines with silent parts removed for Davinci Resolve Free Edition",
    author="oaiwej",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "drnonsilentxml=drnonsilentxml.__main__:main",
        ],
    },
    python_requires=">=3.11"
)