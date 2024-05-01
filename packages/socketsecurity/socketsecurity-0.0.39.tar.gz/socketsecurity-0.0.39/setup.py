from setuptools import setup, find_packages
setup(
    name='socketsecurity',
    version='0.0.39',
    packages=find_packages(),
    install_requires=[
        'click',
        'mdutils',
        'requests',
        'prettytable'
    ],
    entry_points='''
        [console_scripts]
        socketcli=socketsecurity.socketcli:cli
        ''',
)