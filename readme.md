# 章节1 开始入门

## Flask 应用初始化

```python
from flask import Flask
from flask_admin import Admin

app = Flask(__name__)

# 设置网站样式主题，可以在 https://bootswatch.com/3/ 查找
app.config['FLASK_ADMIN_SWATCH'] = 'Paper'

# 初始化Flask Admin 应用，name 表示网站的名称，会在导航前端显示，template_mode 表示模板模式
# name 和 template_mode 参数都是可选的
admin = Admin(app, name='microblog', template_mode='bootstrap3')
# Add administrative views here

app.run()
```

如果启动此应用程序并导航到 http://localhost:5000/admin/ ，您应该看到一个顶部有导航栏的空页面。通过指定适合您需要的
Bootswatch 主题来自定义外观(请参阅 http://bootswatch.com/3/ 获取可用的样本)。

## 添加模型视图

模型视图允许您添加一组专用的管理页面，用于管理数据库中的任何模型。为此，可以创建 ModelView 类的实例。

### 基于 Peewee 模型

Main 代码

```python
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

admin = Admin(app, name='microblog', template_mode='bootstrap3')

admin.add_view(UserModelView(UserModel))

app.run()
```

BaseModel 代码

```python 
import peewee

db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db

```

UserModel 代码

```python
from datetime import datetime

import peewee

from chapter2.model.BaseModel import BaseModel


class UserModel(BaseModel):
    username = peewee.CharField(max_length=80)
    email = peewee.CharField(max_length=120)
    remark = peewee.CharField(max_length=256, null=True)
    createTime = peewee.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username

```

UserModelView 代码

```python
from flask_admin.contrib.peewee import ModelView

from chapter2.view.ModelViewUtil import ModelViewUtil


class UserModelView(ModelView):
    # 功能开启
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    can_set_page_size = True
    # 模板配置
    # list_template = ''
    # edit_template = ''
    # create_template =
    # 查询列表、排序、分页、导出相关
    column_list = ('username', 'email', 'remark', 'createTime')
    column_export_list = ('username', 'email', 'remark', 'createTime')
    export_types = ModelViewUtil.export_types()
    column_labels = dict(username="姓名", email="电子邮箱")
    column_descriptions = dict(username="姓名描述")
    column_formatters = dict(
        username=lambda v, c, m, p: "[" + m.username + "]")
    column_type_formatters = ModelViewUtil.default_type_formatters()
    column_display_pk = False
    column_sortable_list = ('username', 'email')
    column_searchable_list = ('username', 'email')
    column_default_sort = 'username'
    page_size = 2

```

#### 依赖包

```text
Flask
Flask-Admin
peewee
wtf-peewee
tablib[xlsx]
```

#### 视图功能开启

- can_create：开启模型创建，默认 True
- can_edit：开启模型编辑，默认 True
- can_delete：开启模型删除，默认 True
- can_view_details：开启模型详细视图，默认 False
- can_export：开启导出，默认值 False
- can_set_page_size，开启选择 PageSize（只有20、50、100的页记录数选择），默认值 False

#### 列表视图

- column_list:查询列表显示的列，如果不设置默认是模型的所有数据项
- column_labels:列表列的标签显示，dict 类型，key 是模型的数据项名称，value 是标签

```python
# username 是模型的数据项
column_labels = dict(username="姓名", email="电子邮箱")
```

- column_descriptions:列表列的描述信息，dict 类型，key 是模板的数据项名称，value 是描述

```python
# username 是模型的数据项
column_descriptions = dict(username="姓名描述")
```

- column_formatters:设置列数据的格式化，dict 类型，支持 lambda 表达式

```python
# 该代码在显示姓名时，增了中括号
column_formatters = dict(
    username=lambda v, c, m, p: "[" + m.username + "]")
```

- column_type_formatters:设置列类型的默认显示格式，例如 NULL 显示为空字符串等

```python
from datetime import date

from flask_admin.model import typefmt


class ModelViewUtil:
    USER_DEFINED_DEFAULT_FORMATTERS = None

    @staticmethod
    def default_type_formatters():
        if ModelViewUtil.USER_DEFINED_DEFAULT_FORMATTERS is None:
            ModelViewUtil.USER_DEFINED_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
            ModelViewUtil.USER_DEFINED_DEFAULT_FORMATTERS.update({
                type(None): typefmt.empty_formatter,
                date: ModelViewUtil.date_format
            })

        return ModelViewUtil.USER_DEFINED_DEFAULT_FORMATTERS

    @staticmethod
    def date_format(cls, value):
        return value.strftime('%Y年%m月%d日 %H:%M:%S')

    @staticmethod
    def export_types():
        return ['csv', 'xlsx']
```

```python
from flask_admin.contrib.peewee import ModelView

from chapter2.view.ModelViewUtil import ModelViewUtil


class UserModelView(ModelView):
    column_type_formatters = ModelViewUtil.default_type_formatters()
```

- column_display_pk:列表显示主键，默认 True
- column_sortable_list:列表排序字段
- column_default_soft:列表默认排序字段
- column_searchable_list:列表搜索列，配置后会开启搜索输入，可以配置多个列
- column_export_list:列表导出数据列
- export_types:列表导出格式，默认支持 csv 格式，如果需要支持 XLSX 格式，需要安装依赖包 tablib[xlsx]，示例：['csv','xlsx']
- page_size:默认每页记录数量，默认值 10

#### 自定义列表行操作

在视图中，使用装饰器 @action 来自定义的列表行操作，需要参数 name, text, confirmation，name 表示操作的名称，text
是在显示在菜单的文字，confirmation 表示如果操作需要确认提示的文字。被装饰器的函数需要有2个参数，self和 ids，ids
表示选择操作的行的主键，数组类型

```python
from flask_admin.actions import action
from flask_admin.contrib.peewee import ModelView


class UserModelView(ModelView):

    @action('action1', '操作1', '确认消息？')
    def action1(self, ids):
        pass

```

#### 菜单导航

菜单导航依据 add_view 方法的视图参数来配置，示例代码

```python
from flask import Flask
from flask_admin import Admin

app = Flask(__name__)
# 设置网站样式主题，可以在 https://bootswatch.com/3/ 查找
app.config['FLASK_ADMIN_SWATCH'] = 'Paper'
app.config['SECRET_KEY'] = 's21sdf32sdf321dsf'

admin = Admin(app, name='microblog', template_mode='bootstrap3')

admin.add_view(UserModelView(name="用户", endpoint="user", category="菜单分类", model=UserModel))
```

参数说明如下：

- name：表示菜单项
- model：表示模型对象
- endpoint：表示 Url 端点
- category：表示菜单分类，如果为空表示没有下级菜单。