import logging, logging.handlers, sys, yaml, os.path, httplib
from flask import json,request,Flask, url_for,jsonify
from functools import wraps
from ruleFile import fileBuilder

__author__="panos"
__date__ ="$Feb 28, 2016 3:32:07 PM$"

app = Flask(__name__)

global promPath 
promPath = '/opt/Monitoring/prometheus/'

@app.route("/")
def hello():
    urls =  "I am alive..."
    return urls


'''
{"service":"NF777777","rules":[{"description": "Rule_#1", "summary": "Rule combines two metrics", "duration": "4m", "notification_type": 2, "condition": "metric1 - metric2 > 0.25", "name": "Rule 1", "labels":["id = docker","mode = user"]},{"description": "Rule_#2", "summary": "Rule combines two other metrics", "duration": "4m", "notification_type": 2, "condition": "metric3 - metric4 > 0.25", "name": "Rule 2", "labels":["id = docker","mode = user1"]}]}
'''
@app.route('/prometheus/rules', methods = ['POST'])
def api_rules():
    if request.method == 'POST':
        conf = json.loads(request.data)
        if 'service' in conf:
            srv_id = conf['service']
        else:
            message = {
                'status': 500,
                'message': 'KeyError',
            }
            resp = jsonify(message)
            resp.status_code = 500
            return resp
        rf = fileBuilder(srv_id, conf['rules'], promPath)
    status = rf.writeFile();
    message = {
                'status': 200,
                'message': status,
            } 
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    elif request.method == 'GET':    
        return '(GET) get alert for '
    elif request.method == 'PUT':    
        return '(PUT) get alert for '

@app.route('/prometheus/rules/<srv_id>', methods = ['GET','DELETE'])
def api_rules_per_srv(srv_id):
    if request.method == 'DELETE':
        fname = promPath+'rules/'+srv_id.strip()+'.rules'
        if os.path.isfile(fname):
            os.remove(fname)
            with open(promPath+'prometheus.yml', 'r') as conf_file:
                conf = yaml.load(conf_file)
                for rf in conf['rule_files']:
                    if fname in rf:
                        conf['rule_files'].remove(rf)
                        with open(promPath+'prometheus.yml', 'w') as yml:
                            yaml.safe_dump(conf, yml)
			continue
	    reloadServer()
            message = {
                'status': 200,
                'message': 'File DELETED (' +fname+')',
            }
        else:
            message = {
                'status': 200,
                'message': 'File NOT FOUND (' +fname+')',
            }
        resp = jsonify(message)
        resp.status_code = 404  
        return resp

    elif request.method == 'GET':
        fname = promPath+'rules/'+srv_id.strip()+'.rules'
        if os.path.isfile(fname):
            with open(fname, 'r') as conf_file:
                conf = yaml.load(conf_file)
                js_obj = json.dumps(conf)
            return js_obj
        else:
            message = {
                'status': 200,
                'message': 'File ' +fname+' not found',
            }
            return jsonify(message)
    
@app.route('/prometheus/configuration', methods = ['GET', 'POST'])
def api_conf():
    if request.method == 'GET':
        with open(promPath+'prometheus.yml', 'r') as conf_file:
            conf = yaml.load(conf_file)
            js_obj = json.dumps(conf)
            print(js_obj)
        return js_obj
    elif request.method == 'POST':    
        return 'Not supported yet'
    


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

def reloadServer():
    httpServ = httplib.HTTPConnection("localhost", 9090)
    httpServ.connect()
    httpServ.request("POST", "/-/reload")
    response = httpServ.getresponse()
    httpServ.close()




if __name__ == "__main__":
    global promPath 
    promPath = '/opt/Monitoring/prometheus/'
    global logger
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.handlers.RotatingFileHandler("alertconf.out", maxBytes=2048000, backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    app.run()
