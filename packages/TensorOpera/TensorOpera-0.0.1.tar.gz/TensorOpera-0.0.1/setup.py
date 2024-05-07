from setuptools import find_packages, setup

setup(
   name='TensorOpera',
   version='1.0',
   description='TensorOpera: Your Generative AI Platform at Scale',
   author='TensorOpera',
   author_email='h@tensoropera.ai',
   packages=find_packages('src/tensoropera', exclude=['test']),
   install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
)