from setuptools import setup, find_packages
from io import open

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='krestnullbests',
  version='1.5',
  author='Python_Palma',
  author_email='xaker_1515@mail.ru',
  description='BEST',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://pypi.org/krestnullbests',
  packages=find_packages(),
  install_requires=['requests>=2.25.1', 'art'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='Snake ,python, Palma',
  project_urls={
    'Documentation': 'https://youtube.com/'
  },
  python_requires='>=3.5'
)
