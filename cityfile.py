# -*- coding:utf-8 -*-
"""
作者：苎夏星染
日期：2022年11月24日
"""
import time
import pypinyin
import tqdm
from loguru import logger
from fuzzywuzzy import process

logger.add("log.txt", rotation="10MB", encoding="UTF-8", enqueue=True, retention="10 days")


class Cities:
    dict_city = {}

    def __init__(self):

        """
        从文件中读取内容写入到字典
        :param 传入要存储文件内容的空字典
        :return: 无返回值
        """

        f = open("cities.txt", "r", encoding="UTF-8")
        try:
            temp = 0
            for line in f:
                data = line.strip().split(":")
                self.dict_city[data[0]] = data[1]
                temp += 1
            for i in tqdm.tqdm(range(temp), desc="loading..."):
                time.sleep(0.01)
            logger.info("The file was successfully read")
        except Exception as e:
            logger.error(f"The file was failed read,error is '{e}'")
        finally:
            f.close()

    def add_cities(self):

        """
        添加新城市，将城市名为key，首字母为value存入字典，调用时输入想添加的城市名称
        :param 传入想要增加新城市名的字典，
        :return: 无返回值
        """

        x = input("请输入添加的城市名\n")
        if 'A' <= x[0].upper() <= 'Z':
            self.dict_city[x] = x[0].upper()
        elif 'A' <= pypinyin.lazy_pinyin(x, style=pypinyin.Style.FIRST_LETTER)[0].upper() <= 'Z':
            self.dict_city[x] = pypinyin.lazy_pinyin(x, style=pypinyin.Style.FIRST_LETTER)[0].upper()
        else:
            logger.warning("The name doesn't conform to the specification")
            return
        logger.info(f"The city name was added successfully,its name is {x}")

    def add_files(self):

        """
        在已存在的文件末尾写入字典中的数据
        :param 传入想要在文件内添加新内容的字典
        :return: 无返回值
        """

        f = open("cities.txt", "a", encoding="UTF-8")
        try:
            for key in self.dict_city:
                f.write(f"{key}:{self.dict_city[key]}\n")
            logger.info("The file was successfully written")
        except Exception as e:
            logger.error(f"The file was failed written,error is '{e}'")
        finally:
            f.close()

    def new_files(self):

        """
        覆盖文件内原有的数据写入字典中的数据
        :param 传入想要在文件内添加新内容的字典
        :return: 无返回值
        """

        f = open("cities.txt", "w", encoding="UTF-8")
        try:
            for key in self.dict_city:
                f.write(f"{key}:{self.dict_city[key]}\n")
            logger.info("The file was successfully written")
        except Exception as e:
            logger.error(f"The file was failed written,error is '{e}'")
        finally:
            f.close()


def fuzzy_match(para: str, target_range):
    """
    对字符串在可遍历数据类型中进行模糊匹配
    :param para: 需要匹配的字符串
    :param target_range: 进行匹配的可遍历数据类型
    :return: 带有匹配数据和相似度的二维元组
    """

    if type(para).__name__ != 'str':
        logger.warning("Error in the type of the input data")
        return
    temp = process.extract(para, list(target_range), limit=len(target_range))
    target = ((x[0], x[1]) for x in temp if x[1] > 0)
    logger.info("Fuzzy matching success")
    return tuple(target)


if __name__ == "__main__":
    a = Cities()
    print(a.dict_city.keys())
    a.add_cities()
    print(a.dict_city)
