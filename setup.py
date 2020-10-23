from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

INSTALL_REQUIRES = ["requests >= 2.7.0"]

EXTRA_REQUIRES = {"pandas": ["pandas >= 0.14"]}

setup(
    name="altadata",
    version="0.1",
    description="Python library for the ALTADATA API",
    url="https://github.com/altabering/altadata-python",
    author="ALTADATA",
    author_email="contact@altadata.io",
    license="MIT",
    keywords="altadata api data marketplace",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">= 3.5",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRA_REQUIRES,
)
