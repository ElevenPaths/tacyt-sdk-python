from setuptools import setup, find_packages


install_requires = [
  'requests==2.22.0'
]


setup(name='tacytsdk',
      version='2.6',
      description='Tacyt SDK',
      install_requires=install_requires,
      url='https://github.com/ElevenPaths/tacyt-sdk-python',
      author='ElevenPaths',
      author_email='',
      license='GNU',
      packages=find_packages())