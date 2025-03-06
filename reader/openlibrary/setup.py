from setuptools import setup, find_packages

setup(
    name='openlibrary-api',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python library for interacting with the Internet Archive Open Library API',
    packages=find_packages(),
    install_requires=[
        'requests',  # Assuming requests is needed for making HTTP calls
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)