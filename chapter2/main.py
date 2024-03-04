from flask import Flask
from flask_admin import Admin

from chapter2.model.UserModel import UserModel
from chapter2.view.UserModelView import UserModelView

app = Flask(__name__)
# 设置网站样式主题，可以在 https://bootswatch.com/3/ 查找
app.config['FLASK_ADMIN_SWATCH'] = 'Paper'
app.config['SECRET_KEY'] = 's21sdf32sdf321dsf'

admin = Admin(app, name='microblog', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(UserModelView(name="用户", endpoint="user", model=UserModel))

try:
    UserModel.create_table()
except:
    pass

app.run()
