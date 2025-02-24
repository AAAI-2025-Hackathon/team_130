from fpdf import FPDF
from datetime import datetime

class TherapyReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font('Arial', 'B', 16)
        
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Art Therapy Analysis Report', 0, 1, 'C')
        self.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'This report is for self-reflection purposes only and should not be considered as professional psychological advice.', 0, 0, 'C')
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')
        
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)
        
    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()
        
    def add_disclaimer(self):
        self.add_page()
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Important Disclaimers', 0, 1, 'L')
        self.set_font('Arial', '', 12)
        disclaimer_text = """
        1. This art therapy analysis report is generated using automated tools and AI analysis.
        
        2. The interpretations provided are meant for self-reflection and personal insight only.
        
        3. This report should not be used as a substitute for professional psychological evaluation or therapy.
        
        4. If you are experiencing psychological distress, please seek help from a qualified mental health professional.
        
        5. Art interpretation is subjective and may not accurately reflect your actual psychological state.
        
        6. The analysis provided should be considered as possibilities rather than definitive conclusions.
        """
        self.multi_cell(0, 10, disclaimer_text)

def generate_pdf_report(interpretation, report):
    pdf = TherapyReportPDF()
    
    # Add interpretation section
    pdf.chapter_title('Detailed Art Analysis')
    pdf.chapter_body(interpretation)
    
    # Add report sections (split by headers)
    sections = report.split('\n\n')
    for section in sections:
        if section.strip():
            # Check if the section starts with a number (assuming it's a header)
            if any(section.strip().startswith(str(i)) for i in range(1, 7)):
                pdf.chapter_title(section.split('\n')[0].strip())
                pdf.chapter_body('\n'.join(section.split('\n')[1:]).strip())
            else:
                pdf.chapter_body(section)
    
    # Add disclaimers
    pdf.add_disclaimer()
    
    return pdf 