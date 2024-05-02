from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ml-project-tracker',
    version='0.0.3.dev1',
    description='A package for tracking the ML projects',
    author='Lilia MAHDID',
    author_email='jl_mahdid@esi.dz',
    packages=find_packages(exclude=['requirements.sh', 'build.sh']),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/mahdid-lilia/ML-Project-Tracker',
    keywords=['Deep Learning', 'Machine Learning', 'Wandb', 'Neptune'],
    install_requires=[
        'wandb',
        'numpy',
        'torchvision',
        'torch', 
        "neptune"
        # Add any other dependencies here
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],

)