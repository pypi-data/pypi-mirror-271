from setuptools import setup, find_packages

LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

setup(
    name='mypybuildcode',  # this is the name of the package
    version='0.0.2',
    description='this is xjtest library',
    long_description=LONG_DESCRIPTION,
    author='XJ Yian',
    author_email='ianyian@gmail.com',
    url='https://github.com/ianyian/mypybuildcode',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        # list of dependencies e.g.,
        # 'numpy',
        # 'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
