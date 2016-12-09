
from flask import Flask, request, json

import client as client
# from simplejson import loads

app = Flask(__name__)
app.debug = True
@app.route("/pretrain", methods=['POST'])
def pretrain():
	if request.headers['Content-Type'] == 'text/plain':
		data = request.data

	elif request.headers['Content-Type'] == 'application/json':
		data = request.json

	elif request.headers['Content-Type'] == 'application/octet-stream':
		data = request.data	        

	print data
	response = client.pretrain(data)
	return json.jsonify({"response":response})

@app.route("/train", methods=['POST'])
def train():
	if request.headers['Content-Type'] == 'text/plain':
		data = request.data

	elif request.headers['Content-Type'] == 'application/json':
		data = request.json

	elif request.headers['Content-Type'] == 'application/octet-stream':
		data = request.data	        

	print data
	response = client.train(data)
	return json.jsonify({"response":response})


@app.route("/predict", methods=['POST'])
def predict():
	if request.headers['Content-Type'] == 'text/plain':
		data = request.data

	elif request.headers['Content-Type'] == 'application/json':
		data = request.json

	elif request.headers['Content-Type'] == 'application/octet-stream':
		data = request.data	 

	print data
	response = client.predict(data)
	print response
	return json.jsonify({"response":response})

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
