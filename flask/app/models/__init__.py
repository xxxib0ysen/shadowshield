from flask import current_app
from sqlalchemy.ext.automap import automap_base


def init_models():
    """反射数据库表结构并返回模型容器"""
    Base = automap_base()
    Base.prepare(autoload_with=current_app.extensions['sqlalchemy'].engine, reflect=True)

    models = {}
    for table_name, table_class in Base.classes.items():
        models[table_name] = table_class

    return type('DatabaseModels', (object,), models)()  # 动态创建模型容器类
