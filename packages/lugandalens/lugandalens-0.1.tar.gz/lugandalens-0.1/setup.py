from setuptools import setup, find_packages

setup(
    name='lugandalens',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.14.0',  
        'numpy',
        'pandas',
    ],
)

