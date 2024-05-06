
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="dalle3-gen-save",
    version="4.5.50",
    packages=find_packages(),
    py_modules=['dalle3_gen_save'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'dalle3_gen_save = dalle3_gen_save:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
