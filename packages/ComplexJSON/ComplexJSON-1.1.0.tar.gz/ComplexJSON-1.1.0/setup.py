from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='ComplexJSON',
    version='1.1.0',
    author='dail45',
    description='This is the simplest module for serialize and deserialize python complex objects',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url="https://github.com/dail45/ComplexJSON",
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='json complexobject serialize',
    python_requires='>=3.6'
)
