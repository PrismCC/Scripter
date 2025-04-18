"""
utils.py
"""

from collections import UserDict


class IndexableDict(UserDict):
    """
    可用下标索引的字典
    """

    def __init__(self, _dict: dict):
        self._keys = list(_dict.keys())
        self._values = list(_dict.values())
        super().__init__(_dict)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        if key in self._keys:
            index = self._keys.index(key)
            self._values[index] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def __delitem__(self, key):
        super().__delitem__(key)
        index = self._keys.index(key)
        del self._keys[index]
        del self._values[index]

    def key_of_index(self, index: int):
        """
        根据索引获取键
        :param index: 索引
        :return: 键
        """
        return self._keys[index]

    def value_of_index(self, index: int):
        """
        根据索引获取值
        :param index: 索引
        :return: 值
        """
        return self._values[index]

    def get_key_list(self):
        """
        获取键列表
        :return: 键列表
        """
        return self._keys

    def get_value_list(self):
        """
        获取值列表
        :return: 值列表
        """
        return self._values

    def get_dict(self):
        """
        获取字典
        :return: 字典
        """
        return self.data