from setuptools import setup, find_packages

setup(
    name='bgtest',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        # Add dependencies here
        # e.g. 'numpy>=1.11.1'
    ],
    # cml settings
    entry_points={
        "console_scripts": [
            "bgtest = bgtest:hello",
        ],
    },
)
