#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
@version: 1.0
@author: huangwan
@license: peopleNet
@contact: wan_huang@people2000.net
@software: PyCharm
@file: binary_search.py
@time: 2017/11/9 11:08
"""
'''
实现二分查找的三种方式：递归,循环,bisect模块.
循环方式比递归效率高。
对于大数据量，则可以用二分查找进行优化。二分查找要求对象必须有序，其基本原理如下：

    1.从数组的中间元素开始，如果中间元素正好是要查找的元素，则搜素过程结束；
    2.如果某一特定元素大于或者小于中间元素，则在数组大于或小于中间元素的那一半中查找，而且跟开始一样从中间元素开始比较。
    3.如果在某一步骤数组为空，则代表找不到。

二分查找也成为折半查找，算法每一次比较都使搜索范围缩小一半， 其时间复杂度为 O(logn)。
'''
import random
import bisect

class Binary_search():
    def __init__(self):
        pass

    #递归
    def recursion(self,lst,value,low,high):
        '''
        :param lst: 排序后的列表
        :param value: 要查找的数据
        :param low: 最小索引
        :param high: 最大索引
        :return: 查找到的数据的索引
        '''
        if high < low:
            return None

        mid = (low + high) / 2
        if lst[mid] > value:
            return  self.recursion(lst,value,low,mid -1)
        elif lst[mid] < value:
            return  self.recursion(lst,value,mid+1,high)
        else:
            return mid

    #循环
    def loop(self,lst,val):
        low,high = 0,len(lst) -1
        while low <=high:
            mid = (low + high) / 2
            if lst[mid] < val:
                low = mid +1
            elif lst[mid] > val:
                high = mid -1
            else:
                return mid
        return None

    #Python 有一个 bisect 模块，用于维护有序列表。
    # bisect 模块实现了一个算法用于插入元素到有序列表。这样不必要每次都对列表sort操作
    def bisectSearch(self):
        random.seed(1)
        print "-----"
        l = []
        for i in range(1,15):
            r = random.randint(1,100)
            position = bisect.bisect(l,r)
            bisect.insort(l,r)
            print '%3d  %3d' % (r,position), l

    def bisectFunc(self,list,val):
        l = []
        for i in list:
            postion = bisect.bisect(l,i)
            bisect.insort(l,i)
        print "bisect list = ", l
        idx = bisect.bisect_left(l,val)
        return idx

    # def mutiply(self,list):
    #     print "org list = ",list
    #     l = []
    #     i = 0
    #     while i < len(list) and i+1 < len(list):
    #         print "multiply = ",list[i],list[i+1]
    #         tmp = list[i] * list[i+1]
    #         list.pop(0)
    #         list.pop(0)
    #
    #         i = i + 2
    #
    #         l.extend(list)
    #         l.append(tmp)
    #
    #     print "l = ",l,len(l)
    #     if len(l) == 1:
    #         print "====end ===="
    #         return l
    #
    #     self.mutiply(l)





if __name__ == '__main__':
    list = [4,5,6,3,7,9]
    val = 6
    #递归,循环需要先对数组排序
    sort_list = sorted(list)
    print  sort_list

    b = Binary_search()
    print "递归查找结果 = ",b.recursion(sort_list,val,0,len(list))
    print "循环查找结果 = ",b.loop(sort_list,val)
    print "bisect查找结果 = ",b.bisectFunc(list,val)
    # ll = range(1,1231)
    # print b.mutiply(ll)

