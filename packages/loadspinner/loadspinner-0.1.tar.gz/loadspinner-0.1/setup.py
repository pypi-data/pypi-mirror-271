from setuptools import setup
import loadspinner

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="loadspinner",
    version=loadspinner.__version__,
    description=loadspinner.__description__,
    long_description=readme,
    url="https://github.com/xyzpw/loadspinner/",
    long_description_content_type="text/markdown",
    author=loadspinner.__author__,
    maintainer=loadspinner.__author__,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
        "Topic :: Terminals",
        "Environment :: Console",
        "Environment :: Console :: Curses",
        "Intended Audience :: Developers",
    ],
    keywords=[
        "loading",
        "loader",
        "progress",
        "throbber",
        "spinner",
    ],
    license=loadspinner.__license__,
    python_required=">=3.8",
)

