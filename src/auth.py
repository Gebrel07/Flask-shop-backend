from flask_jwt_extended import JWTManager

from src.main.usuario import Usuario

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user: Usuario):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # sub: onde fica a identificação do usuario no token
    identity = jwt_data["sub"]
    return Usuario.query.get(identity)
