import pathlib
from setuptools import setup
import gridtools.__info__ as info

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name=info.__project__,
    version=info.__version__,
    description=info.__summary__,
    long_description=README,
    long_description_content_type="text/markdown",
    url=info.__webpage__,
    author=info.__author__,
    author_email=info.__email__,
    license=info.__license__,
    # TODO: add classifiers here. See https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["gridtools"],
    package_data={
        "gridtools": ["py.typed"]
    },
    # TODO: add the package's requirements here
    install_requires=[],
)
