
from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from models import db, bcrypt, User, Note

app = Flask(__name__)

app.config["SECRET_KEY"] = "development-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return jsonify({"message": "Productivity API is running"})


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")
    password_confirmation = data.get("password_confirmation")

    if not isinstance(username, str) or not username.strip():
        return jsonify({"error": "Username is required"}), 400

    if not isinstance(password, str) or len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    if password != password_confirmation:
        return jsonify({"error": "Passwords do not match"}), 400

    username = username.strip()

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    session.clear()
    session["user_id"] = user.id

    return jsonify(user.to_dict()), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username.strip()).first()

    if user and user.check_password(password):
        session.clear()
        session["user_id"] = user.id
        return jsonify(user.to_dict()), 200

    return jsonify({"error": "Invalid username or password"}), 401


@app.route("/check_session", methods=["GET"])
def check_session():
    user_id = session.get("user_id")

    if user_id:
        user = db.session.get(User, user_id)

        if user:
            return jsonify(user.to_dict()), 200

        session.clear()

    return jsonify({}), 200


@app.route("/logout", methods=["DELETE"])
def logout():
    session.clear()
    return jsonify({}), 200


@app.route("/notes", methods=["GET"])
def get_notes():
    if "user_id" not in session:
        return jsonify({"error": "Please log in first"}), 401

    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    if page < 1 or per_page < 1:
        return jsonify({"error": "Invalid pagination values"}), 400

    per_page = min(per_page, 100)

    notes = Note.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Note.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return jsonify({
        "notes": [note.to_dict() for note in notes.items],
        "pagination": {
            "page": notes.page,
            "per_page": notes.per_page,
            "total": notes.total,
            "pages": notes.pages
        }
    }), 200


@app.route("/notes", methods=["POST"])
def create_note():
    if "user_id" not in session:
        return jsonify({"error": "Please log in first"}), 401

    data = request.get_json(silent=True) or {}

    title = data.get("title")
    content = data.get("content")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    if not isinstance(content, str) or not content.strip():
        return jsonify({"error": "Content is required"}), 400

    note = Note(
        title=title.strip(),
        content=content.strip(),
        user_id=session["user_id"]
    )

    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201


@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    if "user_id" not in session:
        return jsonify({"error": "Please log in first"}), 401

    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    return jsonify(note.to_dict()), 200


@app.route("/notes/<int:note_id>", methods=["PATCH"])
def update_note(note_id):
    if "user_id" not in session:
        return jsonify({"error": "Please log in first"}), 401

    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "Provide fields to update"}), 400

    if not set(data).issubset({"title", "content"}):
        return jsonify({"error": "Only title and content can be updated"}), 400

    for field in data:
        value = data[field]

        if not isinstance(value, str) or not value.strip():
            return jsonify({"error": field + " cannot be empty"}), 400

        setattr(note, field, value.strip())

    db.session.commit()

    return jsonify(note.to_dict()), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    if "user_id" not in session:
        return jsonify({"error": "Please log in first"}), 401

    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
