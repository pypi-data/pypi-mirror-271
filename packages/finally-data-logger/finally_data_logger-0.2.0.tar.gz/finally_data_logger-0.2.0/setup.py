from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="finally_data_logger",
    version="0.2.0",
    description="A simple data logging server and client.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="arbasli",
    author_email="arbasli2@gmail.com",
    url="https://github.com/arbasli2/FinallyDataLogger",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "flask",
        "requests",
        "tinydb",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "finallydatalogger = finally_data_logger.server.finally_data_logger_server:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
