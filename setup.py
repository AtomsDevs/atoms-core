from setuptools import setup

setup(
    name='Atoms Core',
    version='0.1',
    packages=['atoms-core'],
    url='https://github.com/mirkobrombin/atoms-core',
    license='MIT',
    author='Mirko Brombin',
    author_email='send@mirko.pm',
    description='Atoms Core allows you to create and manage your own chroots'
                'and podman containers.',
    install_requires=[
        'orjson'
    ]
)