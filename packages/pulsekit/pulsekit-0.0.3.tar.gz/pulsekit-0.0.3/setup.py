from setuptools import setup

setup(name='pulsekit',
      author='author',
      author_email='germanespinosa@gmail.com',
      long_description=open('./pulsekit/README.md').read() + '\n---\n<small>Package created with Easy-pack</small>\n',
      long_description_content_type='text/markdown',
      packages=['pulsekit'],
      include_package_data=True,
      version='0.0.3',
      zip_safe=False)
