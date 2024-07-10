from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # ... (rest of the Author model remains the same)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)  # Changed to Text
    summary = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('posts', lazy=True))

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        allowed_categories = ['Fiction', 'Non-Fiction', 'Poetry', 'Essay', 'News']
        if category.lower() not in [c.lower() for c in allowed_categories]:
            raise ValueError(f"Post category must be one of: {', '.join(allowed_categories)}")
        return category

    # Removed clickbait requirement from title validation

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Post title must contain clickbait phrases: " + ", ".join(clickbait_phrases))
        return title