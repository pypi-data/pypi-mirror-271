from setuptools import setup, find_packages

setup(
    name='PrismNET',
    version='0.10.0',
    packages=find_packages(),
    author='frane s ',
    author_email='znikafranek@gmail.com',
    description='A easy framework..',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Microbots-io/PrismNet-Framework/tree/main',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[
        'pyinstaller',
        'setuptools',
        'wheel',
    ]
)
