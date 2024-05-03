from setuptools import setup, find_packages

setup(
    name='SocialMediaBot',
    version='2.0',
    packages=find_packages(),
    description='A configurable social media bot designed to automatically post quotes on various platforms.',
    long_description=open('README.md').read(),
    author='Phani Adabala',
    author_email='adabala.phani@gmail.com',
    url='https://github.com/adabalap/SocialMediaBot',
    install_requires=[
        # list of packages your project depends on
    ],
)

