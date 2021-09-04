from flask import Blueprint
from flask import Flask, request, make_response
import json
from flasgger import swag_from
blueprint = Blueprint('planned_order', __name__)

@blueprint.route("", methods=['GET'])
@swag_from('../document/planned_order/list_planned_orders.yml')
def list_planned_orders():
    try:
        # condition = request.args.to_dict()
        # if "role" in condition:
        #     role = condition.get('role')
        #     result = employee.get_all_employee(role=role) 
        #     return make_response(json.dumps(result), 200)
        # result = employee.get_all_employee() 
        return make_response(json.dumps([{"test": 1}]), 200)
    except Exception as e:
        return make_response("Failure: %s." % str(e), 400)