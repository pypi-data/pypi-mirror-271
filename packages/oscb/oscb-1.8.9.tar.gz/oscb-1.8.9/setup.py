from setuptools import setup, find_packages
import os

# Get the current directory
here = os.path.abspath(os.path.dirname(__file__))

# Function to collect all files under oscb folder
def find_oscb_files():
    oscb_files = []
    oscb_dir = os.path.join(here, 'oscb')
    for root, _, files in os.walk(oscb_dir):
        for file in files:
            # Get the relative path of the file
            rel_path = os.path.relpath(os.path.join(root, file), oscb_dir)
            oscb_files.append(rel_path)
    return oscb_files

# Include the parent oscb directory and its contents
oscb_files = find_oscb_files()

setup(
    name='oscb',
    version='1.8.9',
    description='Description of your package',
    long_description='Long description of your package',
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/oscb',
    author='OSCB TEAM',
    author_email='your.email@example.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='sample setuptools development',
    packages=find_packages(),
    package_data={'oscb': oscb_files},  # Include all files and folders under oscb directory
    include_package_data=True,
    install_requires=[
        'torch>=1.6.0',
        'numpy>=1.16.0',
        'tqdm>=4.29.0',
        'scikit-learn>=0.20.0',
        'pandas>=0.24.0',
        'six>=1.12.0',
        'urllib3>=1.24.0',
        'outdated>=0.2.0',
        'joblib>=1.3.2'
    ],
)
