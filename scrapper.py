from bs4 import BeautifulSoup
from fpdf import FPDF
import requests

base = "http://www.dtu.ac.in"
endpoints = [
    "/Web/About/quality.php",
    "/Web/About/history.php", 
    "/Web/Administrations/Chancellor.php",  
    "/Web/Administrations/Vice-Chancellor.php", 
    "/Web/Academics/",
    "/Web/Academics/bacheloroftechnology.php",
    "/Web/Academics/bacheloroftechnology-evening.php",
    "/Web/AcademicsPG/",
    "/Web/Departments/MCG/about/index.php",
    "/Web/Departments/EVRT/about/index.php",
    "/Web/Departments/AppliedChemistry/about/",
    "/Web/Departments/AppliedPhysics/about/",
    "/Web/Departments/BioTech/about/",
    "/Web/Departments/Civil/about/",
    "/Web/Departments/CSE/about/",
    "/Web/Departments/DSM/about/",
    "/Web/Departments/Electronics/about/",
    "/Web/Departments/Electrical/about/",
    "/Web/Departments/Environment/about/",
    "/Web/Departments/Humanities/about/",
    "/Web/Departments/InformationTechnology/about/",
    "/Web/Departments/Mechanical/about/",
    "/Web/Departments/design/about/index.php",
    "/Web/Departments/eastcampus/usme/usme.php",
    "/Web/Departments/SE/about/index.php",
    "/Web/Departments/phyedu/about/index.php"
]

filepath = 'D:/College/BTECH PROJECT-1/ChatbotDTU_Final/files/'

def generate_pdf_from_text(title, text):
    pdf = FPDF(format="A4")
    pdf.add_page()
    pdf.add_font('product_sans',fname="Product Sans Regular.ttf")
    pdf.set_font('product_sans',size=12)
    pdf.multi_cell(200,text=text, ln=True)
    pdf.output(filepath + f"{title}.pdf")

for endpoint in endpoints :
    url = base + endpoint
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string
    title = title.strip()
    title = title.replace('|','_')
    title = title.replace(' ','_')
    title = title.replace('___', '_')

    text = ""

    container = soup.find_all('div', attrs={"class":"col2"})

    for paragraph in container:
        text += paragraph.text
    
    generate_pdf_from_text(title,text)