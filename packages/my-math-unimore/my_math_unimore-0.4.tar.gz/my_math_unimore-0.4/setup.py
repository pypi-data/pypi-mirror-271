from setuptools import setup, find_packages
  
setup( 
    name='my_math_unimore', 
    version='0.4', 
    description='A sample Python package to test CI/CD', 
    long_description='A sample Python package to test CI/CD',
    author='Angelo Ferrando', 
    author_email='angelo.ferrando42@gmail.com', 
    packages=find_packages(), 
    install_requires=['pytest'], 
) 