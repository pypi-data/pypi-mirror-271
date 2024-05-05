from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='SMClib.py',
  version='1.0.9',
  description='biblioteka ułatwiająca prace przy discord botach',
  long_description=open('README.rst').read(),
  url='',  
  author='ESKARABATOS',
  author_email='bartek.torba@interia.pl',
  license='MIT', 
  classifiers=classifiers,
  keywords='SMC Discord',
  packages=find_packages(),
  install_requires=['discord.py'] 
)