from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='genmax',
    version='0.1.6',
    author='Raza Balbale',
    description='A simple code generation tool.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://https://github.com/razaibi/genmax/',
    project_urls={
        'Documentation': 'https://github.com/razaibi/genmax/README.md',
        'Source': 'https://github.com/razaibi/genmax',
        'Tracker': 'https://github.com/razaibi/genmax/',
    },
    keywords='cli code generator automation',
    packages=find_packages(),
    install_requires=[
        "PyYAML==6.0",
        "Jinja2==3.1.2",
        "pluralizer==1.2.0",
        "case-switcher==1.3.13",
        "typer==0.9.0"
    ],
    license='Apache 2.0',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'gmx=gmx.main:app',
        ],
    },
)
