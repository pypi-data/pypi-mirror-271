from fpdf import FPDF
import pandas as pd
from pathlib import Path


class PDFInvoiceGenerator(FPDF):
    """
    Class for generating a PDF invoice from an Excel invoice.

    The Excel file name must be in the following format: '<invoice_number>-<date_format:YYYY.MM.DD>.xlsx'

    For example, if the invoice number is '10003' and the date is '2023.01.18', the Excel file name should be '10003-2023.01.18.xlsx'.

    Args:
        excel_filepath (str): Path to the Excel file containing invoice data.
        logo_filepath (str): Path to the logo image file.
        output_directory (str): Path to the directory where the generated PDF will be saved. Default is "./output".
    """
    def __init__(self, excel_filepath, logo_filepath, output_directory="./output"):
        """
        Initialize the PDFInvoiceGenerator object.

        Args:
            excel_filepath (str): Path to the Excel file containing invoice data.
            logo_filepath (str): Path to the logo image file.
            output_directory (str): Path to the directory where the generated PDF will be saved. Default is "./pdf_invoice".
        """
        # Call the superclass constructor to initialize the PDF object with specified parameters
        super().__init__(orientation='P', unit='mm', format='A4')

        self.excel_filepath = Path(excel_filepath)
        self.logo_filepath = Path(logo_filepath)
        self.output_directory = Path(output_directory)

        # Create the output directory if it doesn't exist
        self.output_directory.mkdir(parents=True, exist_ok=True)

        # Define font styles
        self.title_font = {'family': 'Times', 'size': 13, 'style': 'B'}
        self.value_font = {'family': 'Times', 'size': 11}
        self.header_font = {'family': 'Times', 'size': 10, 'style': 'B'}
        self.data_font = {'family': 'Times', 'size': 8}

        # Define font colors
        self.header_color = (0, 0, 0)
        self.data_color = (80, 80, 80)

        # Define cell dimensions
        self.cell_height = 8
        self.cell_width = 38
        self.title_cell_width = 30
        self.signature_cell_width = 30
        self.logo_width = 10

    def generate(self):
        """
        Generate the PDF invoice.
        """
        filename = self.excel_filepath.stem
        invoice_nr, invoice_date = filename.split('-')
        
        self.add_page()

        # Add invoice number
        self.set_font(**self.title_font)
        self.cell(w=self.title_cell_width, h=self.cell_height,
                 txt=f'Invoice no. ', ln=0)
        self.set_font(**self.value_font)
        self.set_text_color(*self.data_color)
        self.cell(w=self.title_cell_width,
                 h=self.cell_height, txt=invoice_nr, ln=1)

        # Add invoice date
        self.set_font(**self.title_font)
        self.set_text_color(*self.header_color)
        self.cell(w=self.title_cell_width,
                 h=self.cell_height, txt=f'Date: ', ln=0)
        self.set_font(**self.value_font)
        self.set_text_color(*self.data_color)
        self.cell(w=self.title_cell_width,
                 h=self.cell_height, txt=invoice_date, ln=1)
        self.ln()

        # Add invoice data
        self.add_excel_content()

        # Save the PDF
        output_path = self.output_directory / f'{filename}.pdf'
        self.output(str(output_path))

    def add_excel_content(self):
        """
        Add invoice data from Excel to the PDF.
        """
        df = pd.read_excel(self.excel_filepath)
        headers = df.columns

        # Add header row
        self.set_font(**self.header_font)
        self.set_text_color(*self.header_color)
        for header in headers:
            header_formatted = header.title().replace("_", " ")
            self.cell(w=self.cell_width, h=self.cell_height,
                            txt=header_formatted, border=1)
        self.ln()

        # Add data rows
        self.set_font(**self.data_font)
        self.set_text_color(*self.data_color)
        for _, row in df.iterrows():
            for column_data in row:
                self.cell(w=self.cell_width, h=self.cell_height,
                                txt=str(column_data), border=1)
            self.ln()

        # Add total amount due
        for header in headers:
            if header == 'total_price':
                total_sum = df[header].sum()
                self.cell(w=self.cell_width, h=self.cell_height,
                                txt=str(total_sum), border=1, ln=1)
            else:
                self.cell(w=self.cell_width,
                                h=self.cell_height, txt="", border=0)
        self.ln()

        # Add total amount due label and value
        self.set_font(**self.title_font)
        self.set_text_color(*self.header_color)
        self.cell(w=self.cell_width + 10, h=self.cell_height,
                        txt=f'Total Amount Due:  ', ln=0)
        self.set_font(**self.value_font)
        self.set_text_color(*self.data_color)
        self.cell(w=self.cell_width, h=self.cell_height,
                        txt=f'${total_sum}', ln=1)

        # Add signature and logo
        self.set_font(**self.header_font)
        self.set_text_color(*self.header_color)
        self.cell(w=self.signature_cell_width,
                        h=self.cell_height, txt='HardCode E>')
        self.image(str(self.logo_filepath), w=self.logo_width)


if __name__ == "__main__":
    try:
        generator = PDFInvoiceGenerator(excel_filepath='./10003-2023.1.18.xlsx',
                                        logo_filepath='./python.png')
        generator.generate()
        print("\n--- PDF invoice generated successfully ---\n")
    except Exception as e:
        print("\n--- Failure in generating PDF invoice: ---\n")
        print(f"\nError message: {e}\n")
