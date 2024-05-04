from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='roysolver',
  version='0.0.1',
  description='A very basic equation solver',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Roy Perry',
  author_email='roypery2010@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='solver', 
  packages=find_packages(),
  install_requires=[''] 
)