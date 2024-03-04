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
