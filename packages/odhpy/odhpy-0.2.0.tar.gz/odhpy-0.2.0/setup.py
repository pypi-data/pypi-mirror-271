import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open('src/odhpy/version.py').read())

setuptools.setup(
    name="odhpy",
    version=__version__,
    python_requires=">=3.9",
    author="Chas Egan",
    author_email="chas@odhydrology.com",
    description="A collection of splashings to master that which has no form and count that which is uncountable.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/odhydrology/odhpy.git",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'altair>=5.0.1',
        'folium>=0.14',
        'matplotlib>=3.8.3',
        'numpy>=1.26.4',
        'pandas>=2.2.0',
        'plotly>=5.18.0',
    ],    
)