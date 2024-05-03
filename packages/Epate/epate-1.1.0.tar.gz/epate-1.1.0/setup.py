from setuptools import setup, find_packages

from pkg_resources import parse_requirements

install_requires = ['requests==2.31.0']

setup(name="Epate",
      version="1.1.0",
      author="xiaoxlh",
      author_email="xiaoxiaogzs@outlook.com",
      description="A python library for many API of the codemao's website.",
      long_description="eds sdk for python",
      license="Apache License, Version 2.0",
      url="https://xiao.asia",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          "Programming Language :: Python :: 3.12",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      packages=find_packages(),
      install_requires=install_requires,
      entry_points={'console_scripts': ['test = test.help:main']})
