from setuptools import setup, find_packages


# Setup function call with package information
setup(
    name='invoice_pdfgen',  # Package name
    # Automatically find all packages and sub-packages within the directory
    packages=find_packages(),
    version='1.0.0',  # Package version
    license='MIT',  # License type
    # Brief description
    description='This package can be used for generating PDF invoices from Excel invoices.',
    author='Emad S.',  # Author name
    author_email='emads@email.com',  # Author email
    url='https://example.com',  # Project URL
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
