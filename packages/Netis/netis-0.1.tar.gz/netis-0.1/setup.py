from setuptools import setup, find_packages

setup(
    name='Netis',
    version='0.1',
    packages=find_packages(),
    author='Franek S',
    author_email='znikafranek@gmail.com',
    description='A simple file framework for Python',
    long_description=open('README.MD').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
