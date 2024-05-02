from setuptools import setup, find_packages

setup(
    name='stylepy',
    version='0.2',
    packages=find_packages(),
    install_requires=[],
    author='Venkatraman.R',
    author_email='ramsunvtech@gmail.com',
    description='Format CLI output like HTML.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/web-slate/stylepy',
    license='MIT',
    python_requires=">=3.3",
)