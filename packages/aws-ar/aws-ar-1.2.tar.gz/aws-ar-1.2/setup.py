from setuptools import setup, find_packages

setup(
    name='aws-ar',
    summary='Command Line Utility for Configuring Assumed AWS IAM Role Credentials',
    version='1.2',
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
