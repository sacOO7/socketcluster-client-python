from distutils.core import setup
import os.path


def readme():
    if os.path.exists('README.md'):
        with open('README.md') as f:
            return f.read()
    else: 
        return "Python client for socket-cluster framework in node.js"

setup(
    name='socketclusterclient',
    packages=['socketclusterclient'],  # this must be the same as the name above
    version='1.3.4',
    description='Client library for socketcluster framework in nodejs',
    long_description=readme(),
    author='Sachin Shinde',
    author_email='sachinshinde7676@gmail.com',
    license='MIT',
    url='https://github.com/sacOO7/socketcluster-client-python',  # use the URL to the github repo
    download_url='https://github.com/sacOO7/socketcluster-client-python/tarball/v1.3.4',
    keywords=['websocket', 'socketcluster', 'nodejs', 'client', 'socketclusterclient'],  # arbitrary keywords
    install_requires=[
        'websocket-client<=0.48',
    ],
    classifiers=[],
)


# python setup.py register -r pypitest
# python setup.py sdist upload -r pypitest
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi
# python3 -m twine upload dist/

# git tag -a v1.3.4 -m "Fixed #16, websocket client version issue"
# git push --tags origin

# https://upload.pypi.org/legacy/
