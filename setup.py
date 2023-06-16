from setuptools import setup, find_packages

import compileall

compileall.compile_dir("datarangers")

setup(
    name='datarangers-sdk-python',
    version='1.1.1',
    packages=['datarangers',
              'datarangers.collector',
              'datarangers.collector.config',
              'datarangers.collector.writer',
              'datarangers.collector.model',
              'datarangers.collector.util'],
    url='',
    license='DataRangers',
    author='DataRangers',
    author_email='datarangers-opensource@bytedance.com',
    description='',
    install_requires=['requests']
)
