from setuptools import find_packages, setup

setup(
    name="BrazilFiscalReport",
    version="0.3.1",
    long_description="""
    Python library for generating Brazilian auxiliary
    fiscal documents in PDF from XML documents.
    """,
    url="https://github.com/Engenere/BrazilFiscalReport",
    author="Engenere",
    keywords="brazil fiscal report",
    packages=find_packages(),
    license="AGPL-3.0",
    install_requires=["fpdf2", "phonenumbers", "python-barcode"],
)
