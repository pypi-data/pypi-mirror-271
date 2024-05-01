from setuptools import setup, find_packages
setup(
    name='socketsecurity',
    version='0.0.38',
    packages=find_packages(),
    install_requires=[
        'click',
        'mdutils',
        'requests',
        'prettytable'
    ],
    entry_points='''
        [console_scripts]
        my_cli_app=socketcli.socketcli:cli
        ''',
)