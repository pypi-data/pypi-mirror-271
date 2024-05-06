# pip install . # To install the package locally and test it before uploading.

# Change version & download_url in setup.py
# Push the changes
# Create new relase on GitHub
# Activate py env
# python setup.py sdist
# pip install twine
# twine upload dist/*


# from distutils.core import setup
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
  name = 'ashfaquecodes',         # How you named your package folder (MyLib)
  packages = ['ashfaquecodes'],   # Chose the same as "name"
  version = '0.8',      # Start with a small number and increase it with every change you make. # * Change in every build.
  download_url = 'https://github.com/ashfaque/ashfaquecodes/archive/refs/tags/v_08.tar.gz',    # Link of your source code    # * Change in every build.
  license='GNU GPLv3',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository or, https://choosealicense.com/
  description = 'Codes which can be used to increase productivity.',   # Give a short description about your library
  long_description_content_type = "text/markdown",    # Really important if you are using README.md format.
  long_description = long_description,      # Long description read from the the readme file
  author = 'Ashfaque Alam',                   # Type in your name
  author_email = 'ashfaquealam496@yahoo.com',      # Type in your E-Mail
  url = 'https://github.com/ashfaque/ashfaquecodes',   # Provide either the link to your github or to your website
  keywords = ['ASHFAQUE', 'ASHFAQUECODES', 'PRODUCTIVITY'],   # Keywords that define your package best
  install_requires=[            # Your packages dependencies    # * Change if current going build adds some dependencies of external packages.
          'colorama'
          # , 'pandas'
          , 
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU General Public License (GPL)',   # Again, pick a license
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
  ],
)