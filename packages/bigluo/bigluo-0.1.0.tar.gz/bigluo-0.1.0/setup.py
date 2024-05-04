from setuptools import setup, find_packages

setup(
    name='bigluo',
    version='0.1.0',
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
