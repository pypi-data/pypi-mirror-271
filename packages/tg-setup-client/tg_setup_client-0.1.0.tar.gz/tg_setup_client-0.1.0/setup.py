from setuptools import setup, find_packages

setup(
    name='tg_setup_client',  # The package name for pip installation
    version='0.1.0',  # Increment this for every release
    packages=find_packages(),  # Automatically find all packages in the project
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    description='A package to initialize and authenticate Telegram client using Telethon',
    long_description=open('README.md').read(),  # A detailed description from a README file
    long_description_content_type='text/markdown',
    author='thomasjjj',  # Replace with your name
    url='https://github.com/thomasjjj/tg_setup_client',  # URL for the project (e.g., GitHub repo)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'telethon>=1.24.0',  # Add other dependencies as needed
    ],
    python_requires='>=3.6',  # Specify the minimum Python version
)
