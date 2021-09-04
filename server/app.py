from flask import Flask
import json, sys, os
from flask_cors import CORS
from flasgger import Swagger
import threading
import json
import config
from database.db_connection import db
from route.planned_order import blueprint as blueprint_planned_order

app = Flask(__name__)
CORS(app)
#doc
Swagger(app)
# app.config["DEBUG"] = True
app.config['SWAGGER'] = {'uiversion': 3}
app.config["JSON_AS_ASCII"] = False

# init api
app.register_blueprint(blueprint_planned_order, url_prefix='/api/v1.0/planned_orders')

@app.before_request
def before_req():
    db.connect(True)

@app.after_request
def after_req(response):
    db.close()
    return response

if __name__ == '__main__':
    app.run(
        host='localhost',#os.getenv('SERV_IP', '172.17.196.230'),
        port=9897,#os.getenv('SERV_PORT', 9897),
        threaded=True,
        debug = True
    )
    
