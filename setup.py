from setuptools import setup, find_packages

setup(
    name='yd_package',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
       'fastapi',
        'sqlalchemy',
        'pydantic',
        'databases',
        'uvicorn',
        'boto3'
    ],
    entry_points={
        'console_scripts': [
            'your_package=your_package.main:main',
        ],
    },
)
