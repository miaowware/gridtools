import pathlib
from setuptools import setup
import {{pkg_name}}.__info__ as info

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
    # NOTE: add classifiers here. See https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["{{pkg_name}}"],
    package_data={
        # NOTE: if the package has typing annotations, add an empty file named
        # "py.typed" to the package directory.
        # "{{pkg_name}}": ["py.typed"]
    },
    # NOTE: add the package's requirements here
    install_requires=[],
)
