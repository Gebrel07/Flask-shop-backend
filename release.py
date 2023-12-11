# actions to be executed by heroku on release

from flask_migrate import upgrade

from src.app import create_app
from src.extensions import db
from src.main.usuario.usr import UserHandler, Usuario


def add_test_user():
    Usuario.query.filter_by(email="teste@teste.com").delete()
    db.session.commit()

    user_handler = UserHandler()
    user_handler.criar_usuario(
        nome="Usuário Teste", email="teste@teste.com", senha="teste123"
    )


if __name__ == "__main__":
    with create_app().app_context():
        print(f"{'='*10}Running release script{'='*10}")

        print(f"{'-'*10}Running db Migrations{'-'*10}")
        upgrade()

        print(f"{'-'*10}Adding test user{'-'*10}")
        add_test_user()

        print(f"{'='*10}Release Done!{'='*10}")
