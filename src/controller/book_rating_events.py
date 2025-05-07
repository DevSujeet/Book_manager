"""
To update the book summary with rating and summary when the user update/insert a a book review.
"""

# src/events/book_rating_events.py
from sqlalchemy import event, func
from sqlalchemy.orm import Session
from src.models.user_book_review import UserBookReview
from src.models.book_summary import BookSummary
from src.config.log_config import logger


def update_book_summary_rating(mapper, connection, target: UserBookReview):
    """Recalculate and update book_summary.book_rating on rating insert or update."""
    session = Session(bind=connection)
    try:
        avg_rating = session.query(func.avg(UserBookReview.rating))\
                            .filter(UserBookReview.book_id == target.book_id)\
                            .scalar()

        summary = session.query(BookSummary).filter(
            BookSummary.book_id == target.book_id).first()
        logger.info(f"Book summary: {summary}")
        if summary:
            summary.book_rating = round(avg_rating, 2)
            session.commit()
    except Exception as e:
        print(f"Error updating book_summary.book_rating: {e}")
        session.rollback()
    finally:
        session.close()

# Attach events
event.listen(UserBookReview, "after_insert", update_book_summary_rating)
event.listen(UserBookReview, "after_update", update_book_summary_rating)
event.listen(UserBookReview, "after_delete", update_book_summary_rating)