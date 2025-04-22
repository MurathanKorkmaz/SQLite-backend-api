from flask import Flask, jsonify, request, Response
from models import db, User
import json
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pegasoft.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'pegasoft_sifreli_anahtar'

db.init_app(app)
jwt = JWTManager(app)

# Veritabanını oluştur
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    data = {"message": "Pegasoft Backend API çalışıyor!"}
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

# Kullanıcı ekleme (POST)
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return Response(json.dumps({"error": "İsim, e-posta ve şifre alanları zorunludur!"}, ensure_ascii=False), mimetype='application/json'), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return Response(json.dumps({"error": "Bu e-posta zaten kayıtlı!"}, ensure_ascii=False), mimetype='application/json'), 400

    new_user = User(name=data['name'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return Response(json.dumps({"message": f"Kullanıcı {new_user.name} eklendi!"}, ensure_ascii=False), mimetype='application/json')

# Kullanıcı girişi (Login)
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return Response(json.dumps({"error": "Geçersiz e-posta veya şifre!"}, ensure_ascii=False), mimetype='application/json'), 401

    access_token = create_access_token(identity=str(user.id))  # <-- Buraya dikkat!
    return Response(json.dumps({"message": "Giriş başarılı!", "token": access_token}, ensure_ascii=False), mimetype='application/json')

# Kullanıcıları listeleme (GET) — Artık Token Gerekli
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
    return Response(json.dumps(user_list, ensure_ascii=False), mimetype='application/json')

# Kullanıcı silme (DELETE)
@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return Response(json.dumps({"message": f"Kullanıcı {user.name} silindi!"}, ensure_ascii=False), mimetype='application/json')
    else:
        return Response(json.dumps({"error": "Kullanıcı bulunamadı!"}, ensure_ascii=False), mimetype='application/json'), 404

if __name__ == '__main__':
    app.run(debug=True)
