from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from src.database import db
from src.models.user import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'message': 'Credenciais inválidas'}), 400

    user = User.query.filter(or_(User.username == username, User.email == username)).first()
    if user and user.check_password(password):
        return jsonify({'success': True, 'data': user.to_dict()})
    return jsonify({'success': False, 'message': 'Usuário ou senha incorretos'}), 401

@user_bp.route('/users', methods=['GET'])
def listar_usuarios():
    usuarios = User.query.all()
    return jsonify({'success': True, 'data': [u.to_dict() for u in usuarios]})

@user_bp.route('/users', methods=['POST'])
def criar_usuario():
    data = request.get_json() or {}
    if not all(k in data for k in ('username', 'email', 'password')):
        return jsonify({'success': False, 'message': 'Dados incompletos'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'message': 'Usuário já existe'}), 400

    usuario = User(
        username=data['username'],
        email=data['email'],
        nome_completo=data.get('nome_completo', ''),
        perfil=data.get('perfil', 'tecnico')
    )
    usuario.set_password(data['password'])
    db.session.add(usuario)
    db.session.commit()
    return jsonify({'success': True, 'data': usuario.to_dict()}), 201
