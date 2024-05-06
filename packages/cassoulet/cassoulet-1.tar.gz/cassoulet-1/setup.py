from setuptools import setup

setup(
    name='cassoulet',
    version='1',
    packages=['cassoulet'],
    package_dir={'cassoulet': '.'},
    py_modules=['cassoulet'],
    entry_points={
        'console_scripts': [
            'cassoulet = cassoulet:main',
        ]
    },
    author='Mathias Bochet and Thomas Corno',
    description='A delicious terroir meal',
)