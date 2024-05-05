from setuptools import find_packages, setup

setup(
    name='pybb-client',
    packages=find_packages(
        include=[
            'bbclientlib',
        ],
    ),
    version='0.0.1',
    description='Bitbucket client for Python',
    author='novokrest',
    install_requires=[],
    setup_requires=['pytest-runner'],
    test_require=['pytest==8.2.0'],
    test_suite='tests',
)
