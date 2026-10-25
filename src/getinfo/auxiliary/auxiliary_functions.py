import json
import argparse

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

def make_list_equal(arr1, arr2):
    """
    Делает списки равными по длине. Добавляет к меньшему нули
    """
    while len(arr1) < len(arr2):
        arr1.append(0)
    while len(arr2) < len(arr1):
        arr2.append(0)
    return arr1, arr2

def build_parser():
    """
    Создаёт парсер для командной строки

    Здесь 2 параметра: --product и --version для названия продукта и указания версии соотвественно
    """
    parser = argparse.ArgumentParser(prog="getinfo")

    parser.add_argument("--product", required=True, help="Name of the product")
    parser.add_argument("--version", default=None, help="Version of the product")

    return parser