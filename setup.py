import setuptools


setuptools.setup(
    name='keepasshttp',
    version='0.1.0',
    packages=setuptools.find_packages(exclude=['tests']),
    install_requires=[
        'cryptography',
        'pyyaml',
        'pyxdg',
        'requests'
    ],
    setup_requires=['nose>=1.0'],
    tests_require=['mock==2.0.0']
)
