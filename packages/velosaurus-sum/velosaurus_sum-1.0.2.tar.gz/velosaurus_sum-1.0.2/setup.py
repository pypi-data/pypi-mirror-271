from setuptools import find_packages
from setuptools import setup

setup(
    name="velosaurus_sum",
    version="1.0.2",
    description="Just a dummy project for some pipeline and package deployment testing",
    long_description="Just a dummy project for some pipeline and package deployment testing",
    author="Oliver Zott",
    author_email="zott_oliver@web.de",
    url="https://github.com/OliverZott/python-devops-example",
    packages=find_packages(),
    install_requires=[
        # Add any dependencies your project requires
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
