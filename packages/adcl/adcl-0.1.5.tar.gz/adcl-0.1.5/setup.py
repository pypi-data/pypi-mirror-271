from setuptools import setup, find_packages

setup(
    name='adcl',
    version='0.1.5',
    description='Automatic Data Cleaning and Preprocessing Library',
    long_description='''This package provides comprehensive data cleaning,
                        preprocessing, and outlier detection functionalities
                        tailored for machine learning and data science projects.''',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourgithub/ADCL-Automatic-Data-Cleaning',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.16.2,<1.17.0',  # Adjusted to accommodate mxnet's requirements
        'matplotlib>=3.5.3',      # Ensure this is compatible with other dependencies
        'adtk>=0.6.2',            # Advanced data analysis toolkit
        'category-encoders>=2.6.3',  # For categorical variable encoding
        'dtaidistance',           # Dynamic Time Warping (DTW) distance calculation library
        'matrixprofile>=1.1.10',  # Matrix profile for time-series analysis
        'mxnet==1.7.0.post2'      # Deep learning framework
        # Add any additional dependencies your package might require
    ],
    python_requires='>=3.7,<3.8',  # Compatible Python versions
    classifiers=[
        'Development Status :: 4 - Beta',  # Change as appropriate
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',  # Ensure license matches your choice
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='data cleaning, preprocessing, data science, machine learning',
    license='MIT',
    include_package_data=True,
    zip_safe=False
)
