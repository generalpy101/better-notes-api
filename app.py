import os

from api.server import create_app, db
from api.auth.models import *
from dotenv import load_dotenv

load_dotenv()

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Users": Users,
    }

PORT = os.environ.get("PORT", 8080)
HOST = os.environ.get("HOST", "0.0.0.0")
DEBUG = os.environ.get("DEBUG", True)

if __name__ == "__main__":
    app.run(host=HOST,port=PORT, debug=DEBUG)
