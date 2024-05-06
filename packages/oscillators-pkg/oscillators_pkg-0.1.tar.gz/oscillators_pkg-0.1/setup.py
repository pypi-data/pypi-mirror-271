from setuptools import setup, find_packages

setup(
    name="oscillators_pkg",
    version="0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for simulating oscillators",
    long_description='kuramoto oscillator package',
    long_description_content_type="text/markdown",
    url="https://github.com/your_username/oscillators_pkg",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "numba",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)