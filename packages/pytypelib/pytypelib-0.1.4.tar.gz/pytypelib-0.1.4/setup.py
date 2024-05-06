from setuptools import setup, find_packages
long_discription = open(r"README.md", 'r').read()

setup(
    name=r'pytypelib',
    version='0.1.4',
    description=r"Some more helpful python types and objects",
    long_description=long_discription,
    author=r'@malachi196',
    author_email=r'malachiaaronwilson@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires=r'>=3.8',
)