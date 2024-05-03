from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='krest_null_best',
  version='1.3',
  author='Python_Palma',
  author_email='xaker_1515@mail.ru',
  description='BEST',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://pypi.org/krest_null_best',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='Snake ,python',
  project_urls={
    'Documentation': 'https://pypi.org/'
  },
  python_requires='>=3.5'
)
