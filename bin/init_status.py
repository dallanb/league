import logging

from src import Status, db


def init_status(status_enums):
    logging.info(f"init_status started")

    for status_enum in status_enums:
        status = Status(name=status_enum)
        db.session.add(status)

    db.session.commit()
    logging.info(f"init_status completed")
    return
