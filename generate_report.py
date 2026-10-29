import os
import sys
import numpy as np

# Ensure matplotlib uses writable config
os.environ['MPLCONFIGDIR'] = os.path.join(os.getcwd(), 'tmp_mpl')
os.makedirs('tmp_mpl', exist_ok=True)
os.makedirs('report_assets', exist_ok=True)

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, PageBreak, Spacer, Table, TableStyle, Image, Flowable, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT

# Page tracking data structures
page_records = {}
chapter_start_pages = set()

def to_roman(n):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ['m', 'cm', 'd', 'cd', 'c', 'xc', 'l', 'xl', 'x', 'ix', 'v', 'iv', 'i']
    roman_num = ''
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num

class Bookmark(Flowable):
    def __init__(self, key, is_chapter=False):
        super().__init__()
        self.key = key
        self.is_chapter = is_chapter
        self.width = 0
        self.height = 0
    def draw(self):
        p = self.canv._pageNumber
        page_records[self.key] = p
        if self.is_chapter:
            chapter_start_pages.add(p)

class AnnaUniversityCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        first_ch_page = page_records.get('CH1', 8)
        
        for p_idx, page in enumerate(self.pages):
            self.__dict__.update(page)
            p_num = p_idx + 1
            
            # Title page
            if p_num == 1:
                pass
            elif p_num < first_ch_page:
                # Preliminary roman numerals
                roman_str = to_roman(p_num - 1)
                self.setFont('Times-Roman', 10)
                self.drawCentredString(306 + 9, 36, roman_str)
            else:
                # Chapter Arabic numerals
                arabic_p = p_num - first_ch_page + 1
                self.setFont('Times-Roman', 10)
                self.drawCentredString(306 + 9, 36, str(arabic_p))
                
                # Running Header (suppressed on chapter opening pages)
                if p_num not in chapter_start_pages:
                    self.setFont('Times-Italic', 8.5)
                    self.drawString(90, 841.89 - 42, "ANTI-GRAVITY PROPULSION & STABILIZATION SYSTEM")
                    self.drawRightString(595.27 - 72, 841.89 - 42, "VSBCETC / ANNA UNIVERSITY")
                    self.setLineWidth(0.5)
                    self.setStrokeColor(colors.HexColor('#a0aec0'))
                    self.line(90, 841.89 - 46, 595.27 - 72, 841.89 - 46)
                    
            super().showPage()
        super().save()

print("Base harness compiled successfully.")
