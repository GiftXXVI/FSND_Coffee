import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# CORS Headers


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,DELETE,OPTIONS')
    return response


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    form_drinks = [drink.short() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': form_drinks
    })


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
def get_drinks_detail(drink_id):
    drinks = Drink.query.all()
    form_drinks = [drink.long() for drink in drinks]
    return jsonify({
        'success': True,
        'drinks': form_drinks
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
def post_drinks():
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        drink = Drink(title=body.get('title'), recipe=body.get('recipe'))
        drink.refresh()
        form_drink = drink.long()
        drink.dispose()
        return jsonify({
            'success': True,
            'drinks': form_drink
        })


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
def patch_drink(drink_id):
    body = request.get_json()
    if body is None:
        abort(400)
    else:
        drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
        if drink is None:
            abort(422)
        else:
            drink.title = body.get('title')
            drink.recipe = body.get('recipe')
            drink.update()
            form_drink = drink.long()
            drink.dispose()
            return jsonify({
                'success':True,
                'drinks':form_drink
            })


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id):
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()
    if drink is None:
        abort(422)
    else:
        drink.delete()
        drink.dispose()
        return jsonify({
            'success':True,
            'delete':id
        })


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success':False,
        'error':404,
        'message':'not found'
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success':False,
        'error':400,
        'message':'bad request'
    }), 400



'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
