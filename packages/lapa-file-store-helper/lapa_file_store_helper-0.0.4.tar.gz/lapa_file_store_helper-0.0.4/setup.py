from setuptools import find_packages, setup

package_name = "lapa_file_store_helper"

setup(
    name=package_name,
    version="0.0.4",
    packages=find_packages(),
    package_data={
        package_name: ["data/*"],
    },
    install_requires=[
        "requests>=2.31.0",
        "kiss_headers>=2.4.3",
        "lapa_commons>=0.0.1"
    ],
    author="thePmSquare, Lav Sharma, Amish Palkar",
    author_email="thepmsquare@gmail.com, lavsharma2016@gmail.com, amishpalkar302001@gmail.com",
    description="helper to access the file store layer for my personal server.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url=f"https://github.com/thepmsquare/{package_name}",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
