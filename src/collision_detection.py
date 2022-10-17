import numpy as np
import math 
from bounding_volumes import *
import time 
from itertools import product


def visualise_BVT(root,level = 0):
    print("Level ",level,": ",root.name," bounds:",root.bounds, root.leaf)
    if root.children:
        for child in root.children:
            visualise_BVT(child,level=level+1)
        
    return


def collision(obA,obB):
    return True if (obA[0]<obB[2]+obB[0] and obA[2]+obA[0]>obB[0] and obA[1]<obB[3]+obB[1] and obA[3]+obA[1]>obB[1]) else False

def BVT_collision(nodeA,nodeB,flag= False):
    # print("collsion checking for ",nodeA.name," and ",nodeB.name,"Collsion: ",collision(nodeA.bounds,nodeB.bounds))
    if(nodeA.leaf and nodeB.leaf):
        flag = True
        return collision(nodeA.bounds,nodeB.bounds)    
    if collision(nodeA.bounds,nodeB.bounds):
        for childA in nodeA.children:
           flag = BVT_collision(nodeB,childA,flag)
        for childB in nodeB.children:
           flag = BVT_collision(childB,nodeA,flag)
           if flag: break
        #traverse further till leaf node
    return flag


def world_collision_checker(avatar,d,s):
    if BVT_collision(avatar.bvt_root,d['dynamic_truck'].bvt_root):
        return True,"avatar and truck"

    if BVT_collision(avatar.bvt_root,d['dynamic_bike'].bvt_root):
        return True,"avatar and bike"

    if BVT_collision(avatar.bvt_root,s[0].bvt_root):
        return True,"avatar and static_1"

    if BVT_collision(avatar.bvt_root,s[1].bvt_root):
        return True,"avatar and static_2"

    if BVT_collision(avatar.bvt_root,s[2].bvt_root):
        return True,"avatar and static_3"
    
    return False,"No Collision"