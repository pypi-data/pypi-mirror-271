from setuptools import setup, find_packages

setup(
    name='adcl',
    version='0.1.1',
    author='Maykov Stepan',
    author_email='steve19992@mail.ru',
    description='Data preprocessing and cleaning tools for data science projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/maykov-stepan/ADCL-Automatic-Data-Cleaning',
    packages=find_packages(),
    install_requires=[i.strip() for i in open("requirements.txt").readlines()],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7'
    ],
    python_requires='>=3.7',
)