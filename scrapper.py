from bs4 import BeautifulSoup
from fpdf import FPDF
import requests

#Add the base address to your website here, from which you want to extract data
base = "link_to_website"

#Add the endpoints here
endpoints = [
    'example_enpoint1',
    'example_endpoint2'
]

#Add path where you want to save your file
filepath = 'files/path'

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

    #scrap data by analysing the html structure of your webpage
    container = soup.find_all('div', attrs={"class":"col2"})

    for paragraph in container:
        text += paragraph.text
    
    generate_pdf_from_text(title,text)