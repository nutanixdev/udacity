from setuptools import setup, find_packages

setup(
    name='evaluate-udacity-student-blueprint',
    version='0.1',
    description='Take an exported Nutanix Calm Blueprint in JSON format and '
                + 'evaluate various configurations based on a supplied JSON '
                + 'criteria file.',
    author='Chris Rasmussen',
    author_email='crasmussen@nutanix.com',
    install_requires=[
        'wheel',
        'humanize',
        'colorama',
        'dotty-dict'
    ],
    packages=find_packages('.'),
    package_dir={'': '.'}
)
