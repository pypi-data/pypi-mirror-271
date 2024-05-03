from setuptools import setup, find_packages

setup(
    name='handler',
    version='0.1.0',
    package_dir={'': '_userland'},
    packages=find_packages(where='_userland'),
    install_requires=[
        "aws-cdk-lib==2.88.0",
        "boto3",
        "constructs>=10.0.0,<11.0.0",
        "mysql-connector-python",
        "nodeenv",
        "pycognito",
        "pydantic",
        "pymysql",
        "requests",
        "sqlalchemy"
    ],
)
