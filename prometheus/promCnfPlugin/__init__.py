from flask import json,request,Flask, url_for,jsonify
from functools import wraps
from ruleFile import fileBuilder

__author__="panos"
__date__ ="$Feb 28, 2016 3:32:07 PM$"

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"


@app.route('/prometheus/alerts', methods = ['GET', 'POST', 'PUT'])
def api_alerts():
    if request.method == 'POST':
        conf = json.loads(request.data)
        srv_id = conf['service']
        rf = fileBuilder(srv_id, conf['rules']) 
        status = rf.writeFile();
        
        return ''+status
    elif request.method == 'PUT':    
        return '(PUT) get alert for '
    


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp





if __name__ == "__main__":
    global logger
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.handlers.RotatingFileHandler("alertconf.out", maxBytes=2048000, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    app.run()
