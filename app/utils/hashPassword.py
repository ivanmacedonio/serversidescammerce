from passlib.hash import pbkdf2_sha256

def hash_password(password):
    if not password: raise ValueError("Password is required")
    hashed_password = pbkdf2_sha256.hash(str(password))
    return hashed_password

def verify_hash(password, hashed_password):
    return pbkdf2_sha256.verify(password, hashed_password)
    