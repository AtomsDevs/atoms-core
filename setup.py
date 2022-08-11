from setuptools import setup, find_packages

setup(
    name='Atoms Core',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/AtomsDevs/atoms-core',
    license='GPL-3.0-only',
    author='Mirko Brombin',
    author_email='send@mirko.pm',
    description='Atoms Core allows you to create and manage your own chroots'
                'and podman containers.',
    install_requires=[
        'orjson',
    ]
)
