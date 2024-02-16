from sqlalchemy.orm import Session


def saveToDatabase(db: Session, object):
    db.add(object)
    db.commit()
    db.refresh(object)


def deleteFromDatabase(db: Session, object):
    db.delete(object)
    db.commit()
