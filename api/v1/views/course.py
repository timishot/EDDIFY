#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from models.course import Course 
from models.category import Category
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from

@app_views.route('/category/<category_id>', methods=['GET'], strict_slashes=False)
def get_courses(category_id):
    """
    Retrieves a list of all cities
    """
    list_courses = []
    category = storage.get(Category, category_id)
    if not category:
        abort(404)
    for course in category.course:
        list_courses.append(course.to_dict())
    return jsonify(list_courses)


@app_views.route('/courses/<course_id>/', methods=['GET'],
                 strict_slashes=False)
def get_course(course_id):
    """ Retrieves an course """
    course = storage.get(Course, course_id)
    if not course:
        abort(404)
    return jsonify(course.to_dict())



@app_views.route('/courses/<course_id>/', methods=['DELETE'],
                 strict_slashes=False)
def delete_course(course_id):
    """
    Deletes a course based on id provided
    """
    course = storage.get(Course, course_id)

    if not course:
        abort(404)
    storage.delete(course)
    storage.save()

@app_views.route('/category/<category_id>/courses', methods=['POST'], strict_slashes=False)
def post_course(category_id):
    """
    Creates a Course
    """
    category= storage.get(Category, category_id)
    if not category:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'category_name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Course(**data)
    instance.category_id = category.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)

@app_views.route('/courses/<course_id>/', methods=['PUT'],
                 strict_slashes=False)
def put_course(course_id):
    """
    Updates a Course
    """
    course = storage.get(Course, course_id)
    if not course:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(course, key, value)
    storage.save()
    return make_response(jsonify(course.to_dict()), 200)