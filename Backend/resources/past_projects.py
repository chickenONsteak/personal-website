import psycopg2
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from db.db_pool import get_cursor, release_connection
from validators.past_projects import AddOneProject

past_projects = Blueprint('past_projects', __name__)

@past_projects.route('/past-projects', methods=['GET', 'PUT'])
def past_projects_endpoint():
    conn = None
    return_value = None
    status_code = 200

    try:
        conn, cursor = get_cursor()
        if request.method == 'GET':
            cursor.execute('SELECT * FROM past_projects')
            results = cursor.fetchall()
            return_value = {'status': 'ok', 'data': results, 'msg': 'Projects successfully retrieved.'}
        elif request.method == 'PUT':
            data = request.get_json()
            AddOneProject().load(data) # will raise ValidationError if invalid request
            cursor.execute(
                'INSERT INTO past_projects (date, title, tag, description, image_url) VALUES (%s, %s, %s, %s, %s)',
                (data['date'], data['title'], data['tag'], data['description'], data['image_url']))
            conn.commit()
            return_value = {'status': 'ok', 'msg': 'Successfully added new project.'}
    except ValidationError as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': f'Invalid request: {err}'}
    except psycopg2.Error as err:
        status_code = 500
        return_value = {'status': 'error', 'msg': 'A server error occurred while retrieving project data. Please try again later.'}
        print(f'Database error in past_projects_endpoint: {err}') # {err} traceback is confidential and should only be reflected in internal systems and not the client, hence it's only in the print statement and not the return_value
    except SyntaxError as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': f'Invalid syntax: {err}'}
    except Exception as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': f'An unexpected error occurred: {err}'}
    finally:
        release_connection(conn)

    return jsonify(return_value), status_code


@past_projects.route('/projects', methods=['POST', 'PATCH', 'DELETE'])
def add_one_project():
    conn = None
    return_value = None
    status_code = 200
    data = request.get_json()

    try:
        conn, cursor = get_cursor()
        if request.method == 'POST':
            # VALIDATE POST REQUEST
            cursor.execute('SELECT * FROM past_projects WHERE id=%s', (data['id']))
            results = cursor.fetchone()
            return_value = {'status': 'ok', 'data': results, 'msg': 'Project successfully retrieved.'}
    finally:
        release_connection(conn)