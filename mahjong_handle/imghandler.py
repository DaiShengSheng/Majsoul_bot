import math
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont
from .utils import get_path


def get_font(size, w="85"):
    return ImageFont.truetype(
        get_path("assets", "font", f"HYWenHei {w}W.ttf"), size=size
    )


def draw_text_by_line(
    img, pos, text, font, fill, max_length, center=False, line_space=None
):
    """
    在图片上写长段文字, 自动换行
    max_length单行最大长度, 单位像素
    line_space  行间距, 单位像素, 默认是字体高度的0.3倍
    """
    x, y = pos
    _, h = font.getsize("X")
    if line_space is None:
        y_add = math.ceil(1.3 * h)
    else:
        y_add = math.ceil(h + line_space)
    draw = ImageDraw.Draw(img)
    row = ""  # 存储本行文字
    length = 0  # 记录本行长度
    for character in text:
        w, h = font.getsize(character)  # 获取当前字符的宽度
        if length + w * 2 <= max_length:
            row += character
            length += w
        else:
            row += character
            if center:
                font_size = font.getsize(row)
                x = math.ceil((img.size[0] - font_size[0]) / 2)
            draw.text((x, y), row, font=font, fill=fill)
            row = ""
            length = 0
            y += y_add
    if row != "":
        if center:
            font_size = font.getsize(row)
            x = math.ceil((img.size[0] - font_size[0]) / 2)
        draw.text((x, y), row, font=font, fill=fill)


def cut_sprites(
    img: Image.Image, parameter, box: Tuple = None, width_padding=0, sprite_call=None
) -> List:
    """
    sprites匀切分割

    img: sprite图

    parameter:参数

        - (width, height):按icon宽度和icon高度均匀切割,适用于多行多列

        - (amount, 'x/y'):沿x轴或y轴均匀切割成指定数量,适用于单行或单列

    box:指定图像区域

    scale:图像缩放
    """
    if box:
        img = img.crop(box)

    max_width, max_height = img.size
    if isinstance(parameter[1], int):
        width, height = parameter
    else:
        if parameter[1] == "x":
            width = max_width / parameter[0]
            height = max_height
        else:
            width = max_width
            height = max_height / parameter[0]
    max_num = round(max_width / width) * round(max_height / height)
    sprite_list = []
    x1 = 0
    y1 = 0
    x2 = width
    y2 = height
    for i in range(0, max_num):
        box = (x1, y1, x2, y2)
        section = img.crop(box)
        
        if sprite_call:
            section = sprite_call(section)
        
        sprite_list.append(section)
        x1 += width + width_padding
        x2 += width + width_padding
        if max_width - x1 < width:
            x1 = 0
            x2 = width
            y1 += height
            y2 += height
    return sprite_list


def easy_alpha_composite(
    im: Image, im_paste: Image, pos=(0, 0), direction="lt"
) -> Image:
    """
    透明图像快速粘贴
    """
    base = Image.new("RGBA", im.size)
    easy_paste(base, im_paste, pos, direction)
    base = Image.alpha_composite(im, base)
    return base


def easy_paste(im: Image, im_paste: Image, pos=(0, 0), direction="lt"):
    """
    inplace method
    快速粘贴, 自动获取被粘贴图像的坐标。
    pos应当是粘贴点坐标，direction指定粘贴点方位，例如lt为左上
    """
    x, y = pos
    size_x, size_y = im_paste.size
    if "d" in direction:
        y = y - size_y
    if "r" in direction:
        x = x - size_x
    if "c" in direction:
        x = x - int(0.5 * size_x)
        y = y - int(0.5 * size_y)
    im.paste(im_paste, (x, y, x + size_x, y + size_y), im_paste)
