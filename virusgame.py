from kivy.app import App
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
import random
from kivy.core.window import Window
from kivy.uix.image import Image 
from kivy.uix.label import Label,CoreLabel
from kivy.core.audio import SoundLoader
from kivy.graphics import Ellipse,Color,Rectangle
#m kivy.graphics import Instructions
import math
import time
Window.clearcolor = (1, 1, 1, 1)


#Just following kivy documentation, pg 282 
class MyKeyboardListener(Widget):
    def __init__(self, **kwargs):
        super(MyKeyboardListener,self).__init__(**kwargs)
        
        self._keyboard = Window.request_keyboard(self._keyboard_closed,self)
        self._keyboard.bind(on_key_down = self._on_keyboard_down)
        self._keyboard.bind(on_key_up = self._on_keyboard_up)
        self.keyset = set()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_keyboard_down)
        self._keyboard.unbind(on_key_up = self._on_keyboard_up)
        self._keyboard = None
    
    def _on_keyboard_down(self,keyboard,keycode,text,modifiers):
        if keycode[1] == "escape":
            return keyboard.release()
        else:
            self.keyset.add(keycode[1])

    #recycle my self.keyset
    def _on_keyboard_up(self,keyboard,keycode):
        if keycode[1] in self.keyset:
            self.keyset.remove(keycode[1])

class Text_Image(Widget):
    def __init__(self,x,y,txt,src="",fontsize = 30):
        self.live_label = CoreLabel(text= txt,font_size = fontsize)
        self.live_label.refresh()
        self.label_instruction = Rectangle(texture = self.live_label.texture,pos=(x,y),size=self.live_label.texture.size)
        self.image_instruction = Rectangle(source = src,pos=(x+100,y),size=(30,30) )
class Score(Widget):
    def __init__(self,x,y):
        self._score_label = CoreLabel(text="Score : 0",font_size = 30)
        self._score_label.refresh()
        self.score_label_instruction = Rectangle(texture = self._score_label.texture,pos=(x,y),size=self._score_label.texture.size)
        self._score = 0
    
    @property
    def score(self):
        return self._score
    @score.setter
    def score(self,val):
        self._score = val
        self._score_label.text = "Score : " + str(val)
        self._score_label.refresh()
        self.score_label_instruction.texture = self._score_label.texture
        self.score_label_instruction.size = self._score_label.texture.size

class Entity():
    def __init__(self,x,y,r,src):
        self._x = x
        self._y = y
        #kivy takes size as (major,minor)
        self._r = r
        self._size = (r*2,r*2)
        self._source = src
        self._instruction = Ellipse(pos = (self._x,self._y),size = self._size,source = self._source)

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,val):
        self._x = val
        self._instruction.pos = (self._x,self._y)

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,val):
        self._y = val
        self._instruction.pos = (self._x,self._y)

    @property
    def r(self):
        return self._r
    @r.setter
    def r(self,val):
        self._r = val
        self._size = (val*2,val*2)
        self._instruction.size = (self._size)
         
    @property
    def source(self):
        return self._x
    @source.setter
    def source(self,val):
        self._source = val
        self._instruction.source = self._source

class Virus(Entity):
    def __init__(self, x, y, r, src):
        super().__init__(x, y, r, src)
        self.pos = (self.x,self.y)
        self.v_x = 0
        self.v_y = 0
        self.velocity = (self.v_x,self.v_y)
        
    def move(self):
        #* just means to unpack
        self.pos = Vector(*self.velocity) + self.pos
        self.x = self.pos[0]
        self.y = self.pos[1]

    def update(self,*largs):
        self.v_x = self.velocity[0]
        self.v_y = self.velocity[1]
        self.move()

        # bounce off top and bottom
        if (self.y < 0) or (self.y+50 > Window.height):
            self.v_y *= -1
            self.velocity = (self.v_x,self.v_y)

        # bounce off left and right
        if (self.x < 0) or (self.x+50 > Window.width):
            self.v_x *= -1 
            self.velocity = (self.v_x,self.v_y)

class Player(Entity):
    def __init__(self, x, y, r, src):
        super().__init__(x, y, r, src)
        self.kb = MyKeyboardListener()
   
    def move(self,dt):
        step = 10
        if self.x <=0:            
            if "d" in self.kb.keyset:
                self.x += step
            if "w" in self.kb.keyset:
                self.y += step
            if "s" in self.kb.keyset:
                self.y -= step
        elif self.x >= Window.width-70:
            if "a" in self.kb.keyset:
                self.x -= step            
            if "w" in self.kb.keyset:
                self.y += step
            if "s" in self.kb.keyset:
                self.y -= step
        elif self.y <= 0:
            if "a" in self.kb.keyset:
                self.x -= step            
            if "d" in self.kb.keyset:
                self.x += step
            if "w" in self.kb.keyset:
                self.y += step
        elif self.y >= Window.height-70:
            if "a" in self.kb.keyset:
                self.x -= step            
            if "d" in self.kb.keyset:
                self.x += step     
            if "s" in self.kb.keyset:
                self.y -= step
        else:
            if "a" in self.kb.keyset:
                self.x -= step            
            if "d" in self.kb.keyset:
                self.x += step
            if "w" in self.kb.keyset:
                self.y += step            
            if "s" in self.kb.keyset:
                self.y -= step

class Healthpack(Virus):
    def __init__(self, x, y, r, src):
        super().__init__(x, y, r, src)

class GameMain(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kb = MyKeyboardListener()
        self._entities = set()
        self._vitities = list()
        self.score = Score(600,0)
        self.start_time = 0
        self.global_time = time.time()
        self.bg_music = SoundLoader.load("asset/bg_music.wav")
        self.addone = SoundLoader.load("asset/addone.wav")
        self.boom = SoundLoader.load("asset/boom.wav")
        self.virus_num = 0
              
        self.bg_music.play()
        self.bg_music.loop = True
        self.test = Text_Image(400,400,"test")
        with self.canvas:
            #set the main color
            Color(1, 0.7, 0.5, 1)
 
        self.live1 = Text_Image(10,5,"Lives : ","asset/heart.png")
        self.live2 = Text_Image(50,5,"Lives : ","asset/heart.png")
        self.live3 = Text_Image(90,5,"Lives : ","asset/heart.png")
        self.endgame = Text_Image(Window.width/2 - 221,Window.height-200,"GAME OVER",fontsize=80)
        self.player = Player(300,200,50,"asset/character.png")
        self.healthpack = Healthpack(0,300,25,"asset/first_aid.png")

        self.canvas.add(Color(1, 0.7, 0.5, 1))
        self.canvas.add(self.score.score_label_instruction)
        self.canvas.add(self.live1.label_instruction)
        self.canvas.add(self.live1.image_instruction)
        self.canvas.add(self.live2.image_instruction)
        self.canvas.add(self.live3.image_instruction)
        self.lives_remaining = [self.live1.image_instruction,self.live2.image_instruction,self.live3.image_instruction]

        self.add_entity(self.player)
    
        Clock.schedule_interval(self.player.move,1/30)

       


    def collide(self,c1,c2,*largs):
        
        #assume all entities are circles, so radius is just either size[0] or size[1]
        #however this is not exactly correct as I only recently found out...
        dx = c1.x - c2.x
        dy = c1.y-c2.y
        distance = math.sqrt(dx * dx + dy * dy)
       
        if distance < (c1.r + c2.r):
  
     
            self.remove_entity(c2)
          
            return True
    
    def collide_virus(self,c1,c2,*largs):
        
        #assume all entities are circles, so radius is just either size[0] or size[1]
        dx = c1.x - c2.x
        dy = c1.y-c2.y
        distance = math.sqrt(dx * dx + dy * dy)
       
        if distance < (c1.r + c2.r):
  
            
            self.remove_vitities(c2)
          
            return True

    def add_entity(self,entitiy):
        #_entities is a set
        self._entities.add(entitiy)
        self.canvas.add(entitiy._instruction)

    def add_vitities(self,v):
        #_vitities is a list
        self._vitities.append(v)
        self.canvas.add(v._instruction)

    def remove_entity(self,entity):
        try:
            self._entities.remove(entity)
            self.canvas.remove(entity._instruction)
            
        except:
            pass

    def remove_vitities(self,v):
        try:
            self._vitities.remove(v)
            self.canvas.remove(v._instruction)
        except:
            pass

    def mutant_check(self,dt):
        # for the first few checks, time.time - start_time >> 3
        elapsed_time = time.time() - self.start_time
        if (elapsed_time > 3):
            self.player.source = "asset/character.png"
            self.player.r = 50
            game.state = "begin"
            self.start_time = 0            

            
        elif self.healthpack not in self._entities and game.state!="begin":
            self.player.source = "asset/mutant.png"
            self.player.r = 75
            game.state = "mutant"
                    
    def add_healthpack(self,*largs):
        #because canvas is not a set, it is not unique. hence have to remove residue
        try:
            self.canvas.remove(self.healthpack._instruction)
        except:
            pass
        self.healthpack.velocity = Vector(4, 0).rotate(random.randint(0, 360))
        self.add_entity(self.healthpack)
        
    def healthpack_check(self,*largs):
        
        if self.healthpack in self._entities:
            #dont need to have clock because this function is alr in a clock
            self.healthpack.update()              
 
            if self.collide(self.player,self.healthpack) == True:
                self.collide(self.player,self.healthpack)
                self.start_time = time.time()
            game.state = "normal"

    def add_virus(self,*largs):
        if time.time() - self.global_time >10:
            virus_name = "virus"+str(self.virus_num)
            virus_name = Virus(0,100,40,"asset/pink.png")
            self.add_vitities(virus_name)
            virus_name.velocity = Vector(4, 0).rotate(random.randint(0, 360))
            Clock.schedule_interval(virus_name.update,1/30)
            self.virus_num +=1
            self.global_time = time.time()

        elif time.time() - self.global_time >7:
            virus_name = "virus"+str(self.virus_num)
            virus_name = Virus(0,100,30,"asset/yellow.png")
            self.add_vitities(virus_name)
            virus_name.velocity = Vector(4, 0).rotate(random.randint(0, 360))
            Clock.schedule_interval(virus_name.update,1/30)
            self.virus_num +=1

        elif time.time() - self.global_time >5:
            virus_name = "virus"+str(self.virus_num)
            virus_name = Virus(0,100,20,"asset/green.png")
            self.add_vitities(virus_name)
            virus_name.velocity = Vector(4, 0).rotate(random.randint(0, 360))
            Clock.schedule_interval(virus_name.update,1/30)
            self.virus_num +=1

        elif time.time() - self.global_time >0:
            print("entered")
            virus_name = "virus"+str(self.virus_num)
            virus_name = Virus(0,100,15,"asset/black.png")
            self.add_vitities(virus_name)
            virus_name.velocity = Vector(4, 0).rotate(random.randint(0, 360))
            Clock.schedule_interval(virus_name.update,1/30)
            self.virus_num +=1
            print(virus_name)
         
    def colliding_vitities(self,*largs):
        #does not matter if mutant or not. removes virus anyway
        for e in self._vitities:
            if self.collide_virus(self.player,e) == True:
                self.remove_vitities(e)
                
                if game.state == "mutant":
                    print("collide")
                    self.score.score +=1
                    self.addone.play()
                else:
                    self.remove_lives()
                    self.boom.play()

    def remove_lives(self):
        current = self.lives_remaining.pop()
        self.canvas.remove(current)
    
        if current == self.live1.image_instruction:
            self.canvas.add(Color(0, 0., 0., 1))
            self.canvas.add(self.endgame.label_instruction)
            self.bg_music.unload()
            self.bg_music = SoundLoader.load("asset/gameover.wav")
            self.bg_music.play()
            self.bg_music.volume = 1
            self.bg_music.loop = True
            app.event1.cancel()
            app.event2.cancel()
            app.event3.cancel()
            app.event4.cancel()
            app.event5.cancel()

class VirusGame(App):
    def build(self):
        #this add_healthpack is periodic to global clock.Not event triggered
        self.event1 = Clock.schedule_interval(game.add_healthpack,3)
        self.event2 = Clock.schedule_interval(game.add_virus,3)
        self.event3 = Clock.schedule_interval(game.colliding_vitities,1/60)
        self.event4 = Clock.schedule_interval(game.healthpack_check,1/30)
        self.event5 = Clock.schedule_interval(game.mutant_check,1/30)
        return game

#global var for easy access. 
game = GameMain()  
game.state = "begin"

app = VirusGame()
if __name__ == '__main__':
    app.run()