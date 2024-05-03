from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aws-ar',
    summary='Command Line Utility for Configuring Assumed AWS IAM Role Credentials',
    description='Command Line Utility for Configuring Assumed AWS IAM Role Credentials',  
    long_description=long_description,
    version='1.5',
    author='Shashank Dubey',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aws-ar = aws_ar.aws_ar:main'
        ]
    },
    install_requires=[
        'boto3',
    ],
)
