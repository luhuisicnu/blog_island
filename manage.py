import sys
from flask.ext.script import Manager,Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app_blog_island import create_app, db
from app_blog_island.models import User, Role, User_Role_Relation, Article,\
        init_db, Follow
from config import config, jinja_environment


app = create_app(config,jinja_environment)
manager = Manager(app)
migrate = Migrate(app,db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role,
                User_Role_Relation=User_Role_Relation,
                init_db=init_db,Article=Article, Follow=Follow)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    manager.run()
