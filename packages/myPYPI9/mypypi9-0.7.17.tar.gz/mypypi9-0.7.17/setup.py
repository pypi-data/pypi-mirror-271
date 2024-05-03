from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="myPYPI9", #package name Replace with your own username
    version="0.7.17",
    author="timenet2300",
    author_email="endersu@outlook.com",
    description="Create A small package to work with prime numbers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/clement-bonnet/medium-first-package",
    # url="https://github.com/myNKUST/myprimelib9b.git",
    
    #find_packages():find the package module name in myprimelib9b/_init_.py: 
    #from myprimelib9b.prime_numbers import is_prime
    #packages=find_packages(), 
    packages=['myPYPI9'], 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
