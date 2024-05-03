from setuptools import setup, find_packages

setup(
    name='PokerNow',
    version='0.7.25',
    author='Zehm',
    author_email='mrtentacleshasallthetalent@gmail.com',
    description='A Python client for interacting with PokerNow games via the web.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Zehmosu/PokerNow/',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'selenium',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
