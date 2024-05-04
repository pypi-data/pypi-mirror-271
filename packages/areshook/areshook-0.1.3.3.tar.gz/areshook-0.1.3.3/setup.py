from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='areshook',
    version='0.1.3.3',
    author='369',
    author_email='luck.yangbo@gmail.com',
    description='A simple hook library.',
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'frida',
        'frida-tools',
        'heradata',
        'pydantic'
    ],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
