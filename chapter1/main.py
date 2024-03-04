from flask import Flask
from flask_admin import Admin

app = Flask(__name__)

# 设置网站样式主题，可以在 https://bootswatch.com/3/ 查找
app.config['FLASK_ADMIN_SWATCH'] = 'Paper'

admin = Admin(app, name='microblog', template_mode='bootstrap3')
# Add administrative views here

app.run()
