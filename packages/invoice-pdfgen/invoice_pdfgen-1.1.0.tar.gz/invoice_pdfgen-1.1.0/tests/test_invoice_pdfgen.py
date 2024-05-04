import unittest
from invoice_pdfgen import PDFInvoiceGenerator
from pathlib import Path


class TestPDFInvoiceGenerator(unittest.TestCase):
    def test_generate_invoice(self):
        # Create an instance of PDFInvoiceGenerator with sample data
        generator = PDFInvoiceGenerator(
            excel_filepath='tests/testing_resources/10003-2023.1.18.xlsx',
            logo_filepath='tests/testing_resources/python.png')

        # Generate the PDF invoice
        generator.generate()

        # Check if the PDF file is created
        expected_output = Path('tests/output') / '10003-2023.1.18.pdf'
        self.assertTrue(expected_output.exists(), f"Expected {
                        expected_output} to be generated.")


if __name__ == '__main__':
    unittest.main()
