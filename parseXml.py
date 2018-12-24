#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@version: 1.0
@author: huangwan
@license: peopleNet
@contact: wan_huang@people2000.net
@software: PyCharm
@file: parseXml.py
@time: 2017/4/21 16:39
"""
import xml.etree.ElementTree as ET
import sys
import time
class XmlUtils():
    #只解析一次
    def readXml(self,file):
        tree = ET.parse(file)
        return tree

    def writeXml(self,tree,file):
        tree.write(file,encoding="utf-8",xml_declaration=True)

    '''
    xml功能函数
    '''

    #根据属性判断是否有节点
    def if_match(self,node,kv_map):
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True

    #定位节点
    def find_nodes(self,tree,path):
        return tree.findall(path)

    #根据属性找到节点
    def get_node_by_kv(self,nodelist,kv_map):
        return_nodes = []
        for node in nodelist:
            if self.if_match(node,kv_map):
                return_nodes.append(node)
        return return_nodes

    #新建节点
    def create_node(self,tag,property_map,content):
        element = ET.Element(tag,property_map)
        element.text = content
        return element

    #追加节点
    def add_child_node(self,nodelist,element):
        for node in nodelist:
            node.append(element)

    #删除节点
    def del_node_by_tagkv(self,parent_node,tag,kv_map):

        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and self.if_match(child,kv_map):
                parent_node.remove(child)

    # for test
    def mainProcess(self,infile,outfile):
        tree = self.readXml(infile)
        #所有user节点
        nodes = self.find_nodes(tree,"users/user")
        # print "nodes:",nodes

        #获取某个具体的usr节点
        result_nodes = self.get_node_by_kv(nodes,{"id":"u1"})
        # print "rlt nodes: ",result_nodes

        #获取具体用户下的日期节点
        r = result_nodes[0].getchildren()
        # print "data :",r
        # print self.hasNode(tree,"u1","1479831118")
        # self.insertNode(tree,"u1","1479831118","11111111",outfile)
        # tree2 = self.readXml(infile)
        # self.insertNode(tree,"u3","1479831118","3333333",outfile)
        self.filterNodes(tree,outfile,curTime="",timeInterval=1)


    '''
    功能：判断是否有注册信息。
          如果注册信息的日期大于当前处理信息，也相当于没有注册信息。
          默认信息是按照时间排好序的。
    '''
    def hasNode(self,tree,userId,dateStr):
        curDate = long(dateStr)
        info = ""
        #所有user节点
        users = self.find_nodes(tree,"users/user")
        #获取某个具体的usr节点
        user = self.get_node_by_kv(users,{"id":userId})
        if len(user) == 0:
            return (False,info)
        else:
            #user下的子节点
            childs = user[0].getchildren()
            if len(childs) == 0:
                return (False,info)
            else:
                for child in childs:
                    tmpDate = long(child.attrib["date1"])
                    if tmpDate <= curDate:
                        info = child.text
                        continue
        #没有比当前时间更早的注册信息，则返回空
        if info.strip() == "":
            return (False,info)
        return (True,info)


    '''
    功能：插入节点
    判断是否有同等日期的节点，如果有，更新节点，如果没有，直接插入。
    分为有user节点和无user节点情况。
    '''
    def insertNode(self,tree,userId,dateStr,devInfo,outfile):
        #解决中文字符问题
        # reload(sys)
        # sys.setdefaultencoding('utf-8')

        curTime = long(dateStr)
        users = self.find_nodes(tree,"users/user")
        user = self.get_node_by_kv(users,{"id":userId})
        #没有user节点
        if len(user) == 0:
            # print "== apply cnf  no user =="
            #添加user节点
            newUser = self.create_node("user",{"id":userId},"")
            root = self.find_nodes(tree,"users")
            self.add_child_node(root,newUser)
            self.writeXml(tree,outfile)
            #添加user节点下面的节点
            nodes = self.find_nodes(tree,"users/user")
            # print "now users nodes:",nodes
            n = self.get_node_by_kv(nodes,{"id":userId})
            # print "new user = ",n
            # print "new user devInfo= ",devInfo
            item = self.create_node("item",{"date1":dateStr},devInfo)#devInfo
            self.add_child_node(n,item)
            # print "after insert item new user = ",n[0].getchildren()
            # self.writeXml(tree,outfile)

        else:
            #有user节点，但是没有子节点
            schilds = user[0].getchildren()
            if len(schilds) == 0:
                # print "== apply cnf  has user,no item =="
                sitem = self.create_node("item",{"date1":dateStr},devInfo)
                self.add_child_node(user,sitem)
                # self.writeXml(tree,outfile)

            #有user节点，有子节点，按照时间顺序插入
            else:
                # print "== apply cnf  has user,has item =="
                idx = 0
                updateFlag = False
                for schild in schilds:
                    t = long(schild.attrib["date1"])
                    #如果时间相同，则更新信息
                    if curTime == t:
                        updateFlag = True
                        schild.text = devInfo
                        break
                    #如果时间不同，新增节点，按照时间顺序
                    if curTime > t:
                        idx = idx + 1
                        continue

                if updateFlag == False:
                    iitem = self.create_node("item",{"date1":dateStr},devInfo)
                    # print "insert item idx = ",idx
                    schilds.insert(idx,iitem)

                # self.writeXml(tree,outfile)

    #删除用户申请节点
    def deleteNode(self,tree,userId,dateStr,file):
        users = self.find_nodes(tree,"users/user")
        user = self.get_node_by_kv(users,{"id":userId})
        self.del_node_by_tagkv(user,"item",{"date1":dateStr})
        self.writeXml(tree,file)


    '''
    过滤：有不止一条apply信息的，将一个月之前的apply信息去掉。
          如果要过滤指定日期之前的，将curTime设置为 2016-10-24的格式.
          一个用户保留至少一条申请信息。
    '''
    def filterNodes(self,tree,file,curTime="",timeInterval=30):
        #解决中文字符问题
        # reload(sys)
        # sys.setdefaultencoding('utf-8')

        users = self.find_nodes(tree,"users/user")
        for user in users:
            items = user.getchildren()
            if len(items) < 2:
                continue

            delTimeList = []
            #获取系统当前时间
            if curTime.strip() == "":
                curTimeS = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            else:
                curTimeS = curTime#time.strftime('%Y-%m-%d',curTime)

            timeLong = time.mktime(time.strptime(curTimeS, '%Y-%m-%d')) # 1482286976
            sTime = long(timeLong) - timeInterval*24*60*60
            for item in items:
                tmpTime =long(item.attrib["date1"])
                if tmpTime < sTime:
                    delTimeList.append(tmpTime)
            #保留最后一条不删除
            if delTimeList == []:
                self.writeXml(tree,file)
                continue
            maxDelTime = max(delTimeList)
            for delTime in delTimeList:
                if delTime != maxDelTime:
                    self.del_node_by_tagkv(user,"item",{"date1":str(delTime)})
                    self.writeXml(tree,file)



if __name__ == '__main__':
    x = XmlUtils()
    x.mainProcess("../file/conf/test_apply_cnf.xml","../file/conf/rlt_apply_cnf.xml")
