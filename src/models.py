from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), default=True, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow)

    posts = relationship('Post', back_populates='author',
                         cascade='all, delete-orphan')
    comments = relationship(
        'Comment', back_populates='author', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='user',
                         cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "bio": self.bio,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat()
        }


class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    author = relationship('User', back_populates='posts')

    comments = relationship(
        'Comment', back_populates='post', cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='post',
                         cascade='all, delete-orphan')

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "caption": self.caption,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id
        }


class Comment(db.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id'), nullable=False)

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
            "post_id": self.post_id
        }


class Like(db.Model):
    __tablename__ = 'likes'

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id'), nullable=False)

    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')

    def serialize(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
            "post_id": self.post_id
        }
