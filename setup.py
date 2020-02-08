from setuptools import setup


setup(
    name='flask-jwt-auth',
    version='1.0.0',
    author='desun',
    packages=['apps'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
