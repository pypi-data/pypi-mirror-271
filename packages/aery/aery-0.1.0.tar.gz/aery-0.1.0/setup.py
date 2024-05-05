from setuptools import find_packages, setup

setup(
    name='aery',
    version=open('version.txt').read().strip(),
    author='Evan Raw',
    author_email='evanraw.ca@gmail.com',
    description='AeryAI.com',
    license='MIT',
    install_requires=[],
    packages=find_packages()
)
