from setuptools import setup, find_packages

setup(
    name="melodicious",
    version="0.0.1",
    author="Cropsun",
    author_email="melodiciousai@gmail.com",
    description="A simple API client for AI-Music Generate",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cropsun/melodicious",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
