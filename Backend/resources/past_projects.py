import psycopg2
from flask import Blueprint, jsonify, request

from db.db_pool import get_cursor, release_connection

past_projects = Blueprint('past_projects', __name__)

@past_projects.route('/projects')
def find_all_projects():
    conn = None
    try:
        conn, cursor = get_cursor()
        cursor.execute('SELECT * FROM past_projects')
        results = cursor.fetchall()
        return jsonify(status='ok', msg='Projects successfully retrieved.'), 200
    except psycopg2.Error as err:
        print(f'Database error: {err}')
        return jsonify(status='error', msg='A server error occurred while retrieving project data. Please try again later.'), 400
    except SyntaxError as err:
        print(f'Syntax error: {err}')
        return jsonify(status='error', msg='It seems like there is a syntax error.'), 400
    except Exception as err:
        print (f'Some error: {err}')
        return jsonify(status='error', msg='An error has occurred retrieving projects.'), 400
    finally:
        release_connection(conn)

@past_projects.route('/projects', methods=['PUT'])
def add_one_project():
    data = request.get_json()
    conn = None
    try:
        conn, cursor = get_cursor()
        cursor.execute('INSERT INTO past_projects (date, title, tag, description, image_url) VALUES (%s, %s, %s, %s, %s)', (data['date'], data['title'], data['tag'], data['description'], data['image_url']))
        conn.commit()
    finally:
        release_connection(conn)