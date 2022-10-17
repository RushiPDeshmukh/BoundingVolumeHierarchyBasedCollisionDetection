from pickle import TRUE
from collision_detection import *
from utils import *
import pygame
import os
from collections import defaultdict


PATH = os.getcwd() + "/models"

##################### Static Object Class ##########################

class static_object:
    def __init__(self,name,size,path,bvt,pos = (0,0)):
        self.name = name
        self.pos = pos
        self.size = size
        self.path = path
        self.bvt_root = bvt
        self.surf = pygame.image.load(path)
        self.surf = pygame.transform.scale(self.surf,self.size)
        self.surf.set_colorkey(WHITE)

    def draw(self,win,draw_bv = False):
        surf = self.surf

        rect1 = surf.get_rect()
        rect1.center = (self.pos[0]+ self.size[0]/2, self.pos[1]+ self.size[1]/2)
        win.blit(surf,rect1)
        if draw_bv:
            self.draw_bvt(win)
        return

    def get_pos(self):
        return self.pos

    def change_pos(self,pos):
        self.pos = pos
        self.bvt_root.update_node(self.pos)
        return

    def draw_bvt(self,win):
        self.bvt_root.draw(win)

##################### Dynamic Object Class ##########################
class dynamic_object:
    def __init__(self,name,size,path,bvt,pos = (0,0)):
        self.name = name
        self.pos = pos
        self.size = size
        self.path = path
        self.bvt_root = bvt
        self.surf = pygame.image.load(path)
        self.surf = pygame.transform.scale(self.surf,self.size)
        self.surf.set_colorkey(WHITE)

    def draw(self,win,draw_bv = False):
        surf = self.surf

        rect1 = surf.get_rect()
        rect1.center = (self.pos[0]+ self.size[0]/2, self.pos[1]+ self.size[1]/2)
        win.blit(surf,rect1)
        if draw_bv:
            self.draw_bvt(win)
        return

    def change_pos(self,pos):
        self.pos = pos
        self.bvt_root.update_node(self.pos)
        return
    
    def update_pos(self,pos_d):
        self.pos = self.pos[0] + pos_d[0],self.pos[1] + pos_d[1]
        self.bvt_root.update_node(self.pos)
        return self.pos
    
    def get_pos(self):
        return self.pos

    def draw_bvt(self,win):
        self.bvt_root.draw(win)

##################### Avatar Class ##########################

class Avatar:
    def __init__(self,name,size,path,bvt,pos = (0,0)):
        self.name = name
        self.pos = pos
        self.size = size
        self.path = path
        self.bvt_root = bvt
        self.surf = pygame.image.load(path)
        self.surf = pygame.transform.scale(self.surf,self.size)
        self.surf.set_colorkey(WHITE)

    def draw(self,win,draw_bv = False):
        surf = self.surf

        rect1 = surf.get_rect()
        rect1.center = (self.pos[0]+ self.size[0]/2, self.pos[1]+ self.size[1]/2)
        win.blit(surf,rect1)
        if draw_bv:
            self.draw_bvt(win)
        return
    
    def change_pos(self,pos):
        self.pos = pos
        self.bvt_root.update_node(self.pos)
        return
    
    def update_pos(self,pos_d):
        self.pos = self.pos[0] + pos_d[0],self.pos[1] + pos_d[1]
        self.bvt_root.update_node(self.pos)
        return self.pos
    
    def get_pos(self):
        return self.pos

    def draw_bvt(self,win):
        self.bvt_root.draw(win)

##################### BVT node Class ##########################

class BVT_node:
    def __init__(self,name,bounds,pos=(0,0),leaf = False):
        self.name = name
        self.fixedbounds = bounds
        self.bounds = self.fixedbounds
        self.pos = pos
        self.children = []
        self.leaf = leaf

    def update_node(self,pos):
        self.pos = pos
        self.bounds = (self.fixedbounds[0]+self.pos[0],self.fixedbounds[1]+self.pos[1],self.fixedbounds[2],self.fixedbounds[3])
        for child in self.children: child.update_node(pos)

    def refresh(self):
        self.bounds = (self.fixedbounds[0]+self.pos[0],self.fixedbounds[1]+self.pos[1],self.fixedbounds[2],self.fixedbounds[3])
        for child in self.children: child.refresh()

    def draw(self,win):
        self.refresh()
        pygame.draw.rect(win,GREEN,self.bounds,2)
        for child in self.children: child.draw(win)


##################### BVT Tree generator function #######################
def generate_BVT(object, object_name, model):
    tree = defaultdict()
    root = model[object_name]['BVH']['level_0'][0]
    tree['root'] = BVT_node('root',root[1:],object.pos)
    object.bvt_root = tree['root']
    num_levels = model[object_name]['BVH']['num_levels']
    if num_levels != 1:
        for i in range(1,num_levels):
            for node in model[object_name]['BVH']['level_'+str(i)]:
                parent,name,bounds = node[0],node[1],node[2:]
                bv = BVT_node(name,bounds,object.pos,i == num_levels-1)
                tree[parent].children.append(bv)
                tree[name] = bv
    else:
        object.bvt_root.leaf = True
    return
            

    

##################### Make obstacles functions ##########################
def make_static_objects(model,num_objects,PATH):
    static_objects = []
    for i in range(1,num_objects+1):
        name = "static_"+str(i)
        size = model[name]['size']
        path = PATH + model[name]['path']
        bvt = None
        static_objects.append(static_object(name,size,path,bvt))

    return static_objects


def make_dynamic_objects(model,PATH,names = ['truck','bike']):
    dynamic_objects = {}
    for i in names:
        name = "dynamic_"+i
        size = model[name]['size']
        path = PATH +model[name]['path']
        bvt = None
        dynamic_objects[name] = dynamic_object(name,size,path,bvt)

    return dynamic_objects

def make_avatar(model, PATH):
    name = "avatar_car"
    size = model[name]['size']
    path = PATH + model[name]['path']
    bvt = None
    avatar = Avatar(name,size,path,bvt)

    return avatar

def print_tree():
    pass


if __name__ == '__main__':

    s= make_static_objects(model,3,PATH)
    d = make_dynamic_objects(model,PATH,['truck','bike'])
    print(d.keys())
    s3 = s[2]
    generate_BVT(d['dynamic_truck'],d['dynamic_truck'].name,model)
    generate_BVT(d['dynamic_bike'],d['dynamic_bike'].name,model)
    d['dynamic_truck'].change_pos((200,200))
    d['dynamic_bike'].change_pos((200,200))
    generate_BVT(s3,s3.name,model)
    
    pygame.init()
    width_win = 600
    win = pygame.display.set_mode((width_win,width_win))
    pygame.display.set_caption("Title")

    car = make_avatar(model,PATH)
    avatar1 = make_avatar(model,PATH)
    generate_BVT(avatar1,avatar1.name,model)
    generate_BVT(car,car.name,model)
    avatar1.change_pos((200,200))
    
    run = True
    pos = (0,0)
    w_key = False
    d_key = False
    a_key = False
    s_key = False
    while run:
        win.fill(WHITE)
        events = pygame.event.get()

        for ev in events:
            if ev.type == pygame.QUIT:
                run = False
                pygame.quit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_w:
                    w_key = True
                    
                if ev.key == pygame.K_s:
                    s_key = True
                    
                if ev.key == pygame.K_a:
                    a_key = True
                    
                if ev.key == pygame.K_d:
                   d_key = True
            if ev.type == pygame.KEYUP:
                if ev.key == pygame.K_w:
                    w_key = False
                    
                if ev.key == pygame.K_s:
                    s_key = False
                    
                if ev.key == pygame.K_a:
                    a_key = False
                    
                if ev.key == pygame.K_d:
                   d_key = False

        if w_key:
            pos = (0,-1)
            car.update_pos(pos)
        if s_key:
            pos = (0,1)
            car.update_pos(pos)
        if a_key:
            pos = (-1,0)
            car.update_pos(pos)
        if d_key:
            pos = (1,0)
            car.update_pos(pos)
        car.draw(win)
        # avatar1.draw(win)
        d['dynamic_bike'].draw(win)
        if BVT_collision(d['dynamic_bike'].bvt_root,car.bvt_root):
            win.fill(YELLOW)
            car.draw(win)
            # avatar1.draw(win)
            d['dynamic_bike'].draw(win)
            pygame.display.update()
        pygame.time.delay(30)
        
        pygame.display.update()
