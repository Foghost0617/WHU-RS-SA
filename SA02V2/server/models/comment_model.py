from server.database import SessionLocal
from server.models.tables import Comment
def add_comment(data):
    db = SessionLocal()
    try:
        new_comment = Comment(
            content=data["content"],
            added_time=data["added_time"],
            user_id=data["user_id"],
            map_id=data["map_id"]
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment.id
    except Exception as e:
        db.rollback()
        print(f"添加评论失败：{e}")
        raise
    finally:
        db.close()


def get_comments_by_map(map_id):
    db = SessionLocal()
    try:
        comments = db.query(Comment).filter(Comment.map_id == map_id).order_by(Comment.added_time.desc()).all()
        return comments
    except Exception as e:
        print(f"获取评论失败：{e}")
        raise
    finally:
        db.close()