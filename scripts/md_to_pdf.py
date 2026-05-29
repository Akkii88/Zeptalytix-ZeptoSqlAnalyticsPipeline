"""Simple markdown to PDF converter using reportlab.
It writes each markdown line as a paragraph; headings are larger.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import sys

MD = 'slides/Slide_Deck.md'
OUT = 'slides/Slide_Deck.pdf'

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Heading1', fontSize=18, leading=22))
styles.add(ParagraphStyle(name='Heading2', fontSize=14, leading=18))


def md_to_paragraphs(md_text):
    lines = md_text.splitlines()
    elems = []
    for line in lines:
        if line.startswith('# '):
            elems.append(Paragraph(line[2:].strip(), styles['Heading1']))
        elif line.startswith('## '):
            elems.append(Paragraph(line[3:].strip(), styles['Heading2']))
        elif line.strip() == '---':
            elems.append(Spacer(1, 12))
        elif line.strip() == '':
            elems.append(Spacer(1, 6))
        else:
            elems.append(Paragraph(line.strip(), styles['Normal']))
    return elems


def main():
    with open(MD, 'r', encoding='utf-8') as f:
        md = f.read()
    doc = SimpleDocTemplate(OUT, pagesize=letter)
    elems = md_to_paragraphs(md)
    doc.build(elems)
    print('Wrote', OUT)

if __name__ == '__main__':
    main()
