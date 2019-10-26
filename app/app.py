# Copy of http://stackoverflow.com/a/20104705
from flask import Flask, render_template, jsonify, request
from flask_sockets import Sockets
import datetime
import time
import json

app = Flask(__name__)

sockets = Sockets(app)

DB = json.load(open("documentDataDB.json"))

@sockets.route('/chrisDocusignEndpointDotExe')
def echo_socket(ws):
	while True:
		message = ws.receive()
		try:
			position, fileName = message.split(",")
			smallFilename = fileName.replace("/static/", "")
			if smallFilename not in DB:
				DB[smallFilename] = {}
			if position not in DB[smallFilename]:
				DB[smallFilename][position] = 0
			DB[smallFilename][position] += 1
		except Exception as exp:
			print("ERROR")
		# print(DB)
		ws.send(str(datetime.datetime.now()))
		time.sleep(.1)

@app.route("/pdfAnalyticsGenerate/<documentName>")
def doAnalytics(documentName):
	return render_template('pdfThingGet.html', MY_PDF_AYYO="{}".format(documentName))

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
	print(width, height)
	for key, val in DB.get(documentName, {}).iteritems():
		
		# print(int(val/5))

		val = float(val)
		if height == 0:
			height = 170
		y = height * (float(key))
		if y < 170:
			y += 170
		for i in range(int(val / 5)):
			x = 60
			while x < width-40:
				points.append({"x": x, "y": y, "value": val/5})
				x += 20
			y += 20
	return jsonify(points)

@app.route('/echo_test', methods=['GET'])
def echo_test():
	return render_template('display.html')

if __name__ == '__main__':
	app.run(debug=True)
	# Start with gunicorn -k flask_sockets.worker app:app