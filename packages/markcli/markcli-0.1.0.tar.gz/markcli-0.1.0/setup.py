from setuptools import find_packages, setup

with open("README.md") as readme:
        description = readme.read()

setup(
    name='markcli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'jsonargparse',
    ],
    python_requires='>=3.8',
    description="A Jupyter-inspired tool to create documentation of CLI tools.",
    license='Apache License 2.0',
    long_description=description,
    long_description_content_type="text/markdown",
    #url='https://github.com/scribe-security/simple-sarif',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    entry_points={
        'console_scripts': [
            'markcli=markcli:main',  # "mycommand" is the command you'll use in the terminal
        ],
    },
)
