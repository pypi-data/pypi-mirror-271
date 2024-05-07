from setuptools import setup, find_packages

setup(
    author="Hammad Saeed",
    author_email="hammad@supportvectors.com",

    name='hadronic',
    version='0.0.3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    python_requires='>=3.8',
    
    install_requires=[
        "zyx",
        "litellm",
    ],

    entry_points={
        'console_scripts': [
            'hadron=hadronic.core.cli:main',  # Adjust the module path as necessary
        ],
    },
)
