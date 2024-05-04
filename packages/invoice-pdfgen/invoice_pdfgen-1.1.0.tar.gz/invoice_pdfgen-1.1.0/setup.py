from setuptools import setup, find_packages


# Read the contents of README.md file to set as the long description
with open("README.md", "r") as fh:
    long_description = fh.read()

# Setup function call with package information
setup(
    name='invoice_pdfgen',  # Package name
    # Automatically find all packages and sub-packages within the directory
    packages=find_packages(),
    version='1.1.0',  # Package version
    license='MIT',  # License type
    # Brief description
    description='This package can be used for generating PDF invoices from Excel invoices.',
    long_description=long_description,  # Use README.md content as long description
    # Specify that long description is in Markdown format
    long_description_content_type='text/markdown',
    author='emads22',  # GitHub username    
    author_email='emads@email.com',  # Author email
    url='https://github.com/emads22/invoice-pdfgen-python',  # GitHub repository URL
    keywords=['invoice', 'excel', 'pdf'],  # Keywords for the package
    install_requires=['fpdf', 'openpyxl', 'pandas'],  # Required dependencies
    classifiers=[  # Classifiers for the package
        'Development Status :: 3 - Alpha',  # Development status
        'Intended Audience :: Developers',  # Intended audience
        'Topic :: Software Development :: Build Tools',  # Topic
        'License :: OSI Approved :: MIT License',  # License information
        'Programming Language :: Python :: 3.8',  # Supported Python versions
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
