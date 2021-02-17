import os
from flask import Flask, Blueprint
from api_routes.search import search_blueprint
from api_routes.auth import auth_blueprint
from api_config import api_credentials_db

api = Flask(__name__)
api.register_blueprint(search_blueprint)
api.register_blueprint(auth_blueprint)



if os.environ.get("FLASK_ENV") == "development":
    if __name__ == '__main__':
        api.run(debug=True)
else:
    if __name__ == '__main__':
        # Bind to PORT if defined, otherwise default to 5000.
        port = int(os.environ.get('PORT', 9000))
        api.run(host='0.0.0.0', port=port)

