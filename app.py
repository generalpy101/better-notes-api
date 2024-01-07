from api.server import create_app, db
from api.auth.models import *
from flask import Flask

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Users": Users,
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080, debug=True)
