from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="Red-Dashboard",
    version="0.1.5a",
    description="An easy-to-use interactive web dashboard to control your Redbot.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/NeuroAssassin/Red-Dashboard",
    author="Neuro Assassin",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["reddash"],
    include_package_data=True,
    install_requires=[
        "flask==1.1.2",
        "requests==2.23.0",
        "cryptography==2.9.2",
        "websocket_client==0.57.0",
        "waitress==1.4.3",
        "rich==1.3.1",
        "fuzzywuzzy==0.18.0",
        "python-Levenshtein==0.12.0",
        "pyjwt==1.7.1",
        "flask-babel==1.0.0",
    ],
    extras_require={
        "style": ["black==19.10b0"],
        "docs": ["Sphinx==2.4.4", "sphinx-rtd-theme==0.4.3"],
    },
    entry_points={"console_scripts": ["reddash=reddash.__main__:main"]},
)
