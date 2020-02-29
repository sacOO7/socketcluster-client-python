from distutils.core import setup
import os.path
import setuptools

def readme():
    if os.path.exists('README.md'):
        with open('README.md') as f:
            return f.read()
    else:
        return "Python client for socket-cluster framework in node.js"


version = '1.3.6'

setup(
    name='socketclusterclient',
    packages=setuptools.find_packages(),  # this must be the same as the name above
    version=version,
    description='Client library for socketcluster framework in nodejs',
    long_description=readme(),
    long_description_content_type="text/markdown",
    author='Sachin Shinde',
    author_email='sachinshinde7676@gmail.com',
    license='MIT',
    url='https://github.com/sacOO7/socketcluster-client-python',  # use the URL to the github repo
    download_url='https://github.com/sacOO7/socketcluster-client-python/tarball/v' + version,
    keywords=['websocket', 'socketcluster', 'nodejs', 'client', 'socketclusterclient'],  # arbitrary keywords
    install_requires=[
        'websocket-client<=0.48',
    ],
    classifiers=[
        "Programming Language :: Python :: 2/3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)

# python setup.py register -r pypitest
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi
# python3 -m twine upload dist/*

## register

# python setup.py register -r pypitest
# python setup.py register -r pypi

## Build and upload
# python setup.py sdist bdist_wheel
# python3 -m twine upload dist/*

# git tag -a v1.3.4 -m "Fixed #16, websocket client version issue"
# git push --tags origin

# https://upload.pypi.org/legacy/
