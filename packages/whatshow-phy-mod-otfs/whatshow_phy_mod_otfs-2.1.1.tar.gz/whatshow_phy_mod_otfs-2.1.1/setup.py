from setuptools import setup, find_packages

# prepare the instruction
description = "";
with open("README.md", "r") as readme:
    description = readme.read();
setup(
      name="whatshow_phy_mod_otfs",
      version="2.1.1",
      packages=find_packages(),
      install_requires=['numpy>=1.23.5'],
      long_description = description,
      long_description_content_type = "text/markdown"
);