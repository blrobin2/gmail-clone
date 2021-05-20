from datetime import datetime
from flask import Flask, jsonify, request
from flask.helpers import url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)

CORS(app, resources={r'/*': {'origins': '*'}})


class Email(db.Model):
    __tablename__ = "emails"

    id = db.Column(db.Integer, primary_key=True)
    from_email = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(255), nullable=False, default='(No Subject)')
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    archived = db.Column(db.Boolean(), nullable=False, default=False)
    read = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, from_email, subject, body, sent_at=None):
        self.from_email = from_email
        self.subject = subject
        self.body = body
        if sent_at is not None:
            self.sent_at = sent_at

    def to_dict(self):
        return dict(
            id=self.id,
            from_email=self.from_email,
            subject=self.subject,
            body=self.body,
            sent_at=self.sent_at.isoformat() + 'Z',
            archived=self.archived,
            read=self.read,
            _links=dict(
                self=url_for('email', email_id=self.id)
            )
        )

    def from_dict(self, data):
        for field in ['archived', 'read']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def to_collection(query):
        return dict(
            items=[item.to_dict() for item in query]
        )


@app.route("/api")
def index():
    emails = Email.query.order_by(Email.sent_at.desc()).all()
    data = Email.to_collection(emails)
    return jsonify(data)


@app.route("/api/<email_id>", methods=['GET'])
def email(email_id):
    return jsonify(Email.query.get_or_404(email_id).to_dict())


@app.route("/api/<email_id>", methods=["PUT"])
def update_email(email_id):
    email = Email.query.get_or_404(email_id)
    data = request.get_json() or {}
    email.from_dict(data)
    db.session.commit()
    return jsonify(email.to_dict())
