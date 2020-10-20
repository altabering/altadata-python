from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="altadata",
    version="0.1",
    description="Python library for the ALTADATA API.",
    url="https://github.com/altabering/altadata-python",
    author="ALTADATA",
    author_email="info@altadata.io",
    license="MIT",
    keywords="altadata api data marketplace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["requests", "pandas"],
)
