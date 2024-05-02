import os
import setuptools
import xml.etree.ElementTree as ET

pom = ET.parse("./src/hedera_proto/pom.xml")
version_element = pom.getroot().find('{http://maven.apache.org/POM/4.0.0}version')
version = version_element.text.split('-')[0]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hedera-proto",
    version=version,
    author="Wensheng Wang",
    author_email="wenshengwang@gmail.com",
    description="Hedera Protobufs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HbarStudio/hedera-protobufs-python",
    project_urls={
        "Bug Tracker": "https://github.com/HbarStudio/hedera-protobufs-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['grpcio>=1.59.3'],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={ "hedera_proto": ["*.xml"]},
)
