#!/usr/bin/env python3
"""filtered_logger module that implements data obfuscation"""
from typing import List
import re
import logging
import os
import mysql.connector


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns an obfuscated log message
    Args:
        fields: list of strings indicating fields to obfuscate
        redaction: what the field will be obfuscated to
        message: the log line to obfuscate
        separator: the character separating the fields
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator, field+'='+redaction+separator,
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        """initilizes an instance of RedactingFormatter class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redact the message of LogRecord instance
        Args:
            record: LogRecord instance containing message
        Return:
            formatted string
        """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    function that returns a connector to the database
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME')
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    conn = mysql.connector.connect(user=user, password=passwd, host=host,
                                   database=db_name)
    return conn


def main() -> None:
    """
    Obtains a database connection and retrieves all rows in the users table
    and displays each row under a filtered format
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    fields = cursor.column_names
    for row in cursor:
        message = "".join(f'{k}={v}; ' for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
