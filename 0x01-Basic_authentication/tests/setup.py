#!/usr/bin/env python3
""" Setup data
"""
import glob
import os

# remove old persistante data
for path in glob.glob('./*.json'):
    os.remove(path)


# Load users and create 10
from models.user import User

User.load_from_file()

for i in range(10):
    u = User()
    u.email = "email{}@test.com".format(i)
    u.save()

User.save_to_file()
