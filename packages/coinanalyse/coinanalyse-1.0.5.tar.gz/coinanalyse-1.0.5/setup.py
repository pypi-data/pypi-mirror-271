from setuptools import setup

setup(  name= 'coinanalyse', 
        version='1.0.5', 
        description='Coin-help-package For Tr@ding bot.', 
        packages=['coinanalyse'],
		author='Alice',
		license="Python Script",
        install_requires = ["blessings ~= 1.7"],
        extras_require={
            "dev": [
                "pytest>=3.2",
            ],
        },
    )

