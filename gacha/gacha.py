from os.path import dirname,join
from PIL import Image
from io import BytesIO
import base64
import os
import random
import json


path = dirname(__file__)
abspath = dirname(path)

def gacha_loader():
    with open(join(path,"gacha.json"), encoding='utf-8') as fp:
        data = json.load(fp)
    return data

def run_gacha(group_id):
    result = []
    pool = gacha_loader()
    group_pool = group_pool_loader()
    group_pool_list = []
    purple_gift = pool["purple_gift"]
    purple_flag = 0
    poolname = None

    #定位该群卡池
    for i in range(0,len(group_pool)):
        if group_pool[i]["gid"] == str(group_id):
            poolname = group_pool[i]["poolname"]
        else:
            group_pool_list.append(group_pool[i])
    if poolname == None:
        poolname = "up"
        binds = {
            "gid": str(group_id),
            "poolname": "up"
        }
        group_pool_list.append(binds)
        with open(join(path, 'group_pool.json'), 'w', encoding='utf-8') as fp:
            json.dump(group_pool_list, fp, indent=4)

    for i in range (0,10):
        result.append(single_pull(pool,poolname))
        if result[i][0] < 80 and (result[i][1] not in purple_gift):
            purple_flag = purple_flag + 1
    if purple_flag == 10 and result[9][0] <= 95:
        result[9][0] = 1
        result[9][1] = purple_gift[random.randint(0, len(purple_gift) - 1)]
    return concat_images(result,poolname)


def single_pull(pool,pool_name):
    up_pool = []
    for i in range (0,len(pool[pool_name])):
        up_pool.append(pool[pool_name][i] + ".png")
    normal_pool = []
    for i in range (0,len(pool["normal"])):
        normal_pool.append(pool["normal"][i] + ".png")

    gift_list = file_loader("gift")  # 读取礼物
    decoration = file_loader("decoration")  # 读取特效装扮
    person = file_loader("person")  # 读取人物
    if pool_name != "normal" and pool_name != "up" and pool_name != "kuangdu" and pool_name != "douhun":
        tmp_list = []
        for filename in os.walk(abspath + "/resources/decoration/" + pool_name + "/"):
            tmp_list.append(filename)
        decoration = decoration + tmp_list[0][2]
    if pool_name == "up":
        tmp_list = []
        for filename in os.walk(abspath + "/resources/decoration/saki2/"):
            tmp_list.append(filename)
        decoration = decoration + tmp_list[0][2]
    objint = random.randint(1,100)
    if objint < 80:
        prop = gift_list[random.randint(0, len(gift_list)-1)]
    elif objint >= 80 and objint <= 95:
        prop = decoration[random.randint(0, len(decoration)-1)]
    else:
        objint_person = random.randint(1,100)
        if objint_person <=51:
            prop = up_pool[random.randint(0, len(up_pool)-1)]
        else:
            prop = normal_pool[random.randint(0, len(normal_pool) - 1)]
    data = []
    data.append(objint)
    data.append(prop)
    return data

def file_loader(file_type):
    filelist = []
    for filename in os.walk(abspath + "/resources/" + file_type):
        filelist.append(filename)
    return filelist[0][2]

def concat_images(image,pool_name):
    if pool_name == "up":
        pool_name = "saki2"
    COL = 5  # 指定拼接图片的列数
    ROW = 2  # 指定拼接图片的行数
    UNIT_HEIGHT_SIZE = 266  # 图片高度
    UNIT_WIDTH_SIZE = 266  # 图片宽度
    image_names = []
    for tmp_image in image:
        image_names.append(tmp_image[1])
    image_files = []
    for index in range(COL * ROW):
        if image[index][0] < 80:
            imgpath = abspath + "/resources/gift/"
        elif image[index][0] > 95:
            imgpath = abspath + "/resources/person/"
        else:
            imgpath = abspath + "/resources/decoration/"
            if os.path.exists(imgpath + image_names[index]) == False:
                imgpath = abspath + "/resources/decoration/" + pool_name + "/"
        img = Image.open(imgpath + image_names[index])
        img = img.resize((256, 256), Image.ANTIALIAS)
        image_files.append(img)  # 读取所有用于拼接的图片

    target = Image.new('RGB', (UNIT_WIDTH_SIZE * COL+10, UNIT_HEIGHT_SIZE * ROW+10),(255,255,255))  # 创建成品图的画布
    for row in range(ROW):
        for col in range(COL):
            target.paste(image_files[COL * row + col], (10 + UNIT_WIDTH_SIZE * col, 10 + UNIT_HEIGHT_SIZE * row))
    return pil2b64(target)

def pil2b64(data):
    bio = BytesIO()
    data = data.convert("RGB")
    data.save(bio, format='JPEG', quality=75)
    base64_str = base64.b64encode(bio.getvalue()).decode()
    return 'base64://' + base64_str

def group_pool_loader():
    with open(join(path,'group_pool.json'),encoding='utf-8') as fp:
        data = json.load(fp)
    return data

def get_pool_id(name):
    if name == "up" or name == "当前up池": return "up"
    elif "辉夜" in name or name == "辉夜up池": return "huiye"
    elif name == "天麻up池1": return "saki1"
    elif name == "天麻up池2": return "saki2"
    elif "标配" in name or name == "标配池": return "normal"
    elif "斗牌" in name or name == "斗牌传说up池": return "douhun"
    elif "狂赌" in name or name == "狂赌up池": return "kuangdu"
    else : return None

def get_pool_name(id):
    if id == "up": return "当前up池"
    elif id == "huiye": return "辉夜up池"
    elif id == "saki1": return "天麻up池1"
    elif id == "saki2": return "天麻up池2"
    elif id == "normal": return "标配池"
    elif id == "douhun": return "斗牌传说up池"
    elif id == "kuangdu": return "狂赌up池"