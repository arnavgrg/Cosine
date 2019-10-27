from flask import Flask, render_template, jsonify, request
from flask_sockets import Sockets
import datetime
import time
import json
import textstat
import requests
import traceback
from pdf2image import convert_from_path
from wand.color import Color
from wand.image import Image
from PIL import ImageFont, ImageDraw, ImageEnhance
import PIL

#__file__ = "~/Workspace/Calhacks-2019/app/"

#__name__ = "~/Workspace/Calhacks-2019/app/"

import os
import sys
sys.path.insert(0,'text_summarization/')
sys.path.insert(0,'./')

print(sys.path)
print(__file__)
print(__name__)

from tools import pdfParse, text_sum
from tools import email_client as email_form
#from . import pdfParse
#from . import email_client as email_form

#from app.text_summarization import text_sum

app = Flask(__name__)

sockets = Sockets(app)

DB = json.load(open("documentDataDB.json"))

RESPONSES = [None]

#def send_text_to_api():
#	print convert_pdf_to_png("static/tesla.pdf")
#	return

@app.route("/update")
def updated():
    print("updated")
    with open('documentDataDB.json', 'w') as outfile:
            json.dump(DB, outfile, indent=4)
    headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjY4MTg1ZmYxLTRlNTEtNGNlOS1hZjFjLTY4OTgxMjIwMzMxNyJ9.eyJUb2tlblR5cGUiOjUsIklzc3VlSW5zdGFudCI6MTU3MjEyOTYyNiwiZXhwIjoxNTcyMTU4NDI2LCJVc2VySWQiOiIyMDVhMWYxNS0yNTc0LTQxMWQtYjZlMC1hMDcyZTRlNTMyNTMiLCJzaXRlaWQiOjEsInNjcCI6WyJzaWduYXR1cmUiLCJjbGljay5tYW5hZ2UiLCJvcmdhbml6YXRpb25fcmVhZCIsImdyb3VwX3JlYWQiLCJwZXJtaXNzaW9uX3JlYWQiLCJ1c2VyX3JlYWQiLCJ1c2VyX3dyaXRlIiwiYWNjb3VudF9yZWFkIiwiZG9tYWluX3JlYWQiLCJpZGVudGl0eV9wcm92aWRlcl9yZWFkIiwiZHRyLnJvb21zLnJlYWQiLCJkdHIucm9vbXMud3JpdGUiLCJkdHIuZG9jdW1lbnRzLnJlYWQiLCJkdHIuZG9jdW1lbnRzLndyaXRlIiwiZHRyLnByb2ZpbGUucmVhZCIsImR0ci5wcm9maWxlLndyaXRlIiwiZHRyLmNvbXBhbnkucmVhZCIsImR0ci5jb21wYW55LndyaXRlIl0sImF1ZCI6ImYwZjI3ZjBlLTg1N2QtNGE3MS1hNGRhLTMyY2VjYWUzYTk3OCIsImlzcyI6Imh0dHBzOi8vYWNjb3VudC1kLmRvY3VzaWduLmNvbS8iLCJzdWIiOiIyMDVhMWYxNS0yNTc0LTQxMWQtYjZlMC1hMDcyZTRlNTMyNTMiLCJhdXRoX3RpbWUiOjE1NzIxMjkyMTIsInB3aWQiOiJmYzUwYmZlNS05YzUzLTQwMGUtOGYzMC02YjU3MDY1MDVkYjIifQ.r5CE9QneRUa3C8oAyRD2f3a_Ue8HJAyq6mKO8tx9eFzaoL5LfTIV-Dj10kpFbCQ_pxbYMWVOZ2lVDc-folOYtls3jMY6-he9d1DneK3ZAxH5rk57lHke4LZZCHZzbosPUIkSv7BVEdQG0kv9Ne2zG0Fc4r-FHciMaGMVdeakmVEbv966Dp9wmlF0Bz6BabYfFzWiFaH8Go0JQli0Su0NVW8HiX1Fy9MEweAwpGE0Aega0tk1yemo0qB1TYwfIUln0-2anBapZ40l3fj5qDfJiLUNRkPKHj_LRoFKV3VUc6_suY5kEWxkVMWf8zchSbXAa9FXB5yULewkYoMIzjiirg',
    'Accept': 'application/json',
    }

    res = requests.get('https://demo.docusign.net/clickapi/v1/accounts/82472fcb-a7cd-4ca1-831f-c2dbc8b9d423/clickwraps/dd2f59a4-6acf-400a-82da-8bb2cf5c3533/users', headers=headers)
    print("IM HERE")
    print(res.text)
    print("ENDNED")

    RESPONSES[-1] = res.json()
    return "AYY"

@sockets.route('/getUpdatedFromDocusign')
def echo_socket_docusign(ws):
    prev = "AYYY"
    while True:
        try:
            if prev != RESPONSES[-1]:
                updated()
                ws.send(str(RESPONSES[-1]))
                prev = RESPONSES[-1]
        except Exception as exp:
    #	print traceback.print_exc()
            print("Exception in get updated from docusign" + str(exp))
        time.sleep(.1)

def convert_pdf_to_png(filenameVal):
	pdf = Image(filename=filenameVal, resolution=200)

	pages = len(pdf.sequence)

	image = Image(
		width=pdf.width,
		height=pdf.height * pages
	)

	for i in xrange(pages):
		image.composite(
			pdf.sequence[i],
			top=pdf.height * i,
			left=0
		)
	image.background_color = Color("white")
	image.alpha_channel = 'remove'
	image.save(filename="out.png")
	return remove_points_from_image(filenameVal)

def remove_points_from_image(filenameVal):
	source_img = PIL.Image.open("out.png").convert("RGBA")
	width, height = source_img.size
	draw = ImageDraw.Draw(source_img)
	for val in DB[filenameVal.partition("/")[2]].keys():
		y = float(height * float(val))
		# print(y)
		draw.rectangle(((0, y), (width, y+40)), fill="white")
	# draw.text((20, 70), "something123", font=ImageFont.truetype("font_path123"))
	source_img.save("newFile.png", "png")
	return pdfParse.Get_text_from_image("newFile.png")

def extract_unused_sentences(fileName):
	pages = convert_from_path('pdf_file', 500)
	for page in pages:
		convert_pdf_to_png("static/tesla.pdf").save('out.png', 'png')
	DB[fileName].values()
	return 

@sockets.route('/chrisDocusignEndpointDotExe')
def echo_socket(ws):
    while True:
        if not ws.closed:
            message = ws.receive()
            try:
                # print(message)\
                position, fileName = message.split(",")
                print("Success")
                smallFilename = fileName.replace("/static/", "")
                if smallFilename not in DB:
                    DB[smallFilename] = {}
                if position not in DB[smallFilename]:
                    DB[smallFilename][position] = 0
                DB[smallFilename][position] += 1
                ws.send(str(datetime.datetime.now()))
            except Exception as exp:
                print("ERROR" + str(exp))
    #	print message
            # print(DB)
        time.sleep(.1)

@app.route("/pdfAnalyticsGenerate/<documentName>")
def doAnalytics(documentName):
	return render_template('pdfThingGet.html')

@app.route("/pdfAnalyticsView/<documentName>")
def doAnalyticsView(documentName):
	with open('documentDataDB.json', 'w') as outfile:
		json.dump(DB, outfile, indent=4)
	return jsonify(DB.get(documentName, []))
	# return render_template('pdfThingView.html', MY_PDF_AYYO="/static/{}".format(documentName))

@app.route("/getDataOnDocument/<documentName>")
def getData(documentName):
	points = []
	width = float(request.args.get("width"))
	height = float(request.args.get("height"))
	# raw_input(str(width) + str(height))
	for key, val in DB.get(documentName, {}).items():
		try:
			# print(int(val/5))

			val = float(val)
			if height == 0:
				height = 100
			y = height * (float(key))
			if y < 100:
				y += 100
			for i in range(int(val / 5)):
				x = 40
				while x < width-20:
					points.append({"x": int(x), "y": int(y), "value": int(val/5)})
					x += 10
				y += 10
		except:
			pass
	return jsonify({"data": points})

@app.route('/echo_test', methods=['GET'])
def echo_test():
	return render_template('display.html')

@app.route('/admin', methods=['GET'])
def admin():
	return render_template('admin.html')

@app.route('/index', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/textAnalytics', methods=['GET', 'POST'])
def text_analytics():
	return jsonify({"result": textstat.flesch_reading_ease(request.form.get("text"))})
	# return render_template('index.html')

if __name__ == '__main__':
	# send_text_to_api()
	app.run(debug=True)
	# Start with gunicorn -k flask_sockets.worker app:app