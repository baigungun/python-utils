#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
@version: 1.0
@author: huangwan
@license: peopleNet
@contact: wan_huang@people2000.net
@software: PyCharm
@file: randomRate.py
@time: 2017/11/8 20:26
"""
'''
加权随机算法一般应用在以下场景：有一个集合S，里面比如有A,B,C,D这四项。
这时我们想随机从中抽取一项，但是抽取的概率不同，比如我们希望抽到A的概率是50%,
抽到B和C的概率是20%,D的概率是10%。一般来说，我们可以给各项附一个权重，
抽取的概率正比于这个权重。那么上述集合就成了：

{A:5，B:2，C:2，D:1}
'''
import random
import bisect


'''
enumerate 用法注解
>>>seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
'''

class RandomRate():
    def __init__(self):
        pass

    def weight_choice1(self,list,weight):
        """
        把序列按权重值扩展成:lists=[A,A,A,A,A,B,B,C,C,D]
        :param list: 待选取序列
        :param weight: list对应的权重序列
        :return:选取的值
        """
        new_list = []
        for i,val in enumerate(list):
            new_list.extend(val*weight[i])
        return random.choice(new_list)

    def weight_choice2(self,list,weight):
        '''
        sum等于10，如果随机到1-5，则会在遍历第一个数字的时候就退出遍历。符合所选取的概率。
        '''
        t = random.randint(0,sum(weight) -1)
        for i,val in enumerate(weight):
            t -= val
            if t < 0 :
                return list[i]

    def weight_choice3(self,list,weight):
        '''
        weight_sum = [5,7,9,10],t=0-9,
        bisect_right返回t如果要插入weight_sum列表，应该插入的位置。这样t=0-5时都返回0，即返回A
        '''
        weight_sum = []
        sum = 0
        for a in weight:
            sum += a
            weight_sum.append(sum)
        t = random.randint(0,sum - 1)
        idx = bisect.bisect_right(weight_sum,t)
        return list[idx]

if __name__ == '__main__':
    r = RandomRate()
    print r.weight_choice1(['A', 'B', 'C', 'D'], [5, 2, 2, 1])
    print r.weight_choice2(['A', 'B', 'C', 'D'], [5, 2, 2, 1])
    print r.weight_choice3(['A', 'B', 'C', 'D'], [5, 2, 2, 1])
