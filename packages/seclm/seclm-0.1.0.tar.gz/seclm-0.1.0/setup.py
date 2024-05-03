from setuptools import setup

setup(
    name='seclm',
    version='0.1.0',
    description='seclm',
    author='stneng',
    author_email='git@stneng.com',
    url='https://github.com/sec-lm/seclm',
    packages=['seclm', 'seclm.ssl'],
    install_requires=[
        'cryptography'
    ],
    python_requires='>=3.10',
)
