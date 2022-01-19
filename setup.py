#from setuptools import setup, find_packages
import pkg_resources
# import find_packages,setuptools
from setuptools import find_packages, setup

setup(
    name='dmLibrary',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    entry_points={
                    'console_scripts':
                    [
                        'run-api=dmLibrary.run:run',
                        'run-cli=dmLibrary.run:cli',
                        'run-manage=dmLibrary.run:manage'

                    ],
                }
)
