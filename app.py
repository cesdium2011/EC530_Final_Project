import os
import logging
import queue
from flask import Flask, request, redirect, flash, url_for, render_template, jsonify, abort
from flask_dance.contrib.google import make_google_blueprint, google
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from feed_ingester import feed_ingester
from doc_feed_analyzer import analyze_document, analyze_feed
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from functools import wraps
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from celery import Celery
from flask_restful import Api, Resource
from flasgger import Swagger



# Configure app, logging, databases and queue
app = Flask(__name__)
api = Api(app)

#API setup
swagger = Swagger(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

logging.basicConfig(filename='app.log', level=logging.INFO)
upload_queue = queue.Queue()

# Google authentication
blueprint = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_url='/',
)
app.register_blueprint(blueprint, url_prefix="/login")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    
    return User.query.get(int(user_id))

@app.route('/protected_route')
@login_required
def protected_route():
    return "This is a protected route. You must be logged in to access it."

# Authentication decorator
def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not google.authorized:
            return redirect(url_for("google.login"))
        return func(*args, **kwargs)
    return decorated_view

#API preset

class UploadAPI(Resource):
    def post(self):
        """
        Upload a file
        ---
        tags:
          - File Management
        parameters:
          - in: formData
            name: file
            type: file
            required: true
            description: The file to upload
        responses:
          200:
            description: File uploaded and read successfully
        """
        #file upload logic
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join("uploaded_files", filename))
            return {"message": "File uploaded and saved.", "filename": filename}, 200
        else:
            return {"error": "No file provided."}, 400


class IngestFeedAPI(Resource):
    def post(self):
        """
        Ingest a feed
        ---
        tags:
          - Feed Management
        parameters:
          - in: formData
            name: feed_url
            type: string
            required: true
            description: The URL of the feed to ingest
        responses:
          200:
            description: Feed ingestion initiated. Processing in the background.
        """
        #feed ingestion logic
        feed_url = request.form.get('feed_url')
        if feed_url:
            task = process_feed.delay(feed_url)
            return {"message": "Feed ingestion initiated. Processing in the background.", "task_id": str(task.id)}, 200
        else:
            return {"error": "No feed URL provided."}, 400

api.add_resource(UploadAPI, '/api/upload')
api.add_resource(IngestFeedAPI, '/api/ingest_feed')

#Celery instance for API 
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

@celery.task()
def process_feed(feed_url):
    feed = feedparser.parse(feed_url)
    # Process the feed data as needed
    # Save the processed data to a database, file, or any other storage
    return {"message": f"Feed '{feed_url}' processed."}

# Routes
@app.route('/')
@login_required
def index():
    analysis_results = {}  # Initialize an empty analysis results dictionary

    # Get the analysis results if available in session data
    if 'analysis_results' in session:
        analysis_results = session['analysis_results']

    return render_template('index.html', analysis_results=analysis_results)

@app.route('/upload_file', methods=['POST'])
@login_required
def upload_file():
    # ... file upload logic here ...
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        logging.info(f"File uploaded: {filename}")
    else:
        flash('File type not allowed')
        return redirect(request.url)

@app.route('/ingest_feed', methods=['POST'])
@login_required
def ingest_feed():
    url = request.form['url']
    try:
        feed_items = feed_ingester(url)
        # ... process feed_items ...
    except Exception as e:
        flash(f"Error ingesting feed: {str(e)}")
        return redirect(request.url)

@app.route('/analyze')
@login_required
def analyze():
    document_analysis = analyze_document('path/to/document.pdf')
    feed_analysis = analyze_feed('path/to/feed.xml')
    return jsonify({'document_analysis': document_analysis, 'feed_analysis': feed_analysis})

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email address already exists.")
            return redirect(url_for("register"))

        new_user = User(username=username, email=email, password=generate_password_hash(password, method="sha256"))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return redirect(url_for("login"))

        login_user(user, remember=remember)
        return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


#error handling
@app.errorhandler(400)
def bad_request(error):
    response = jsonify({"error": "Bad Request", "message": str(error)})
    response.status_code = 400
    return response

@app.errorhandler(403)
def forbidden(error):
    response = jsonify({"error": "Forbidden", "message": str(error)})
    response.status_code = 403
    return response

@app.errorhandler(404)
def not_found(error):
    response = jsonify({"error": "Not Found", "message": str(error)})
    response.status_code = 404
    return response




if __name__ == "__main__":
    app.run(debug=True)
