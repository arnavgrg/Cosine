import os
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import gc
import json

DB = json.load(open("ocrCache.json"))
print(type(DB))

def Get_text_from_image(pdf_path):
    if pdf_path in DB:
        return DB[pdf_path]
    pdf=wi(filename=pdf_path,resolution=300)
    pdfImg=pdf.convert('jpeg')
    imgBlobs=[]
    extracted_text=[]
    for img in pdfImg.sequence:
        page=wi(image=img)
        imgBlobs.append(page.make_blob('jpeg'))
    for imgBlob in imgBlobs:
        im=Image.open(io.BytesIO(imgBlob))
        text=pytesseract.image_to_string(im,lang='eng')
        extracted_text.append(text)
    text = ([i.replace("\n","") for i in extracted_text])
    DB[pdf_path] = text
    with open('ocrCache.json', 'w') as outfile:
        json.dump(DB, outfile, indent=4)
    return text

if __name__ == '__main__':
    print(Get_text_from_image("static/tesla.pdf"))
