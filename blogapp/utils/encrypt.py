import hashlib
# 导入django中setting.py文件自带加密的盐：SECRET_KEY
from blogsite.settings import SECRET_KEY

def md5(data_string):
    """md5加密"""
    obj = hashlib.md5(SECRET_KEY.encode("utf-8"))
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()