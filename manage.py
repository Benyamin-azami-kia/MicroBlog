from app import app, db
from flask_script import Manager
from models import User

manager=Manager(app)

@manager.command
def init():
    db.create_all()
    return 'Done!'


@manager.command
def create_admin():
    firstname, lastname=input("Please Enter First Name And LastName: ").split()
    email=input('Plaese Enter Email: ')
    password=input('Please Enter Password: ')
    admin=User.User.query.filter_by(email=email).first()
    if admin:
        print('User/Admin Is Already Exist by That Email!')
        return False
    else:
        admin=User.User(firstname=firstname, lastname=lastname, email=email, passwd=password, admin=1)
        db.session.add(admin)
        db.session.commit()
        return 'New Admin Added!'

if __name__ == '__main__' :
    manager.run()
