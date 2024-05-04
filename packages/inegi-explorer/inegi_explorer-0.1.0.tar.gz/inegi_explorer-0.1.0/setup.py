from setuptools import setup

setup(
    name='inegi_explorer',
    version='0.1.0',
    author='Fabio Sol',
    author_email='fabioso2231@gmail.com',
    description='A Python package for exploring and fetching INEGI data without requiring an API key.',
    long_description='INEGI Explorer is a Python package that provides tools for exploring and fetching data from the '
                     'Instituto Nacional de Estadística y Geografía (INEGI) of Mexico. It allows users to easily '
                     'access and analyze INEGI data without the need for an API key. '
                     'The package aims to simplify the process of retrieving and working with '
                     'INEGI data for various purposes',
    long_description_content_type='text/markdown',
    url='https://github.com/FabioSol/INEGIExplorer',
    packages=['inegi_explorer'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'setuptools~=65.5.1',
        'pandas~=1.3.0',
        'typing~=3.7.4'
    ],
)
