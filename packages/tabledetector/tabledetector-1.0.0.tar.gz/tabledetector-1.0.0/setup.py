from io import open
from setuptools import setup, find_packages

with open('requirements.txt', encoding="utf-8-sig") as f:
    requirements = f.readlines()

def readme():
    with open('README.md', encoding="utf-8-sig") as f:
        README = f.read()
    return README

setup(
    name='tabledetector',
    packages=find_packages(),
    include_package_data=True,
    version='1.0.0',
    install_requires=requirements,
    license='MIT License',
    description='End-to-End table structure detector',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Rishav Banerjee',
    author_email='rishavbanerjee10.rb@gmail.com',
    url='https://github.com/rajban94/TableDetector',
    download_url='https://github.com/rajban94/TableDetector.git',
    keywords=['table detector'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 1 - Planning',
        'Operating System :: OS Independent'
    ],

)