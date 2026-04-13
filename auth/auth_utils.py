import bcrypt

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    # bcrypt.hashpw returns a byte string, we decode it to store as a string
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a password against a provided hash."""
    pwd_bytes = password.encode('utf-8')
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)
