from src import db


def init_status(model, status_enums):
    for status_enum in status_enums:
        status = model(name=status_enum)
        db.session.add(status)

    db.session.commit()
    return
