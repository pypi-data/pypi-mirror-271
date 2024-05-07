from setuptools import setup

setup(
    name='vowels_counter1.0',
    version='0.1.1',
    packages=['vowels_counter'],
    description="This package counts the number of vowels from the input text.",
    install_requires=[
        'importlib; python_version == "3.11"',
    ],
)