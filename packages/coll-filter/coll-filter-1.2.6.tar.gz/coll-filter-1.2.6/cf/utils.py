#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from typing import Iterable, Tuple, Mapping
from logging import basicConfig, INFO, getLogger

logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def read_data(path: str) -> Iterable[str]:
    with open(path) as f:
        lines = f.readlines()
    return lines


def handle_line(line: str) -> (str, str, float):
    user_id, item_id, score = line.strip().split(",")
    return user_id.strip(), item_id.strip(), float(score.strip())


def pre_process(data: Iterable[str], handle_func=handle_line) -> Iterable[Tuple[str, str, float]]:
    return map(handle_func, data)


def sort_similar(similar: Mapping, similar_num: int):
    for key, item_score in similar.items():
        similar[key] = sorted(item_score.items(), key=lambda x: x[1], reverse=True)[:similar_num]
    return similar


def print_cost_time(task_content, start_time):
    logger.info(f"{task_content}: {time.perf_counter()-start_time:.2f} seconds.")


def fusion(icf_items, ucf_items, recall_num, ratio):
    """

    :param icf_items: item_cf列表
    :param ucf_items: user_cf列表
    :param recall_num: 每个用户最大召回个数
    :param ratio: 推荐结果中item_cf所占比例
    :return:
    """
    ucf_items_dict = dict(ucf_items)
    # item_cf和user_cf共同出现的先放进result_items里
    result_items = [(item[0], item[1] + ucf_items_dict[item[0]]) for item in icf_items if item[0] in ucf_items_dict]
    result_items_len = len(result_items)
    if result_items_len >= recall_num:
        return result_items[:recall_num]

    leave_num = recall_num - result_items_len
    half = round(leave_num * ratio + 1e-5)  # 加1e-5避免1.5、2.5等四舍五入向下取整
    result_item_ids = [item[0] for item in result_items]
    leave_icf_items = [item for item in icf_items if item[0] not in result_item_ids]
    leave_ucf_items = [item for item in ucf_items if item[0] not in result_item_ids]
    if len(leave_icf_items) > half and len(leave_ucf_items) > (leave_num - half):
        result_items.extend(icf_items[:half])
        result_items.extend(leave_ucf_items[:(leave_num - half)])
        return result_items
    elif len(leave_icf_items) < half:
        result_items.extend(leave_icf_items)
        result_items.extend(leave_ucf_items[:(leave_num - half)])
        return result_items
    elif len(leave_ucf_items) < (leave_num - half):
        result_items.extend(leave_icf_items[:(leave_num - len(leave_ucf_items))])
        result_items.extend(leave_ucf_items)
        return result_items

    result_items.extend(leave_icf_items[:leave_num])
    leave_num = recall_num - len(result_items)
    if leave_num > 0:
        result_items.extend(leave_ucf_items[:leave_num])

    return result_items

