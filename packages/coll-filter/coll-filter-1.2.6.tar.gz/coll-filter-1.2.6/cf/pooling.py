#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""pool_coll_filter"""

import os
import time
import math
from multiprocessing import Pool
from typing import Iterable, Tuple
from .base import BaseCollFilter
from . import default_similar_func, CFType, U, T
from .utils import print_cost_time, sort_similar, logger


class PoolMultiProcessor:

    def __init__(self, parallel_num):
        cpu_count = os.cpu_count()
        self.parallel_num = cpu_count if parallel_num <= 1 else parallel_num
        self.pool = Pool(cpu_count - 1) if self.parallel_num >= cpu_count else Pool(self.parallel_num - 1)

    def cal_similar(self, dict1, items_list, cal_fn, similar_fn):
        size = len(items_list)
        split_size = math.ceil(size / self.parallel_num)
        results = [self.pool.apply_async(func=cal_fn, args=(dict1, items_list[i:i+split_size], similar_fn))
                   for i in range(split_size, size, split_size)]

        similar = cal_fn(dict1, items_list[:split_size], similar_fn)

        for result in results:
            for key, items in result.get().items():
                if key in similar:
                    for item, score in items.items():
                        similar[key][item] = similar[key].get(item, 0.0) + score
                else:
                    similar[key] = items

        return similar

    def cf(self, user_item_ratings, user_items_list, similar_dict, recall_num, cf_fn):
        size = len(user_item_ratings)
        split_size = math.ceil(size / self.parallel_num)
        results = [self.pool.apply_async(func=cf_fn,
                                         args=(user_item_ratings,
                                               similar_dict,
                                               user_items_list[i:i + split_size],
                                               recall_num
                                               )
                                         )
                   for i in range(split_size, size, split_size)]

        cf_result = cf_fn(user_item_ratings, similar_dict, user_items_list[:split_size], recall_num)

        for result in results:
            cf_result.update(result.get())

        return cf_result

    def release(self):
        self.pool.close()


class PoolCollFilter(BaseCollFilter):

    def __init__(self, data: Iterable[Tuple[U, T, float]], parallel_num=0, similar_fn=default_similar_func,
                 cache_similar=False):
        super().__init__(data, similar_fn, cache_similar)
        self.processor = PoolMultiProcessor(parallel_num)

    def release(self):
        super().release()

    def _cal_similar(self, cf_type: CFType, similar_num, similar_fn):
        """
        计算相似度

        @return dict{:dict}    {user1: {user2: similar}}
        """
        logger.info(f'开始{cf_type.value}相似度计算, similar_num: {similar_num}')
        func_start_time = time.perf_counter()
        dict1, items_list, cal_similar_func = self._get_cal_similar_inputs(cf_type)
        items_list = list(items_list)
        similar_fn = similar_fn if similar_fn else self.similar_fn
        similar = self.processor.cal_similar(dict1, items_list, cal_similar_func, similar_fn)
        similar = sort_similar(similar, similar_num)
        print_cost_time(f"完成{cf_type.value}相似度计算, 当前进程<{os.getpid()}>, 总生成 {len(similar)} 条记录, 总耗时", func_start_time)
        return similar
        self.processor.release()

    def _cf(self, user_ids, similar_dict, recall_num, cf_type: CFType):
        logger.info(f'开始{cf_type.value}推理, recall_num: {recall_num}')
        func_start_time = time.perf_counter()
        if user_ids:
            if not set(user_ids).intersection(self.user_item_ratings.keys()):
                return {user_id: [] for user_id in user_ids}

            user_items_list = list(map(lambda x: (x, self.user_item_ratings.get(x, [])), user_ids))
        else:
            user_items_list = self.user_item_ratings.items()

        cf_func = self._rating_user_cf if cf_type == CFType.UCF else self._rating_item_cf
        if len(user_items_list) > 4096:
            cf_result = self.processor.cf(self.user_item_ratings, user_items_list, similar_dict, recall_num, cf_func)
        else:
            cf_result = cf_func(self.user_item_ratings, similar_dict, user_items_list, recall_num)
        print_cost_time(f"完成{cf_type.value}推理, 当前进程<{os.getpid()}>, 生成{len(cf_result)}条记录, 总耗时", func_start_time)
        return cf_result

