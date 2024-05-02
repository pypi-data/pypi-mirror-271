from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='onessds',
  version='1.0.0',
  author='Python_Palma',
  author_email='admin@gmail.com',
  description='This is my first module',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://pypi.org/onessds',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='my  python',
  project_urls={
    'Documentation': 'https://pypi.org/'
  },
  python_requires='>=3.7'
)
