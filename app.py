from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail


app=Flask(__name__)


if app.config['ENV'] == 'production':
    app.config.from_object('config.ProductionConfig')
else:
    app.config.from_object('config.DevelopmentConfig')



mail=Mail(app)

def allow_file_type(filename):
    type=['jpg','png','PNG']
    ex=filename[-3:]
    if not ex in type :
        return False
    return True

db=SQLAlchemy(app)
from models import User, Article
from controller import home, user, auth, admin, post

CATEGORIES=Article.Category.query.all()
app.jinja_env.globals['CATEGORIES']= CATEGORIES


moment=Moment(app)
login=LoginManager()
login.init_app(app)
login.login_view='signin'
login.login_message_category='info'



@login.user_loader
def UserLoader(userid):
    return User.User().query.get(userid)

homeController=home.Home()
authController=auth.Authentication()
userController=user.Account()
adminController=admin.Admin()
postController=post.Post()


#Home Route
app.add_url_rule('/','main',homeController.main)
app.add_url_rule('/category/<int:category_id>','viewCategory',homeController.viewCategory)
app.add_url_rule('/article/<int:article_id>','single',homeController.single)
app.add_url_rule('/search/','searchItems',homeController.searchItems)
app.add_url_rule('/article/<int:article_id>/comment','sendComment',homeController.sendComment, methods=['POST','GET'])


#Authentication Routes
app.add_url_rule('/signin','signin',authController.signin, methods=['POST','GET'])
app.add_url_rule('/signup','signup',authController.signup, methods=['POST','GET'])
app.add_url_rule('/forgetpassword','forgetPassword',authController.forgetPassword, methods=['POST','GET'])
app.add_url_rule('/resetPassword/<string:user_token>/<int:user_id>','resetPassword',authController.resetPassword, methods=['Post','GET'])
app.add_url_rule('/signout','signout',authController.signout)


#Account User Routes
app.add_url_rule('/account','account',userController.account)
app.add_url_rule('/account/info','account_info',userController.account_info)
app.add_url_rule('/account/edit','account_edit',userController.account_edit, methods=['POST','GET'])
app.add_url_rule('/account/change_password','change_password',userController.change_password, methods=['POST','GET'])
app.add_url_rule('/account/upload_avatar','upload_avatar',userController.upload_avatar, methods=['POST','GET'])


#Admin Routes
app.add_url_rule('/admin','adminAccount',adminController.adminAccount)
app.add_url_rule('/admin/user','userList',adminController.userList, methods=['POST','GET'])
app.add_url_rule('/admin/admin_info','admin_info',adminController.admin_info)
app.add_url_rule('/admin/comments','commentList',adminController.commentList, methods=['POST','GET'])
app.add_url_rule('/admin/comments/<int:comment_id>/approve','approveComment',adminController.approveComment, methods=['POST','GET'])
app.add_url_rule('/admin/admin_edit','admin_account_edit',adminController.admin_account_edit, methods=['POST','GET'])
app.add_url_rule('/admin/admin_change_password','admin_change_password',adminController.admin_change_password, methods=['POST','GET'])
app.add_url_rule('/admin/admin_upload_avatar','admin_upload_avatar',adminController.admin_upload_avatar, methods=['POST','GET'])
app.add_url_rule('/admin/user/createuser','admin_create_user',adminController.admin_create_user,methods=['POST','GET'])
app.add_url_rule('/admin/user/edit','admin_edit_user',adminController.admin_edit_user, methods=['POST','GET'])


#Post Routes
app.add_url_rule('/admin/post/create','createPost',postController.createPost,methods=['POST','GET'])
app.add_url_rule('/admin/post/postlist','postList',postController.postList,methods=['POST','GET'])
app.add_url_rule('/admin/post/editPost','editPost',postController.editPost,methods=['POST','GET'])
app.add_url_rule('/admin/category/category','categories',postController.categories, methods=['POST','GET'])
app.add_url_rule('/admin/category/editCategory','editCategory',postController.editCategory, methods=['POST','GET'])
app.add_url_rule('/admin/category/createCategory','createCategory',postController.createCategory, methods=['POST','GET'])


@app.template_filter('subContent')
def subContent(content):
    return content[0:80] + ' ...'

app.jinja_env.filters['subContent']=subContent



@app.errorhandler(404)
def notfound(error):
    return render_template('404.html'), 404


if __name__ == '__main__' :
    app.run()