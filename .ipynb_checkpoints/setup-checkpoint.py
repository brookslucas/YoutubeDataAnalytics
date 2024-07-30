from setuptools import setup, find_packages

setup(
    name='your_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Your dependencies, e.g., 'fastapi', 'sqlalchemy', etc.
        # These can be copied from requirements.txt
    ],
    entry_points={
        'console_scripts': [
            'your_package=your_package.main:main',
        ],
    },
)
