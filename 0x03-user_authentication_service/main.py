#!/usr/bin/env python3
"""
End-to-end integration test for the flask app
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Test for register a user with the given email and password.
    Args:
        email: The email of the user.
        password: The password of the user.
    Returns:
        None
    """
    resp = requests.post('http://127.0.0.1:5000/users',
                         data={'email': email, 'password': password})
    if resp.status_code == 200:
        assert(resp.json() == {"email": email, "message": "user created"})
    else:
        assert(resp.status_code == 400)
        assert(resp.json() == {"message": "email already registered"})


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test for log in with the given wrong credentials.
    Args:
        email: The email of the user.
        password: The password of the user.
    Returns:
        None
    """
    resp = requests.post('http://127.0.0.1:5000/sessions',
                         data={'email': email, 'password': password})
    assert(resp.status_code == 401)


def log_in(email: str, password: str) -> str:
    """
    Test for log in with the given correct email and password.
    Args:
        email: The email of the user.
        password: The password of the user.
    Returns:
        The session_id of the user.
    """
    resp = requests.post('http://127.0.0.1:5000/sessions',
                         data={'email': email, 'password': password})
    assert(resp.status_code == 200)
    assert(resp.json() == {"email": email, "message": "logged in"})
    return resp.cookies.get('session_id')


def profile_unlogged() -> None:
    """
    Test for profile without being logged in with session_id.
    Returns:
        None
    """
    resp = requests.get('http://127.0.0.1:5000/profile')
    assert(resp.status_code == 403)


def profile_logged(session_id: str) -> None:
    """
     Test for profile with being logged in with session_id.
    Args:
        session_id: The session_id of the user.
    Returns:
        None
    """
    resp = requests.get('http://127.0.0.1:5000/profile',
                        cookies={'session_id': session_id})
    assert(resp.status_code == 200)


def log_out(session_id: str) -> None:
    """
    Test for log out with the given session_id.
    Args:
        session_id: The session_id of the user.
    Returns:
        None
    """
    resp = requests.delete('http://127.0.0.1:5000/sessions',
                           cookies={'session_id': session_id})
    if resp.status_code == 302:
        assert(resp.url == 'http://127.0.0.1:5000/')
    else:
        assert(resp.status_code == 200)


def reset_password_token(email: str) -> str:
    """
    Test for reset password token with the given email.
    Args:
        email: The email of the user.
    Returns:
        The reset_token of the user.
    """
    resp = requests.post('http://127.0.0.1:5000/reset_password',
                         data={'email': email})
    if resp.status_code == 200:
        return resp.json().get('reset_token')
    assert(resp.status_code == 401)


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test for update password with the given email,
    reset_token and new_password.
    Args:
        email: The email of the user.
        reset_token: The reset_token of the user.
        new_password: The new password of the user.
    Returns:
        None
    """
    resp = requests.put('http://127.0.0.1:5000/reset_password',
                        data={'email': email,
                              'reset_token': reset_token,
                              'new_password': new_password})
    if resp.status_code == 200:
        assert(resp.json() == {"email": email, "message": "Password updated"})
    else:
        assert(resp.status_code == 403)


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)