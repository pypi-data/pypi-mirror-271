from setuptools import setup, find_packages

setup(
    name='SQLLink',
    version='1.0.0',
    author='AK',
    author_email='ak@stellar-code.com',
    description='SQLLink is a simple library which enables you to use SQLite databases without SQL.',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/TRC-Loop/SQLLink',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'sqlite3',  # This is part of the Python standard library for Python versions 3.x
    ],
    python_requires='>=3.6',
)
