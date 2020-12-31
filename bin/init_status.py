import logging

from src import db


def init_status(model, status_enums):
    logging.info(f"init_status started")

    for status_enum in status_enums:
        status = model(name=status_enum)
        db.session.add(status)

    db.session.commit()
    logging.info(f"init_status completed")
    return
