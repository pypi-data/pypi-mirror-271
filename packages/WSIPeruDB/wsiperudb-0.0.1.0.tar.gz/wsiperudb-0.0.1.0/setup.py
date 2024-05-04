from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='WSIPeruDB',
    version='0.0.1.0',
    packages=find_packages(where='.'),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'mysql-connector-python',
        'folium',
        'scikit-learn',
        'plotly_express',
        'ipywidgets',
        'geopandas',
        'xlsxwriter'
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    author='Carol Romero',
    author_email='romeroroldancarol@gmail.com',
    description='Water Stable Isotope Database in Peru',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/karoru23/WSI-PeruDB',
)
