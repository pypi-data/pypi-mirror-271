from setuptools import setup, find_packages

setup(
    name='SX1509_gpio_expander',
    version='0.1.0',
    author= "Tim Schumann",
    description='A package to control the SX1509 GPIO expander',
    url='https://github.com/T-N-S/SX1509_gpio_expander_package',  # replace with your URL
    packages=find_packages(),
    package_data={
        'SX1509_gpio_expander': ['*.py'],
    },
    include_package_data=True,
    install_requires=[
        'adafruit-circuitpython-busdevice',
    ]
)