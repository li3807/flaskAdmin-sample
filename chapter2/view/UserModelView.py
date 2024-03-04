from flask_admin.actions import action
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

    @action('action1', '操作1', '确认消息？')
    def action1(self, ids):
        print(f"id={ids}")
