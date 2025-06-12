from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
         user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        return jsonify({"message": "Logado com sucesso"})
    return jsonify({"message": "Credenciais inválidas"}), 400 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria todas as tabelas definidas nos modelos
    app.run(debug=True)
