from setuptools import setup, find_packages

setup(
    name='TijaToolsProgressRing',
    version='0.1.0',
    description='A customizable progress ring for terminal applications.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Janos Tigyi',
    author_email='tigyi.janos@bugfactory.hu',
    #url='https://github.com/yourusername/TijaToolsProgressRing',
    packages=find_packages(),
    install_requires=[
        'asyncio'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
