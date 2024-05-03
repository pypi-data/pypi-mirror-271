from setuptools import setup, find_packages

long_description = """
This is a basic CLI package that allows you to interact with the Groq API.
It provides different options to select the role type (the way which the model will interact) and
model type (the model which will be used to solve your query).
"""

setup(
    name='groq-cli',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'groq'
    ],
    build_system="setuptools.build_meta",
    setup_requires=['wheel'],
    entry_points={
        'console_scripts': [
            'grc=groq_cli_chat.work:main'
        ],
    },
    description='A CLI package for interacting with the Groq API.',
    long_description=long_description,
    long_description_content_type='text/plain',
    author='Akshad Agrawal',
    url='https://github.com/Akshad135/groq-cli',
)
