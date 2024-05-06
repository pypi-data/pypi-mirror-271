from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='pypa-make-easy',
    version='0.1',
    license='Apache License 2.0',
    description='Script to Create PyPi projects, but in easy',
    long_description=readme(),
    author='Kevin Alexander Krefting',
    author_email='kakrefting@gmail.com',
    url='https://github.com/DevMasterLinux/pypa-make-easy',
    scripts=['pypa-make-easy', 'pypa'],
    install_requires=["ruamel.yaml"],
    classifiers=(
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3'
    )
)
