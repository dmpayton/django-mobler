#!/usr/bin/env python

import os
from mobler import __version__, __description__
from setuptools import setup, find_packages

## Package detection from django-registration

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dirpath, dirnames, filenames in os.walk('mobler'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[11:] # Strip "mobler/" or "mobler\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name='django-mobler',
    version=__version__,
    description=__description__,
    long_description=__description__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    keywords='django mobile browscap',
    maintainer = 'Derek Payton',
    maintainer_email = 'derek.payton@gmail.com',
    url='https://github.com/dmpayton/django-mobler',
    download_url='https://github.com/dmpayton/django-mobler/tarball/v1.1.0',
    license='MIT License',
    include_package_data=True,
    packages=packages,
    package_data={'mobler': data_files},
    package_dir={'mobler': 'mobler'},
    zip_safe=False,
    )
