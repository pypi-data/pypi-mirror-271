from setuptools import setup, find_packages

setup(
    name='adcl',
    version='0.1.7',
    author='Maykov Stepan',
    author_email='steve19992@mail.ru',
    description='Data preprocessing and cleaning tools for data science projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maykov-stepan/ADCL-Automatic-Data-Cleaning',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.16.2,<1.17.0',
        'matplotlib==3.2.2',
        'adtk>=0.6.2',
        'category-encoders>=2.6.3',
        'dtaidistance',
        'matrixprofile>=1.1.10',
        'mxnet==1.7.0.post2'
    ],
    python_requires='>=3.7,<3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='data cleaning, preprocessing, data science, machine learning',
    license='MIT',
    include_package_data=True,
    zip_safe=False
)