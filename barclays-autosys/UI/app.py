
from flask import Flask, request, json, make_response, current_app, send_from_directory
from datetime import timedelta
import generate as client
# from simplejson import loads
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__, static_url_path='')
app.debug = True
@app.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('html', path)


@app.route("/nodes", methods=['GET'])
@crossdomain(origin='*')
def nodes():
	# if request.headers['Content-Type'] == 'text/plain':
		# data = request.data

	# elif request.headers['Content-Type'] == 'application/json':
		# data = request.json

	# elif request.headers['Content-Type'] == 'application/octet-stream':
		# data = request.data	 

	# print data
	nodes = client.nodes()
	# links = client.links()
	# print response
	return json.jsonify({"nodes":nodes})


@app.route("/links", methods=['GET'])
@crossdomain(origin='*')
def links():
    # if request.headers['Content-Type'] == 'text/plain':
        # data = request.data

    # elif request.headers['Content-Type'] == 'application/json':
        # data = request.json

    # elif request.headers['Content-Type'] == 'application/octet-stream':
        # data = request.data    

    # print data
    links = client.links()
    # links = client.links()
    # print response
    return json.jsonify({"links":links})

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
