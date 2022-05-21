import os
import base64
from .utils import *
from .dfs import *
from PIL import ImageFont,ImageDraw,Image
from io import BytesIO

FILE_PATH = os.path.dirname(os.path.dirname(__file__))

class ImgText:
    FONTS_PATH = os.path.join(FILE_PATH,'fonts')
    FONTS = os.path.join(FONTS_PATH,'msyh1.otf')
    font = ImageFont.truetype(FONTS, 14)
    def __init__(self, text):
        # 预设宽度 可以修改成你需要的图片宽度
        self.width = 600
        # 文本
        self.text = text
        # 段落 , 行数, 行高
        self.duanluo, self.note_height, self.line_height, self.drow_height = self.split_text()
    def get_duanluo(self, text):
        txt = Image.new('RGBA', (400, 800), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        # 所有文字的段落
        duanluo = ""
        # 宽度总和
        sum_width = 0
        # 几行
        line_count = 1
        # 行高
        line_height = 0
        for char in text:
            width, height = draw.textsize(char, ImgText.font)
            sum_width += width
            if sum_width > self.width: # 超过预设宽度就修改段落 以及当前行数
                line_count += 1
                sum_width = 0
                duanluo += '\n'
            duanluo += char
            line_height = max(height, line_height)
        if not duanluo.endswith('\n'):
            duanluo += '\n'
        return duanluo, line_height, line_count
    def split_text(self):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        allText = []
        for text in self.text.split('\n'):
            duanluo, line_height, line_count = self.get_duanluo(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        drow_height = total_lines * line_height
        return allText, total_height, line_height, drow_height
    def draw_text(self):
        """
        绘图以及文字
        :return:
        """
        im = Image.new("RGB", (600, self.drow_height), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        # 左上角开始
        x, y = 0, 0
        for duanluo, line_count in self.duanluo:
            draw.text((x, y), duanluo, fill=(0, 0, 0), font=ImgText.font)
            y += self.line_height * line_count
        bio  = BytesIO()
        im.save(bio, format='PNG')
        base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()
        mes  = f"[CQ:image,file={base64_str}]"
        return mes

def calc_shanten_13(hc=None, hc_list=None):
    if hc_list:
        hc = hc_list
    else:
        hc = convert_hc_to_list(hc)
    if sum(hc) != 13:
        raise ValueError("请传入13位手牌.")
    m = get_mianzi(hc)
    # 没有面子拆解的情况 传入空数组
    if not m:
        m = [[]]
    # 最大8向听
    xt_list = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    ]
    for x in m:
        # 面子数量
        mianzi_count = len(x)
        thc = get_trimed_hc(hc.copy(), x)
        dazi_list = get_dazi(thc)
        da_list_xt_min = 999
        for dazi in dazi_list:
            # 是否有雀头
            if_quetou = 0
            for y in dazi:
                if y[1] > 0:
                    if_quetou = 1
            dazi_count = len(dazi)
            xt = calc_xiangting(mianzi_count, dazi_count, if_quetou)
            if xt <= da_list_xt_min:
                tthc = get_trimed_dazi(thc.copy(), dazi)
                # 孤张
                guzhang_list = get_guzhang(tthc)
                # 进张
                tenpai = get_tenpai_from_dazi(dazi, xt)

                # TODO 或许有更多情况
                # 向听为0
                if xt == 0:
                    # 无搭子 即单吊
                    if not dazi:
                        tenpai += guzhang_list
                # 向听数为1
                if xt == 1:
                    if dazi_count == 1:
                        if if_quetou:
                            ga = get_guzhang_around(guzhang_list)
                            tenpai += ga
                            tenpai += guzhang_list
                        else:
                            tenpai += guzhang_list
                    if dazi_count == 2:
                        # 搭子自身可以减少向听
                        for d in dazi:
                            i = d[0]
                            if d[1] > 0:
                                tenpai.append(i)
                            elif d[2] > 0:
                                tenpai.append(i)
                                tenpai.append(i + 1)
                            elif d[3] > 0:
                                tenpai.append(i)
                                tenpai.append(i + 2)
                # 向听为2以上
                if xt >= 2:
                    if mianzi_count + dazi_count < 5:
                        # 4搭子0雀头, 不需要新的搭子(顺子型)
                        if mianzi_count + dazi_count == 4 and not if_quetou:
                            less_than5 = get_md_less_than5(tthc,0)
                            tenpai += less_than5
                        else:
                            less_than5 = get_md_less_than5(tthc)
                            tenpai += less_than5
                        #pass
                    elif mianzi_count + dazi_count >=5:
                        # 超载时 搭子自身可以化为雀头 孤张也可
                        if not if_quetou:
                            for d in dazi:
                                i = d[0]
                                if d[1] > 0:
                                    tenpai.append(i)
                                elif d[2] > 0:
                                    tenpai.append(i)
                                    tenpai.append(i + 1)
                                elif d[3] > 0:
                                    tenpai.append(i)
                                    tenpai.append(i + 2)
                            tenpai += guzhang_list
                tenpai = list(set(tenpai))
                tenpai.sort()
                xt_list[xt] += tenpai
    for y in range(len(xt_list)):
        if xt_list[y]:
            # (向听数, 进张列表)
            return (y, list(set(xt_list[y])))


# 一般形牌理分析
def calc_shanten_14(hc: str):
    result_list = []
    result_list.append("PS：本插件牌理暂不考虑七对子与国士无双听牌\n当前手牌:" + hc + "\n")
    hc = convert_hc_to_list(hc)
    if sum(hc) != 14:
        return "手牌数量存在问题,请输入14张手牌或检查输入牌型是否正常。"
    for amount in hc:
        if amount >4:
            return "手牌枚数异常,请检查输入牌型是否存在问题。"
    xt_list = []
    for x in range(len(hc)):
        if hc[x] > 0:
            # 变位
            hc[x] -= 1
            xt = calc_shanten_13(hc_list=hc)
            if xt:
                xt_list.append([x, xt])
            # 复位
            hc[x] += 1
    # 最小向听数
    if xt_list == []:
        result_list.append("手牌状态：十三不搭\n\n")
        result_list.append("依据场况切手牌中任意一张牌即可。\n")
        return result_list
    xt_min = min([x[1][0] for x in xt_list])
    if xt_min == 0:
        result_list.append("手牌状态：聴牌\n\n")
    else:
        result_list.append("手牌状态：" + f"{xt_min}向听\n\n")
    card_advice_list = []
    for xxt in xt_list:
        xt = xxt[1]
        if xt[0] == xt_min:
            xt[1].sort()
            msum = calc_tenpai_sum(hc, xt[1])
            card_advice_list.append([xxt[0], xt[1], msum])
    card_advice_list.sort(key=lambda x: x[2], reverse=1)
    for x in card_advice_list:
        choice = "打" + convert_num_to_card(x[0]) +"  可摸进:["
        for i in range (0,len(x[1])):
            choice = choice + convert_num_to_card(x[1][i])
            if i != len(x[1])-1:
                choice = choice + "、"
        choice = choice + "]  共" + str(x[2]) +"枚\n"
        result_list.append(choice)
    if not xt:
        return "出现错误，请检查错误日志。"
    return result_list
