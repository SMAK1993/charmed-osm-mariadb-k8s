from sys import version_info
from setuptools import find_packages, setup

minimum_python_version = (3, 5, 0)

if version_info[:3] < minimum_python_version:
    raise RuntimeError(
        'Unsupported python version {}. Please use {} or newer'.format(
            '.'.join(map(str, version_info[:3])),
            '.'.join(map(str, minimum_python_version)),
        )
    )


_NAME = 'mariadb-operator'
setup(
    name=_NAME,
    version='0.1.0',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
    ],
    author='Syed Mohammad Adnan Karim',
    author_email='syed.karim@canonical.com',
    include_package_data=True,
)
