import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pfex",
    version="0.1.11",
    author="Alexander Lachmann",
    author_email="alexander.lachmann@mssm.edu",
    description="Package for fast and accurate calculation of Fisher Exact Test with Enrichr library support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maayanlab/pfx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "pfex": ["data/*"]
    },
    include_package_data=True,
    install_requires=[
        'pandas>=1.1.5',
        'numpy',
        'statsmodels',
        'numba',
        'python-louvain',
        'networkx'
    ],
    python_requires='>=3.6',
)
