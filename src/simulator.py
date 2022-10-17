import pygame
from bounding_volumes import *
from collision_detection import *
from utils import *
from math import *


#Parameters
width = 800
height = 800

def make_world(model):
    s = make_static_objects(model,3,PATH)   #import the static objects from config file to the class object
    generate_BVT(s[0],s[0].name,model)      #generate the BV Tree
    generate_BVT(s[1],s[1].name,model)
    generate_BVT(s[2],s[2].name,model)
    s[0].change_pos((300,300))
    s[1].change_pos((600,300))
    s[2].change_pos((300,600))

    d = make_dynamic_objects(model,PATH,['truck','bike'])
    generate_BVT(d['dynamic_truck'],d['dynamic_truck'].name,model)
    generate_BVT(d['dynamic_bike'],d['dynamic_bike'].name,model)
    d['dynamic_truck'].change_pos((100,400))
    d['dynamic_bike'].change_pos((150,200))

    car = make_avatar(model,PATH)
    generate_BVT(car,car.name,model)
    car.change_pos((0,300))

    return s,d,car

def draw_static(s,win,draw_bounds= False):
    for i in s:
        i.draw(win,draw_bounds)

def draw_dynamic(d,win,draw_bounds = False):
    d['dynamic_truck'].draw(win,draw_bounds)
    d['dynamic_bike'].draw(win,draw_bounds)






if __name__ == '__main__':
    
    pygame.init()
    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Haptics Simulator")

    s,d,car = make_world(model)
    
    run = True
    pos = (0,0)
    w_key = False
    d_key = False
    a_key = False
    s_key = False
    while run:
        win.fill(GREY)
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
            
        if s_key:
            pos = (0,1)
            
        if a_key:
            pos = (-1,0)
            
        if d_key:   
            pos = (1,0)
        
        car.update_pos(pos)
        pos = (0,0)
        car.draw(win)
        draw_static(s,win)
        draw_dynamic(d,win)
        struck , comment = world_collision_checker(car,d,s)
        if struck:
            win.fill(WHITE)
            car.draw(win,True)
            draw_static(s,win,True)
            draw_dynamic(d,win,True)
            pygame.display.update()
        
        pygame.time.delay(20)
        
        pygame.display.update()





