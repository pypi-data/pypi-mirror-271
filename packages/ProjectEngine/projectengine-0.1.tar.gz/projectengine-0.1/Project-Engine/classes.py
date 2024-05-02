import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from objloader.objloader import *

import threading
#import winsound
#from Shaders import *

def ThreadingFunc(func):
	print("Threaded")
	#threading.Thread(target=lambda:func()).start()
	func()
class RigidBody3:
	def __init__(self):
		pass
class Render:
	VERTICIES = 1
	OBJ = 2
class DRAWTYPE:
	WIREFRAME = 1
	SOLID = 2
	#TEXTURED = 3 not yet implemented
class KeyboardReader:
	def __init__(self):
		self.win = None
		self.events = []
		self.pressed = {'A1':False,'A': False,'B': False,'C': False,'D': False,'E': False,'F': False,'G': False,'H': False,'I': False,'J': False,'K': False,'L': False,'M': False,'N': False,'O': False,'P': False,'Q': False,'R': False,'S': False,'T': False,'U': False,'V': False,'W': False,'X': False,'Y': False,'Z': False}
	def addWin(self,w):
		self.win = w
	def addEvents(self,e):
		self.events = e
	def update(self): # make this threaded
		#print("Update")
		#print(self.pressed)
		for i in self.pressed.keys():
			self.pressed[i] = False
		i = pygame.key.get_pressed()
		#print(i[pygame.K_a])
		#if True:
		#	pass
		if i[pygame.K_a] == True:
			#print("A")
			self.pressed["A"] = True
		#else:
		#	self.pressed["A"] = False
		if i[pygame.K_b]== True:
			self.pressed["B"] = True
		else:
			self.pressed["B"] = False
		if i[pygame.K_c]== True:
			self.pressed["C"] = True
		else:
			self.pressed["C"] = False
		if i[pygame.K_d]== True:
			self.pressed["D"] = True
		else:
			self.pressed["D"] = False
		if i[pygame.K_e]== True:
			self.pressed["E"] = True
		else:
			self.pressed["E"] = False
		if i[pygame.K_f]== True:
			self.pressed["F"] = True
		else:
			self.pressed["F"] = False
		if i[pygame.K_g]== True:
			self.pressed["G"] = True
		else:
			self.pressed["G"] = False
		if i[pygame.K_h]== True:
			self.pressed["H"] = True
		else:
			self.pressed["H"] = False
		if i[pygame.K_i]== True:
			self.pressed["I"] = True
		else:
			self.pressed["I"] = False
		if i[pygame.K_j]== True:
			self.pressed["J"] = True
		else:
			self.pressed["A"] = False
		if i[pygame.K_k]== True:
			self.pressed["K"] = True
		else:
			self.pressed["K"] = False
		if i[pygame.K_l]== True:
			self.pressed["L"] = True
		else:
			self.pressed["L"] = False
		if i[pygame.K_m]== True:
			self.pressed["M"] = True
		else:
			self.pressed["M"] = False
		if i[pygame.K_n]== True:
			self.pressed["N"] = True
		else:
			self.pressed["N"] = False
		if i[pygame.K_o]== True:
			self.pressed["O"] = True
		else:
			self.pressed["O"] = False
		if i[pygame.K_p]== True:
			self.pressed["P"] = True
		else:
			self.pressed["P"] = False
		if i[pygame.K_q]== True:
			self.pressed["Q"] = True
		else:
			self.pressed["Q"] = False
		if i[pygame.K_r]== True:
			self.pressed["R"] = True
		else:
			self.pressed["R"] = False
		if i[pygame.K_s]== True:
			self.pressed["S"] = True
		else:
			self.pressed["S"] = False
		if i[pygame.K_t]== True:
			self.pressed["T"] = True
		else:
			self.pressed["T"] = False
		if i[pygame.K_u]== True:
			self.pressed["U"] = True
		else:
			self.pressed["U"] = False
		if i[pygame.K_v]== True:
			self.pressed["V"] = True
		else:
			self.pressed["V"] = False
		if i[pygame.K_w]== True:
			self.pressed["W"] = True
		else:
			self.pressed["W"] = False
		if i[pygame.K_x]== True:
			self.pressed["X"] = True
		else:
			self.pressed["X"] = False
		if i[pygame.K_y]== True:
			self.pressed["Y"] = True
		else:
			self.pressed["Y"] = False
		if i[pygame.K_z]== True:
			self.pressed["Z"] = True
		else:
			self.pressed["Z"] = False
		'''for i in self.events:
			if i.type == pygame.KEYDOWN:
				#print(i.key)
				#print(pygame.K_a)
				if i.key == pygame.K_a:
					self.pressed["A"] = True
				if i.key == pygame.K_b:
					self.pressed["B"] = True
				if i.key == pygame.K_c:
					self.pressed["C"] = True
				if i.key == pygame.K_d:
					self.pressed["D"] = True
				if i.key == pygame.K_e:
					self.pressed["E"] = True
				if i.key == pygame.K_f:
					self.pressed["F"] = True
				if i.key == pygame.K_g:
					self.pressed["G"] = True
				if i.key == pygame.K_h:
					self.pressed["H"] = True
				if i.key == pygame.K_i:
					self.pressed["I"] = True
				if i.key == pygame.K_j:
					self.pressed["J"] = True
				if i.key == pygame.K_k:
					self.pressed["K"] = True
				if i.key == pygame.K_l:
					self.pressed["L"] = True
				if i.key == pygame.K_m:
					self.pressed["M"] = True
				if i.key == pygame.K_n:
					self.pressed["N"] = True
				if i.key == pygame.K_o:
					self.pressed["O"] = True
				if i.key == pygame.K_p:
					self.pressed["P"] = True
				if i.key == pygame.K_q:
					self.pressed["Q"] = True
				if i.key == pygame.K_r:
					self.pressed["R"] = True
				if i.key == pygame.K_s:
					self.pressed["S"] = True
				if i.key == pygame.K_t:
					self.pressed["T"] = True
				if i.key == pygame.K_u:
					self.pressed["U"] = True
				if i.key == pygame.K_v:
					self.pressed["V"] = True
				if i.key == pygame.K_w:
					self.pressed["W"] = True
				if i.key == pygame.K_x:
					self.pressed["X"] = True
				if i.key == pygame.K_y:
					self.pressed["Y"] = True
				if i.key == pygame.K_z:
					self.pressed["Z"] = True
			if i.type == pygame.KEYUP:
				if i.key == pygame.K_a:
					self.pressed["A"] = False
				if i.key == pygame.K_b:
					self.pressed["B"] = False
				if i.key == pygame.K_c:
					self.pressed["C"] = False
				if i.key == pygame.K_d:
					self.pressed["D"] = False
				if i.key == pygame.K_e:
					self.pressed["E"] = False
				if i.key == pygame.K_f:
					self.pressed["F"] = False
				if i.key == pygame.K_g:
					self.pressed["G"] = False
				if i.key == pygame.K_h:
					self.pressed["H"] = False
				if i.key == pygame.K_i:
					self.pressed["I"] = False
				if i.key == pygame.K_j:
					self.pressed["J"] = False
				if i.key == pygame.K_k:
					self.pressed["K"] = False
				if i.key == pygame.K_l:
					self.pressed["L"] = False
				if i.key == pygame.K_m:
					self.pressed["M"] = False
				if i.key == pygame.K_n:
					self.pressed["N"] = False
				if i.key == pygame.K_o:
					self.pressed["O"] = False
				if i.key == pygame.K_p:
					self.pressed["P"] = False
				if i.key == pygame.K_q:
					self.pressed["Q"] = False
				if i.key == pygame.K_r:
					self.pressed["R"] = False
				if i.key == pygame.K_s:
					self.pressed["S"] = False
				if i.key == pygame.K_t:
					self.pressed["T"] = False
				if i.key == pygame.K_u:
					self.pressed["U"] = False
				if i.key == pygame.K_v:
					self.pressed["V"] = False
				if i.key == pygame.K_w:
					self.pressed["W"] = False
				if i.key == pygame.K_x:
					self.pressed["X"] = False
				if i.key == pygame.K_y:
					self.pressed["Y"] = False
				if i.key == pygame.K_z:
					self.pressed["Z"] = False'''
class Shapes:
	def Cube():
		verticies = ((1, -1, -1),(1, 1, -1),(-1, 1, -1),(-1, -1, -1),(1, -1, 1),(1, 1, 1),(-1, -1, 1),(-1, 1, 1))
		edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))
		triangles = ((0,0,0),(0,1,0),(1,0,0),(0,1,0),(1,1,0),(1,0,0))
		#vao = glGenVertexArrays(1)
		#glBindVertexArray(self.vao)
		#vbo = glGenBuffers(1)
		#glBindBuffer(GL_ARRAY_BUFFER,vbo)
		#glBufferData(GL_ARRAY_BUFFER,verticies.nbytes,GL_STATIC_DRAW)
		#glEnableVertexAttribArray(0)
		#glVertexAttribPointer(0,3,GL_FLOAT,GL_FALSE,32, ctypes.c_void_p(0))
		#glEnableVertexAttribArray(1)
		#glVertexAttribPointer(2,3,GL_FLOAT,GL_FALSE,32, ctypes.c_void_p(12))
		#glEnableVertexAttribArray(2)
		#glVertexAttribPointer(2,2,GL_FLOAT,GL_FALSE,32, ctypes.c_void_p(20))
		
		return {"VERT":verticies, "EDGE": edges, "TRI": triangles}
	def Triangle_Square():
		verticies = (
			(1,0,1),(-1,0,-1),(-1,0,1),(1,0,-1),(0,1,0)
		)
class Object:
	def __init__(self,verts,shape,colour=[0,0,0],alpha=255,texture=None, Type=DRAWTYPE.WIREFRAME):
		self.verts = verts
		self.texture = texture
		self.shape = shape
		self.rotation = [0,0,0]
		self.active = True
		self.move = [0,0,0]
		self.colour = colour
		self.alpha = alpha
		self.type = Type
		self.debug = False
		#self.shader = Shader()
		#glUseProgram(self.shader)
		#glUniformli(glGetUniformLocation(self.shader,"imageTexture"),0)
		
	def rotate(self,vector):
		self.rotation[0] += vector[0]
		self.rotation[1] += vector[1]
		self.rotation[2] += vector[2]
		for i in self.rotation:
			if i >= 360:
				i = 0
	def setColour(self,colour,alpha=255):
		self.colour = colour
		self.alpha = alpha
	def scale(self,by):
		self.verts["VERT"] = UsefulFunctions.scaleVerticies(by,self.verts["VERT"])
	def transform(self,vector):
		self.move[0] += vector[0]
		self.move[1] += vector[1]
		self.move[2]= vector[2]
	def render(self,cam):
		glTranslatef(-cam.location[0],-cam.location[1],-cam.location[2])
		glPushMatrix()
		#self.texture.use()
		#if self.texture:
		#	#print("HERE")
		#	glEnable(GL_TEXTURE_2D)
		#	glBindTexture(GL_TEXTURE_2D,self.texture.texture)
		glRotatef(self.rotation[0],1,0,0)
		glRotatef(self.rotation[1],0,1,0)
		glRotatef(self.rotation[2],0,0,1)
		glTranslatef(self.move[0],self.move[1],self.move[2])
		if self.type == DRAWTYPE.WIREFRAME:
			glBegin(GL_LINES)
			x = UsefulFunctions.scaleVerticies(self.shape,self.verts["VERT"])
			for edge in self.verts["EDGE"]:
				if self.debug == True: print(edge)
				for vertex in edge:
					if self.debug == True: print(vertex)
					glVertex3fv(x[vertex])
		elif self.type == DRAWTYPE.SOLID:
			glBegin(GL_TRIANGLES)
			x = UsefulFunctions.scaleVerticies(self.shape,self.verts["TRI"])
			print(x)
			if self.debug == True: print(x)
			for edge in self.verts["TRI"]:
				if self.debug == True: print(edge)
				glVertex3f(edge[0],edge[1],edge[2])
				for vertex in edge:
					if self.debug == True: print(vertex)
					
					#glVertex3fv(x[vertex])
					#glVertex3f(vertex)
		else:
			glBegin(GL_LINES)
		
		glColor(round(self.colour[0]/255,2),round(self.colour[1]/255,2),round(self.colour[2]/255),round(self.alpha/255,2))
		glEnd()
		glDisable(GL_TEXTURE_2D)
		glPopMatrix()
		glTranslatef(cam.location[0],cam.location[1],cam.location[2])
	def toggleActive(self,to=None):
		if to:
			self.active = to
			return
		self.active = not(self.active)
class UsefulFunctions:
	def scaleVerticies(scale,verticies, triangles=True):  # Take into Classes
		'''if triangles == True:
			pass
			x = []
			for i in verticies:
				toAdd = []
				y = 0
				#((0,0,0),(0,1,0),(1,0,0),(0,1,0),(1,1,0),(1,0,0))
				for l in i:
					if y == 0 and l == 0:
						toAdd.append()
						'''
		x = []
		for i in verticies:
			toAdd = []
			y = 0
			for l in i:
				#print(l)
				if l == 0:
					toAdd.append(0)#]
				if y == 0 and l > 0:
					toAdd.append(l+scale[0])
				if y == 1 and l > 0:
					toAdd.append(l+scale[1])
				if y == 2 and l > 0:
					toAdd.append(l+scale[2])
					#print("Z +")
				if y == 0 and l < 0:
					toAdd.append(l-scale[0])
				if y == 1 and l < 0:
					toAdd.append(l-scale[1])
				if y == 2 and l < 0:
					toAdd.append(l-scale[2])
					#print("Z -")
				if y >= 2:
					y = 0
				y += 1          
			toAdd = tuple(toAdd)
			x.append(toAdd)
		return tuple(x)
	def render(verticies,shape=None,RenderPipeLine=Render.VERTICIES):
		if RenderPipeLine == Render.VERTICIES:
			glBegin(GL_LINES)
			x = UsefulFunctions.scaleVerticies(shape,verticies["VERT"])
			for edge in shape["EDGE"]:
				#print(edge)
				for vertex in edge:
					#print(vertex)
					glVertex3fv(x[vertex])
			glEnd()
		if RenderPipeLine == Render.OBJ:
			s = OBJ(verticies)
			glPushMatrix()
			s.render()
			glPopMatrix()
class Camera:
	def __init__(self):
		self.location = [0,0,0]
	def move(self,vector):
		#glTranslatef(vector[0],vector[1],vector[2])
		self.location[0] += vector[0]
		self.location[1] += vector[1]
		self.location[2] += vector[2]
		glTranslatef(self.location[0],self.location[1],self.location[2])
	def setPosition(self,vector):
		self.location = vector
	def rotateself(self,vector):
		#glRotatef(vector[0],1.0,0.0,0.0)
		#glRotatef(vector[1],0.0,1.0,0.0)
		#glRotatef(vector[2],0.0,0.0,1.0)
		pass
class Texture:
	def __init__(self, path):
		self.texture = glGenTextures(1) # Generate Texture
		glBindTexture(GL_TEXTURE_2D, self.texture) # Bind Texture to GL
		#Add parameters
		glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		image = pygame.image.load(path).convert()
		image_width, image_height = image.get_rect().size
		image_data = pygame.image.tostring(image,"RGBA")
		glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,image_width,image_height,0,GL_RGBA,GL_UNSIGNED_BYTE,image_data)
		glGenerateMipmap(GL_TEXTURE_2D)
	def use(self):
		glActiveTexture(GL_TEXTURE0)
		glBindTexture(GL_TEXTURE_2D, self.texture)
		
	def destroy(self):
		glDeleteTextures(1,(self.texture,))
class Window:
	def __init__(self,displaySize=(800,600),fpsgoal=60,colour=(255,255,255)):
		pygame.init()
		pygame.mixer.init()
		self.display = pygame.display.set_mode(displaySize,DOUBLEBUF|OPENGL)
		glClearColor(colour[0],colour[1],colour[2],255)
		self.clock = pygame.time.Clock()
		gluPerspective(45,(displaySize[0]/displaySize[1]),0.1,75)
		glTranslatef(0.0,0.0,-50.0)
		self.isRunning = False
		self.objects = []
		self.fpsgoal = fpsgoal
		self.clock = pygame.time.Clock()
		self.camera = None
		self.keyboard_reader = None
	def addKeyboardReader(self,k):
		self.keyboard_reader = k
		self.keyboard_reader.addWin(self)
	def playsound(self,filename):
		sound = pygame.mixer.Sound(filename)
		sound.play()
	def run(self,func=None):
		self.isRunning = True
		while 1:
			if self.keyboard_reader:
				threading.Thread(target=self.keyboard_reader.update).start()
				#self.keyboard_reader.update()
				self.keyboard_reader.addEvents(pygame.event.get())
				#print(pygame.key.get_pressed())
			for event in pygame.event.get():
				#if self.keyboard_reader:
				#	
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
			threading.Thread(target=func).start()
			#threading.Thread(target=self.draw,args=(self.camera)).start()
			self.draw(self.camera)
			
			self.clock.tick(self.fpsgoal)
			pygame.display.flip()
			pygame.time.wait(10)
	def draw(self,cam):
		#glTranslatef(-self.camera.location[0],-self.camera.location[1],-self.camera.location[2])
		for i in self.objects:
			if i.active == True:
				i.render(cam)
		#glTranslatef(self.camera.location[0],self.camera.location[1],self.camera.location[2])
	def addObj(self,obj):
		self.objects.append(obj)
	def setCamera(self,c):
		self.camera = c
if __name__ == "__main__":
	pygame.init()
	display = (800,600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	clock = pygame.time.Clock()
	gluPerspective(45, (display[0]/display[1]), 0.1, 75)
	glTranslatef(0.0,0.0, -50)
	cube = Object(verts=Shapes.Cube(),shape=[10,10,10])
	c = Object(verts=Shapes.Cube(),shape=[1,1,1])
	cam = Camera()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		#Stuff Here
		#UsefulFunctions.render(Shapes.Cube(),shape=[10,10,10],RenderPipeLine=Render.VERTICIES)
		
		cube.render(cam)
		c.render(cam)
		cube.rotate([2,2,2])
		c.rotate([-2,-2,-2])
		#cube.scale([0.1,0.1,0.1])
		clock.tick(120)
		pygame.display.flip()
		pygame.time.wait(10)
		
		#import math
		#print(math.pi)
		#pi_value=math.pi
		#num=round(pi_value)
		#print(num)
		
