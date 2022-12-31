# pour les fonction qui ne sont pas des views
#import repotlab
from reportlab.pdfgen import canvas

def pdf_gen(content,path='./gestionStock/files/doc.pdf'):
    p = canvas.Canvas(path)               # Init a PDF object
    p.drawString(100, 100, content)       # Draw a simple String  
    
    # Create the PDF
    p.showPage()                         
    p.save()
    return path.split('/')[-1]

def cleaning_post_info(info):
    r = ''
    for i in info:
        if i != "csrfmiddlewaretoken":
            r += f"{i}:{info[i]}\n"
    return r