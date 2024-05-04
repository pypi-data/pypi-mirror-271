
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

   

setup(name='juan_stats',
      version='2.1',
      description='Probability density or mass function calculator for Binomial and Gaussian distributions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages=['juan_stats'],
      author='Juan P',
      zip_safe=False)
