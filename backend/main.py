from flask import Flask
from flask_cors import CORS  # Add this import
from config.config import Config
from routes.email_routes import email_bp
from routes.dashboard_routes import dashboard_bp
from mcp.mcp_retriever import initialize_vector_store
from utils.logger import get_logger

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # Enable CORS for all routes
logger = get_logger(__name__)

initialize_vector_store()

app.register_blueprint(email_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api')

if __name__ == '__main__':
    logger.info("Starting Flask application")
    print("[INFO] Starting Flask application")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)