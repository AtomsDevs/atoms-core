from setuptools import setup, find_packages

setup(
    name='Atoms Core',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/AtomsDevs/atoms-core',
    license='GPL-3.0-only',
    author='Mirko Brombin',
    author_email='send@mirko.pm',
    description='Atoms Core allows you to create and manage your own chroots'
                'and distrobox containers.',
    install_requires=[
        'orjson',
    ]
)
