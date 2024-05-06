
VERSION = "3"
IS_CROP_MODEL = r'checkpoints/is_crop.pth'
IS_GRAPH_TEXT = r'checkpoints/is_grape_text.pth'
GRAPH_CONTENT = r'checkpoints/shape_cls.pth'
TEXT_CONTENT = r'checkpoints/is_single_multi.pth'
GRAY2K = r'configurations/gray2k.json'
HRANK = r'configurations/h_range.json'



NO_PROCESS = r'configurations/logo_no_process.json'
# SR_MODEL = r"checkpoints/0925-x4_rep_epoch151_x4.pth"
# THICK_THIN_MODEL =r"checkpoints/resnet18-thick-thin.pt"
# SHAPE_MODEL = r'checkpoints/resnet18-shape.pt'
DATA_PACKAGE_MAP = r'configurations/data_package_map.json'
 
IMGURL = 'https://fusenapi.kayue.cn:8010/storage'

DEFAULTQRCODE = "https://www.fusenpack.com/"
DEFAULTWEBSITE = "Your Website Here"
DEFAULTADDRESS = "Your Address Here"
DEFAULTSLOGAN = "Your Slogan Here"
DEFAULTPHONE = "Your Phone Number Here"
OLDVERSION_TEMPLATES = ["A1","A2","A3","B1","B4","B8","B9","B11","B12","B13","B14","B15","B16","B17","B18","C1","C2","C3","C4","C5","C6","C7","C10","C11"]
DARK_LIGHT_K_VALUE = 20


REDIS_IP = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_PASSWORD = ""  # 没有设置。
BIND = "0.0.0.0:8999"
WORKERS = 4
THREADS = 2
PIDFILE = "log/gunicorn.pid"
ACCESSLOG = "log/access.log"
ERRORLOG = "log/gunicorn.log"
TIMEOUT = 24000