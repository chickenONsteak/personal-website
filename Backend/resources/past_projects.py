import psycopg2
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from db.db_pool import get_cursor, release_connection
from validators.projects import AddOneProject

projects = Blueprint('projects', __name__)

@projects.route('/past-projects', methods=['GET', 'PUT'])
def projects_endpoint():
    conn = None
    return_value = None
    status_code = 200
    try:
        conn, cursor = get_cursor()
        if request.method == 'GET':
            # RETRIEVE ALL PROJECTS
            cursor.execute('SELECT * FROM projects')
            results = cursor.fetchall()
            return_value = {'status': 'ok', 'data': results, 'msg': 'Projects successfully retrieved.'}
        elif request.method == 'PUT':
            # ADD NEW PROJECT
            data = request.get_json()
            AddOneProject().load(data) # will raise ValidationError if invalid request
            cursor.execute(
                'INSERT INTO projects (date, title, tag, description, image_url) VALUES (%s, %s, %s, %s, %s)',
                (data['title'], data['completed_date'], data['categories'], data['description'], data['image_urls']))
            conn.commit()
            return_value = {'status': 'ok', 'msg': 'Successfully added new project.'}
    except ValidationError as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': f'Invalid request: {err}'}
    except psycopg2.Error as err:
        status_code = 500
        return_value = {'status': 'error', 'msg': 'A server error occurred while retrieving project data. Please try again later.'}
        print(f'Database error in projects_endpoint: {err}') # {err} traceback is confidential and should only be reflected in internal systems and not the client, hence it's only in the print statement and not the return_value
    except SyntaxError as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': f'Invalid syntax: {err}'}
    except Exception as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': f'An unexpected error occurred: {err}'}
    finally:
        release_connection(conn)
    return jsonify(return_value), status_code


@projects.route('/projects', methods=['POST', 'PATCH', 'DELETE'])
def add_one_project():
    conn = None
    return_value = None
    status_code = 200
    data = request.get_json()

    try:
        conn, cursor = get_cursor()
        if request.method == 'POST':
            # RETRIEVE ONE PROJECT BY PROJECT ID
            cursor.execute('SELECT * FROM projects WHERE id=%s', (data['id']))
            results = cursor.fetchone()
            return_value = {'status': 'ok', 'data': results, 'msg': 'Project successfully retrieved.'}
        elif request.method == 'PATCH':
            # UPDATE ONE PROJECT BY PROJECT ID
            cursor.execute('SELECT * FROM projects WHERE id=%s', (data['id'])) # get data that matches the id
            results = cursor.fetchone()
            cursor.execute('UPDATE projects ' # set new values (if any)
                           'SET title=COALESCE(%s, %s), '
                           'completed_date=COALESCE(%s, %s), '
                           'categories=COALESCE(%s, %s), '
                           'description=COALESCE(%s, %s), '
                           'image_urls=COALESCE(%s, %s), '
                           'WHERE id=%s',
                           (results['title'], data['title'],
                            results['completed_date'], data['completed_date'],
                            results['categories'], data['categories'],
                            results['description'], data['description'],
                            results['image_urls'], data['image_urls'],
                            data['id'])
                           )
            conn.commit()
            return_value = {'status': 'ok', 'msg': 'Project details successfully updated.'}
        elif request.method == 'DELETE':
            # DELETE ONE PROJECT BY PROJECT ID
            cursor.execute('DELETE * FROM projects WHERE id=%s', (data['id']))
            conn.commit()
            return_value = {'status': 'ok', 'msg': 'Project deleted successfully.'}
    except ValidationError as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': f'Invalid request: {err}'}
    except psycopg2.Error as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': 'A server error occurred while retrieving project data. Please try again later.'}
        print(f'Database error in projects_endpoint: {err}')
    except SyntaxError as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': f'Invalid syntax: {err}'}
    except Exception as err:
        status_code = 400
        return_value = {'status': 'error', 'msg': f'An unexpected error occurred: {err}'}
    finally:
        release_connection(conn)
    return jsonify(return_value), status_code