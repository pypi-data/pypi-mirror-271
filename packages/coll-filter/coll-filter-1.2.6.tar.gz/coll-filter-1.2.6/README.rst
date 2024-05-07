Usage Sample
''''''''''''

.. code:: python

    from cf import CollFilter

    if __name__ == '__main__':
        data = read_data('file_path')
        data = pre_process(data)  # return [(user_id: Any, item_id: Any, float),]
        cf = CollFilter(data)

        ucf = cf.user_cf()  # return {user_id: [(item_id, score),],}
        icf = cf.item_cf()  # return {user_id: [(item_id, score),],}

        recommend = cf.recommend(user_id, recall_num=5) # return [(item_id, score),]
        recommends = cf.recommends(user_ids, recall_num=5) # return {user_id: [(item_id, score),],}

        cf.release()

