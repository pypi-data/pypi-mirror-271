from setuptools import setup, find_packages

VERSION = '1.0.7' 
DESCRIPTION = 'A toolkit for quickly implementing llm powered functionalities.'
LONG_DESCRIPTION = 'llm_axe allows you to quickly implement complex interactions for local LLMs, such as function callers, online agents, pre-made generic agents, and more.'

# Setting up
setup(
        name="llm_axe", 
        version=VERSION,
        author="Emir Sahin",
        author_email="emirsah122@gmail.com",
        license="MIT",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'beautifulsoup4>=4.12.3',
            'docstring_parser>=0.16',
            'google>=3.0.0',
            'ollama>=0.1.9',
            'pypdf>=4.2.0',
            'PyYAML>=6.0.1',
            'requests>=2.31.0'
        ], 
         package_data={
        '': ['*.yaml'],
        },
        
        keywords=['python', 'llm axe', 'llm toolkit', 'local llm', 'local llm internet', 'function caller llm'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)