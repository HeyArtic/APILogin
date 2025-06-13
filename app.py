from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def  load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
         user = User.query.filter_by(username=username).first()

         if user and user.password == password:
             login_user(user)
             return jsonify({"message": "Logado com sucesso"})
         
    return jsonify({"message": "Credenciais inválidas"}), 400 

@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Deslogado com sucesso."})

@app.route('/user', methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Registrado com sucesso"})
    return jsonify({"message": "Credenciais inválidas"}), 400 

@app.route('/user/<int:id_user>', methods=["GET"])
@login_required
def read_user(id_user):
    user = User.query.get(id_user)
    if user:
        return {"username": user.username}
    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/user/<int:id_user>', methods=["PUT"])
@login_required
def upgrade_user(id_user):
    data = request.get_json()
    user = User.query.get(id_user)

    if user.id != current_user.id and current_user.role != 'admin':
        return jsonify({"message": "Você não tem permissão para fazer isso"}), 403
        
    if user and data.get("password"):
        user.password = data.get("password")
        db.session.commit()
        return jsonify({"message": f"Usuário {id_user} teve a senha alterada com sucesso."})
    return jsonify({"message": "Usuário não encontrado"}), 400

@app.route('/delete/<int:id_user>', methods=["DELETE"])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)

    if current_user.id == id_user:
        return jsonify({"message": "Você não tem permissão para fazer isso"})
    
    if current_user.role != 'admin':
        return jsonify({"message": "Você não tem permissão para fazer isso"})
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuário deletado com sucesso"})
    
    return jsonify({"message": "Erro ao deletar"}), 404


if __name__ == '__main__':
    app.run(debug=True)