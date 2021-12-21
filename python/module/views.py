from flask import Blueprint, jsonify

bp = Blueprint('module', __name__, url_prefix='/api')


@bp.route('/hello')
def hello():
    return {'hello': 'world'}


@bp.route('/ipecho')
def ipecho():
    return jsonify('192.168.1.1')
