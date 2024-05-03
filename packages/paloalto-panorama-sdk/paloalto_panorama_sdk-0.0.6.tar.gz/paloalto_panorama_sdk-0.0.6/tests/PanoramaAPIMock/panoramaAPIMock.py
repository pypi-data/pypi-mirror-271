from flask import Flask, request, jsonify, make_response
from dicttoxml import dicttoxml
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


@app.route('/api/', methods=['GET'])
def keygen():
    type = request.args.get("type")
    user = request.args.get('user')
    password = request.args.get('password')
    if (type == "keygen" and
            user == 'testuser' and
            password == 'testpassword'):
        response_dict = {'apikey': 'mock_apikey_12345'}
        xml_response = dicttoxml(response_dict, custom_root='response', attr_type=False)
        response = make_response(xml_response)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        error_response = dicttoxml({'error': 'Authentifizierung fehlgeschlagen'}, custom_root='response',
                                   attr_type=False)
        response = make_response(error_response, 401)
        response.headers['Content-Type'] = 'application/xml'
        return response


def run_server(port=5002):
    app.run(port=port)
