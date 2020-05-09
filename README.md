# My Game
In this tumultuous time of Covid, we have to be socially reponsible and avoid catching the virus. Hence my theme : simple 2D single player game on avoiding virus

# How to Play
Control the human with WASD for up,left,down,right respectively. 
Avoid the viruses. 
Getting 1 virus means dropping 1 life.
Eating the health pack and then hitting a virus adds 1 point
Obj is to get the most point that you can

# Code explanation
I will explain each class in the code. I tried my best to make the game modular without having multiple files. 

## MyKeyboardListener(Widget)
this class extends the Widget class and the code is pretty standard in python kivy. 
Main thing that I modified is adding a **self.keyset = set()**. When a key is pressed, the keycode is added to the set. when key is released, the keycode is removed. When i later call this class and check correspondingly what is in the keyset and update the graphics accordingly. 

## TextImage() 
This is a special class I created to add label and images on screen in a more painless way. 

## Score()
This is a class to keep track of my scores. It takes x,y as cordinates.
The displaying part works similar to TextImage()
There is a getter and setter for scores.

## Entity()
This is a class that defines all the basic moving parts of the game, both the player and virus. 
It imagines everything is a circle, hence it takes x,y,r,src as args.
r is radius
src is source
there is getter and setter for each of them

## Virus(Entity)
This class extends the entity class. It defines how the virus should move by using kivy vectors for velocity

## Player(Entitiy)
This class extends entity as well. It basically checks if WASD is in the keyset and moves accordingly. It also checks for window bounds so the player does not go out 

## Healthpack(Virus)
Its basically the same as virus. That's why I extended from virus but used a different name so it won't get confused by reader

## GameMain(Widget)
Main logic. There's check entity and vitities. vitities stand for virus entity. Reason is entities are sets while vitities are lists. 

## VirusGame(app)
Where all the scheduling clock events are. 
