#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users """
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    """
    all_users = storage.all(User).values()
    list_users = []
    for user in all_users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def get_user(user_id):
    """ Retrieves an user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user Object
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users/signup', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def post_user_():
    """
    create a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'first_name' not in request.get_json():
        abort(400, description="Missing first_name")
    if 'last_name' not in request.get_json():
        abort(400, description="Missing last_name")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    if 'phone_no' not in request.get_json():
        abort(400, description="Missing phone_no")
    if 'image_file' not in request.get_json():
        abort(400, description="Missing image_file")
    """if 'confirmed' not in request.get_json():
        abort(400, description="Missing confirmed")"""

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/users/login', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user_login.yml', methods=['POST'])
def login_user():
    """
    login a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.json or 'password' not in request.json:
        abort(400, description="Missing email or password")

    email = request.json['email']
    password = request.json['password']

    # Find the user by email
    # user = User.query.filter_by(email=email).first()
    user = storage.get_user(User, email)


    if not user:
        abort(401, description="Invalid email or password")

    # Verify the password
    if not user.password:
        abort(401, description="Invalid email or password")

    # Generate and return an authentication token
    #later

    # You may want to return additional user information along with the token
    return jsonify({'user': user.to_dict()}), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """
    Updates a user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
