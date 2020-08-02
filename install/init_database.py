from dot_game import app, db
from dot_game.models import KeyModel, UserModel, GuideLineModel

import base64
import yaml

with open("install/key.yaml") as f:
    key_list = yaml.safe_load(f)

def addKey():
    """ add default secret key """
    new_admin_key = KeyModel(
        "admin",
        bytes(key_list['admin_key'], 'utf-8'),
        "admin key is generate by install function"
    )

    db.session.add(new_admin_key)
    db.session.commit()

    new_normal_user_key = KeyModel(
        "normal_user",
        bytes(key_list['normal_user_key'], 'utf-8'),
        "normal user key is generate by install function"
    )
    
    db.session.add(new_normal_user_key)
    db.session.commit()

def addAdmin():
    """ add default admin to users table """
    new_admin_user = UserModel(
        "admin",
        str(key_list['admin_password'])
    )
    new_admin_user.admin = True # active admin permission to user
    db.session.add(new_admin_user)
    db.session.commit()

def addGuideline():
    """ add guideline title to GuideLine table """
    guideline_list = key_list['guideline_list']
    for guideline in guideline_list:
        new_guideline = GuideLineModel(
            version = guideline['guideline']['version'],
            name = guideline['guideline']['name'],
            description = guideline['guideline']['description']
        )
        db.session.add(new_guideline)
        db.session.commit()

def install():
    """ combination of addKey, addAdmin and addGuideline """
    addKey()
    addAdmin()
    addGuideline()