from settings import *
import moderngl as mgl
import pygame as pg
import sys
from shader_program import ShaderProgram
from scene import Scene
import player
from textures import Textures
from camera import Camera
import world
import subprocess
import os
import socket
import threading
######import Launcher######
import time


fps = 200
frame_duration = 1.0 / fps

SocketMultiPlayer = False

#def start_launcher():
    # Lance le script du launcher
    #process = subprocess.Popen(['python', 'Menu/Launcher.py'])
    #process.wait()


####  VoxelEngine  ######################################################################
class VoxelEngine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES)
        #pg.display.set_mode((0, 0), pg.FULLSCREEN) 
        pg.display.set_mode((1920, 1080),flags=pg.OPENGL | pg.DOUBLEBUF)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        pg.display.set_icon(pg.image.load('icon.ico'))

        self.is_running = True
        self.on_init()

    def on_init(self):
        self.textures = Textures(self)
        self.player = player.Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)


    def update(self):
        self.player.update(pg)
        self.shader_program.update()
        self.scene.update()

        pg.display.set_caption(("BlockyPy ||| FPS : "+str(math.floor(self.clock.get_fps()))))
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001

    def render(self):
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        self.player.render()
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            self.player.handle_event(event=event, pg=pg)
    #def update_player():
    #    global x_pos
    #    global y_pos
    #    global z_pos
    #    position = Camera.get_pos()
    #    x_pos = position[0]
    #    y_pos = position[1]
    #    z_pos = position[2]-
    def run(self):
        while self.is_running:
            start_time = time.time()
            self.handle_events()
            self.update()
            self.render()
            #self.update_player()
            #Socket_game.print_data()
            elapsed_time = time.time() - start_time
            time.sleep(max(0, frame_duration - elapsed_time))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        pg.quit()
        sys.exit()
    

####  VoxelEngine  ######################################################################

#### General ############################################################################

def launch_game():
    app = VoxelEngine()
    app.run()

#### General ########################################################################



#### Multiplayers Sockets ###############################################################
'''''''''
class Socket_game:
    def print_data():
        Name=values[0]
        equiped_weapon=values[1]
        #x_pos=values[2]
        #y_pos=values[3]
        #z_pos=values[4]
        x_cam= values[5]
        y_cam=values[6]
        Score=values[7]
        IsAlive=values[8]
        IsShooting=values[9]
        os.system("cls")
        print (f"Name: {Name}")
        print (f"Equiped Weapon: {equiped_weapon}")
        #print (f"X: {x_pos}")
        #print (f"Y: {y_pos}")q
        #print (f"Z: {z_pos}")
        print (f"X Cam: {x_cam}")
        print (f"Y Cam: {y_cam}")
        print (f"Score: {Score}")
        print (f"Is alive: {IsAlive}")
        print (f"Is Shooting: {IsShooting}")
        
    def receive_data():
        while True:
            try:
                # Recevoir des donnees du serveur GWA GWA GWA PE-PE-PEWW NICO ET THOTHO LES BOSS DE LA PROGRAMMATION ENFAITE 😝
                ReceivedData = client_socket.recv(1024).decode()
                print(f"Received Data: {ReceivedData}")
                os.system("cls")
                global values
                values = ReceivedData.split('¤')[1:]
                
    
            except Exception as e:
                print(e)
                break


    def send_data():
        while True:
            # Envoyer les donnees au serveur en boucle
            DataToSend = ""
            data_list = [                
                player.Name, 
                player.equiped_weapon, 
                #x_pos,
                #y_pos,
                #z_pos,
                player.x_cam, 
                player.y_cam,
                player.Score, 
                player.IsAlive, 
                player.IsShooting 
                ]
            
            for i in data_list:
                DataToSend += str("¤"+str(i))
            client_socket.sendall(DataToSend.encode()) # (Datatosend.encode()) OK but (Datatosend).encode() not OK
            print(DataToSend)
'''''

#### Multiplayers Sockets ###############################################################
if __name__ == "__main__":
    #VoxelEngine.update_player()
    #client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCKET ITEM
    print("Cree Thomas M. et Nicolas P. depuis la France avec 9 386km de distance mdr!")  # print Creds
    #print("IP: localhost",55555)
    #client_socket.connect(('localhost', 55555))
    #thread_recv = threading.Thread(target=Socket_game.receive_data)
    #thread_send = threading.Thread(target=Socket_game.send_data)
    #thread_recv.start()
    #thread_send.start()
    launch_game()