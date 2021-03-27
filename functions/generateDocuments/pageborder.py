import docx
from docx.oxml.xmlchemy import OxmlElement
from docx.oxml.shared import qn

doc = docx.Document()
sec_pr = doc.sections[0]._sectPr # get the section properties el
# create new borders el
pg_borders = OxmlElement('w:pgBorders')
ignoreheader = OxmlElement('w:bordersDoNotSurroundHeader')
# specifies how the relative positioning of the borders should be calculated
pg_borders.set(qn('w:offsetFrom'), 'text')
for border_name in ('top', 'left', 'bottom', 'right',): # set all borders
    border_el = OxmlElement(f'w:{border_name}')
    border_el.set(qn('w:val'), 'single') # a single line
    border_el.set(qn('w:sz'), '4') # for meaning of  remaining attrs please look docs
    if border_name in ('top','bottom'):
        border_el.set(qn('w:space'), '1')
    else:
        border_el.set(qn('w:space'), '4')
    border_el.set(qn('w:color'), 'auto')
    pg_borders.append(border_el) # register single border to border el
sec_pr.append(pg_borders) # apply border changes to section
sec_pr.append(ignoreheader)

doc.save('border_test.docx')
