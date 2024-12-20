def to_update(db_document, body):
    for k, v in body:
        if k in db_document:
            db_document[k] = v