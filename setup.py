from setuptools import find_packages, setup

install_requires = [
    'requests>=2.22.0',
    'simplejson>=3.13.2',
    'Deprecated>=1.2.7',
    'six>=1.14.0'
]


setup(name='tacytsdk',
      version='2.8',
      description='Tacyt SDK',
      install_requires=install_requires,
      url='https://github.com/ElevenPaths/tacyt-sdk-python',
      author='ElevenPaths',
      author_email='',
      license='GNU',
      packages=find_packages())
