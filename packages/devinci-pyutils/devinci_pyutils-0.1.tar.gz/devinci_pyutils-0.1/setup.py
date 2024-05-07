from setuptools import setup, find_packages

setup(
    name='devinci-pyutils',
    version='0.1',
    author='devinci-it',
    description='Collection of Python utility modules for developers.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gist.github.com/devinci-it/d432708e796d6e6160efe13ee6cc7bbc/',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.6',
    setup_requires=['setuptools', 'wheel'],

)
