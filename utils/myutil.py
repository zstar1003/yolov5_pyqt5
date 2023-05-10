# 查验导入数据是否是图片
def file_is_pic(suffix):
    if suffix == "png" or suffix == "jpg" or suffix == "bmp":
        return True
    return False


# 全局变量
class Globals:
    camera_running = False
