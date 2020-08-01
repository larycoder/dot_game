from dot_game import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from install.init_database import addKey, addAdmin, addGuideline

migrate = Migrate(app, db)
manager = Manager(app)

# migration
manager.add_command('db', MigrateCommand)

@manager.command
def run_app():
    """ run server """
    app.run()

@manager.command
def install_key():
    """ install default key to database """
    addKey()

@manager.command
def init_admin():
    """ create user admin with default password """
    addAdmin()

@manager.command
def add_guideline():
    """ add default guideline to GuideLine table """
    addGuideline()

@manager.command
def install():
    """ combine of install_key, add_guideline and init_admin """
    addKey()
    addAdmin()
    addGuideline()

@manager.command
def drop_db():
    db.drop_all()

if __name__ == '__main__':
    manager.run()