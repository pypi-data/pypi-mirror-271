from setuptools import setup, find_packages

setup(
    name='hrbdataproject',
    version='2.2',
    packages=find_packages(),
    #py_modules=['data_quality_checks'],  # Specify the individual Python file here
    description='A library for data quality checks in Databricks notebooks',
    author='Harun Raseed Basheer',
    author_email='harun.raseed093@gmail.com',
    url='https://github.com/harunraseed/hrbdataproject',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)