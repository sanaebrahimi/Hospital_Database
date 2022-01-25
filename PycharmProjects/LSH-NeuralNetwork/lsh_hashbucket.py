import collections
import os
import sys
import math
import random
import numpy as np
import numpy.random
import scipy as sp
import scipy.stats
from importlib import reload

class LSH:
    def __init__(self, func, K, L):
        self.func = func
        self.K = K
        self.L = L
        self.sample_size = 0
        self.count = 0
        self.hash_buckets = HashBuckets(K, L)
    def stats(self):
        avg_size = self.sample_size // max(self.count, 1)
        self.sample_size = 0
        self.count = 0
        print("Avg. Sample Size:", avg_size)

    def insert(self, item_id, item):
        fp = self.func.hashSignature(item)
        self.hash_buckets.insert(fp, item_id)



    # def insert_multi(self, items, N):
    #     fp = self.func.hash(items).int().cpu().numpy()
    #     self.lsh_.insert_multi(fp, N)

    # def query_remove_matrix(self, items, labels, total_size):
    #     # for each data sample, query lsh data structure, remove accidental hit
    #     # find maximum number of samples
    #     # create matrix and pad appropriately
    #     batch_size, D = items.size()
    #     fp = self.func.hash(items).int().cpu().numpy()
    #     result, total_count = self.lsh_.query_matrix(fp, labels.cpu().numpy(), batch_size, total_size)
    #     batch_size, ssize = result.shape
    #     self.sample_size += total_count
    #     self.count += batch_size
    #     return result

    def query_remove(self, item, label):
        fp = self.func.hashSignature(item)
        result = self.hash_buckets.query(np.squeeze(fp))
        if label in result:
            result.remove(label)
        self.sample_size += len(result)
        self.count += 1
        return list(result)

    def query(self, item):
        fp = self.func.hashSignature(item)
        result = set(self.hash_buckets.query(fp))
        self.sample_size += len(result)
        self.count += 1
        return result

    # def query_multi(self, items, N):
    #     fp = self.func.hash(items).int().cpu().numpy()
    #     return list(self.lsh_.query_multi(fp, N))

    def clear(self):
        self.hash_buckets.clear()



class HashBuckets:

    def __init__(self, K, L):
        self.tables = []
        self.K = K
        self.L = L
        for i in range(L):
            table ={}
            self.tables.append(table)

    def insert(self, fp, item_id):

        for idx in range (self.L):
            self.add(fp[idx], idx, item_id)

    def add(self, key, id, item_id):
        table = self.tables[id]
        if key not in table.keys():
            self.tables[id][key] = [item_id]

        else:
            self.tables[id][key].append(item_id)

    def query(self, keys):

        result = []
        for i in range (self.L):
            self.retrieve(result, i, keys[i])

        # result.remove(-1)
        # print("query", result)
        return result

    def retrieve(self, res, table_id, key):
        table = self.tables[table_id]
        # print(table.keys())
        # print(key)
        if key in table.keys():
            res += table[key]
        # print("ret", res)
    def clear(self):
        for i in range(self.L):
            self.tables[i] = {}

