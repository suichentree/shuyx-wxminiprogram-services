# scripts/code_generator.py
from jinja2 import Environment, FileSystemLoader
import os
from modules.module_exam.model import mp_user_model, mp_exam_model

def generate_crud_files(models_dir, output_dir):
    # 初始化Jinja2环境
    env = Environment(loader=FileSystemLoader('templates'))

    # 获取所有模型
    models = [mp_user_model.MpUserModel, mp_exam_model.MpExamModel]

    for model in models:
        model_name = model.__name__
        table_name = model.__tablename__

        # 生成DAO层
        dao_template = env.get_template('dao_template.py')
        dao_content = dao_template.render(model_name=model_name, table_name=table_name)

        # 生成Service层
        service_template = env.get_template('service_template.py')
        service_content = service_template.render(model_name=model_name, table_name=table_name)

        # 生成Controller层
        controller_template = env.get_template('controller_template.py')
        controller_content = controller_template.render(model_name=model_name, table_name=table_name)

        # 写入文件
        os.makedirs(f'{output_dir}/dao', exist_ok=True)
        os.makedirs(f'{output_dir}/service', exist_ok=True)
        os.makedirs(f'{output_dir}/controller', exist_ok=True)

        with open(f'{output_dir}/dao/{model_name.lower()}_dao.py', 'w') as f:
            f.write(dao_content)

        with open(f'{output_dir}/service/{model_name.lower()}_service.py', 'w') as f:
            f.write(service_content)

        with open(f'{output_dir}/controller/{model_name.lower()}_controller.py', 'w') as f:
            f.write(controller_content)


# 使用示例
generate_crud_files('./modules/module_exam/model', './modules/module_exam')