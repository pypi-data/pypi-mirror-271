from setuptools import setup, find_packages

setup(
    name='taskprogressbar',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'ipywidgets',
    ],
    python_requires='>=3.6',
    author='N.Wen',
    author_email='nwen@clemson.edu',
    description='A package for displaying a multi-color task progress bar in Jupyter.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='http://github.com/nwen-cu/taskprogressbar',
)
