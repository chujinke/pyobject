# encoding=utf-8
import os

#配置模板，静态文件等信息
file_setting={
    "template_path":os.path.join(os.path.dirname(__file__), "../templates"),
    "static_path" : os.path.join(os.path.dirname(__file__), "../statics"),
}
