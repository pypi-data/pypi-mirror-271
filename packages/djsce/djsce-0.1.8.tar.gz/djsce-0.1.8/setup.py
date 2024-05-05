from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='djsce',
  version='0.1.8',
  description='DJSCE',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mihir Panchal',
  author_email='mihirpanchal5400@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['djsce'], 
  packages=find_packages(),
)