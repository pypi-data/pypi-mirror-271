from setuptools import setup, find_packages

setup(name="fastboard",
      version="0.0.1",
      author="0aaxs",
      author_email="",
      license="MIT",
      description="A simple library for making a dashboard.",
      long_description=open("README.rst").read(),
      packages=find_packages(),
      install_requires=["discord.py", "discord"]
      )