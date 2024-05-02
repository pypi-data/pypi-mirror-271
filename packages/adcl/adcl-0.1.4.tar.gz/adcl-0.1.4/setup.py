from setuptools import setup, find_packages

setup(
    name='adcl',
    version='0.1.4',
    author='Maykov Stepan',
    author_email='steve19992@mail.ru',
    description='Data preprocessing and cleaning tools for data science projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maykov-stepan/ADCL-Automatic-Data-Cleaning',
    packages=find_packages(),
    install_requires=[
    'numpy>=1.15.0',
    'pandas>=1.0.5,<=1.3.5',
    'tensorflow>=2.11.0',
    'mxnet>=1.4.0',
    'openml>=0.14.1',
    'scipy>=1.5.4',
    'dtaidistance>=2.3.11',
    'matrixprofile>=1.1.10',
    'pyod>=1.1.3',
    'adtk>=0.6.2',
    'scikit-learn>=1.0.2',
    'matplotlib>=3.5.3',
    'category-encoders>=2.6.3'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.7',
)