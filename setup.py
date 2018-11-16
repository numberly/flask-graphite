from setuptools import setup


def get_description():
    with open("README.rst") as file:
        return file.read()


setup(
    name='Flask-Graphite',
    version='0.5.2',
    url='https://github.com/numberly/flask-graphite',
    license='MIT',
    description="Push useful metrics for each request without effort!",
    long_description=get_description(),
    author='numberly',
    author_email='ramnes@1000mercis.com',
    packages=['flask_graphite'],
    include_package_data=True,
    zip_safe=False,
    platform='any',
    install_requires=[
        'Flask>=0.12',
        'graphitesend>=0.10.0'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
