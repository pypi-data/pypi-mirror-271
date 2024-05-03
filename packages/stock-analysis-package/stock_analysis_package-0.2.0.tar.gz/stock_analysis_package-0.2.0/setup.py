from setuptools import setup, find_packages

setup(
    name='stock_analysis_package',
    version='0.2.0',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=open('requirements.txt').read().splitlines(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "stock_analysis=stock_analysis.cli:main",
        ]
    },
    author='Samhith Raj',
    author_email='ssaneboi@stevens.edu',
    description="A small python package for stock market analysis",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/samhith-raj/stock_analysis_package"
)
