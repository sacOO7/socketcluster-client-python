from distutils.core import setup

setup(
    name='socketclusterclient',
    packages=['socketclusterclient'],  # this must be the same as the name above
    version='1.2.1',
    description='Client library for socketcluster framework in nodejs',
    author='Sachin Shinde',
    author_email='sachinshinde7676@gmail.com',
    license='MIT',
    url='https://github.com/sacOO7/socketcluster-client-python',  # use the URL to the github repo
    download_url='https://github.com/sacOO7/socketcluster-client-python/tarball/v1.2.1',  # I'll explain this in a second
    keywords=['websocket', 'socketcluster', 'nodejs', 'client', 'socketclusterclient'],  # arbitrary keywords
    install_requires=[
          'websocket-client',
      ],
    classifiers=[],
)


# python setup.py register -r pypitest
# python setup.py sdist upload -r pypitest
# python setup.py register -r pypi
# python setup.py sdist upload -r pypi

# git tag -a v0.2 -m "My more optimized version of socketcluster client"
# git push --tags origin