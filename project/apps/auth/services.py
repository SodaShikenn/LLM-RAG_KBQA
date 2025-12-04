def validate_user(email, password):
    # Using hard-coded user data for validation. In production, use database to maintain email and password
    valid_users = {
        'admin@qq.com': '123456'
    }
    if email in valid_users and password == valid_users[email]:
        return True
    return False