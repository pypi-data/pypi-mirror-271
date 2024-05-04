from setuptools import setup, find_packages


setup(
    name='ConsoleVerse',
    version='0.1.0',
    description='A Python library for managing console output',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    author='Sebastian Martinez',
    author_email='sebastian.martinez.serna@gmail.com',
    url='https://github.com/JuanS3/consoleverse',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
)
