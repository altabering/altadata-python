from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="altadata",
    version="0.0.2",
    description="Python library for the ALTADATA API",
    url="https://github.com/altabering/altadata-python",
    author="ALTADATA",
    author_email="contact@altadata.io",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="altadata api data marketplace",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    packages=find_packages(exclude=["docs", "tests"]),
    python_requires=">= 3.5",
    install_requires=["requests >= 2.7.0"],
    extras_require={"pandas": ["pandas >= 0.21.0"]},
)
