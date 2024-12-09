from setuptools import setup, find_packages

setup(
    name='auth-middleware',
    version='0.0.1',
    long_description=open('README.md').read(),
    url='https://github.com/grimimirg/auth-middleware',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask==2.2.2',
        'PyJWT==2.6.0',
        'pycryptodome==3.14.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6'
)
