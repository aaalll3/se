"""
解析原始 xml 文件，每个数据生成 dict，保存到 data/parsed 中
"""

import os
import re
import pickle
import xmltodict
import zipfile
import itertools
from xml.parsers.expat import ExpatError
from collections import Counter
from multiprocessing import Pool
from typing import *
from config import *


def xml_zip_paths() -> Iterator[str]:
    """
    :return: 所有 xml 压缩包路径的 generator
    """
    for root, dirs, files in os.walk(XML_ZIP_DIR):
        for filename in files:
            if filename[-4:] == '.zip':
                yield os.path.join(root, filename)


def all_xml() -> Iterator[Tuple[str, str]]:
    """
    :return: generator (文件目录，文件内容)
    """
    for zip_path in xml_zip_paths():
        file = zipfile.ZipFile(zip_path)
        for file_info in file.infolist():
            if '__MACOSX' in file_info.filename:
                continue
            if file_info.filename[-4:] == '.xml':
                try:
                    yield os.path.join(zip_path, file_info.filename), file.read(file_info).decode()
                except UnicodeDecodeError:
                    print('cannot decode file "%s"' % file_info.filename)
                    print(file.read(file_info))


def extract_values(name: str, d: dict) -> Iterator[Tuple[str, str]]:
    """
    :return: 所有的 '@nameCN' 和 '@value'（或 '@oValue'）对
    """
    value = d.get('@value', d.get('@oValue'))
    if value is not None:
        yield d.get('@nameCN', name), value
    for key, value in d.items():
        if isinstance(value, dict):
            for tup in extract_values(key, value):
                yield tup


def parse_one(tup: Tuple[str, str]) -> Tuple[str, Dict[str, Set[str]]]:
    """
    解析 xml 字符串，生成字典
    """
    path, raw = tup
    try:
        parsed = xmltodict.parse(raw)['writ']
    except (ExpatError, KeyError):
        return '', {}
    result = {}
    for key, value in extract_values('ROOT', parsed):
        if key in result:
            result[key].add(value)
        else:
            result[key] = {value}
    return path, {key: list(value) for key, value in result.items()}


def parse_all(chunk_size: int = 10000):
    """
    解析所有 xml，每 `chunk_size` 个保存一个文件
    """
    print('parsing xml files...')
    with Pool(NPROC) as pool:
        xml_generator = all_xml()
        for cnt in itertools.count():
            chunk = itertools.islice(xml_generator, chunk_size)
            output = [
                (path, value) for path, value in
                pool.imap_unordered(parse_one, chunk, 100)
                if isinstance(value, dict) and ('全文' in value or 'QW' in value)
            ]
            if len(output) == 0:
                break
            output_path = os.path.join(OUTPUT_DIR, 'parsed_%02d' % cnt)
            pickle.dump(output, open(output_path, 'wb'))
            print('%d entries > %s' % (len(output), output_path))


def all_data(try_parse=True) -> Iterator[Tuple[str, Dict[str, str]]]:
    """
    :return: 从 parsed 读取所有样本的 dict
    """
    parsed_paths = [
        os.path.join(root, filename)
        for root, dirs, files in os.walk(OUTPUT_DIR)
        for filename in files if filename[:7] == 'parsed_'
    ]
    if len(parsed_paths) == 0:
        if try_parse:
            parse_all()
            return all_data(False)
        else:
            raise Exception('cannot find data')

    for path in parsed_paths:
        for key, entry in pickle.load(open(path, 'rb')):
            yield key, entry
