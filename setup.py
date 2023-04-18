from setuptools import find_packages, setup

"""Upload on PyPi :
1. python setup.py bdist_wheel --universal

2. twine upload dist/*
"""

setup(name='thorpy',
      version='2.0',
      description='GUI library for Pygame',
      long_description='ThorPy is a non-intrusive, straightforward GUI kit for Pygame.',
      author='Yann Thorimbert',
      author_email='yann.thorimbert@gmail.com',
      url='http://www.thorpy.org/',
      keywords=['pygame', 'gui', 'menus', 'buttons', 'widgets', 'user interface', 'toolkit'],
      packages=find_packages(),
      include_package_data=True,
      license='MIT')