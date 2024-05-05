from setuptools import setup, find_packages

setup(
    name='discohooks',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='A simple library for interacting with Discord webhooks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nyxoy201',
    author_email='discord.nyxoy@proton.me',
    url='https://github.com/Nyxoy201/discohooks',
)
