"""
Database module for Alice and Bob.
"""
import decouple

from sqlalchemy import create_engine, Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = decouple.config("DATABASE_URL", default="postgresql+psycopg://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    origin = Column(String, index=True)
    provider = Column(String, index=True)

    published = Column(DateTime)

    # Create composed index with: title, origin and provider
    __table_args__ = (
        UniqueConstraint("title", "origin", "provider"),
    )

    def __repr__(self):
        return f"<News(title={self.title}, published={self.published})>"


# Create the table
Base.metadata.create_all(bind=engine)


def find_news(n: News) -> bool:
    ses = SessionLocal()
    return ses.query(News).filter(
        News.title == n.title,
        News.origin == n.origin,
        News.provider == n.provider
    ).count() > 0


def insert_news(n: News) -> None:
    ses = SessionLocal()
    ses.add(n)
    ses.commit()


if __name__ == '__main__':
    # Create the table
    print("Creating the table...", end="")
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error: {e}")
    print("Done!")

    # Add a new news
    print("Adding a new news...", end="")
    news = News(
        title="New News",
        origin="https://www.example.com",
        provider="AliceBob"
    )
    session = SessionLocal()

    session.add(news)
    session.commit()

__all__ = ("News", "find_news", "insert_news")
