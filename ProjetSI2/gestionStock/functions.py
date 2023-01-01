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
    r = f"date:{info['date']}\n"
    r += f"fournisseur:{info['fournisseur']}\n"
    r += "code produits : quantité\n"

    l = list(info.lists()) #une liste des 2-tuple (key:list(val))
    
    #3 = n° tuple produits
    #4 = n° tuple quantité
    for i in range(len(l[3][1])):
        r += f"{l[3][1][i]} : {l[4][1][i]}\n" 
        
    return r