from classes import *

x = 0
toAdd = 0
def update(win,variables=None):
	cube.rotate([2,2,2])
	cube.scale([0.2,0.2,0.2])
	
	if win.keyboard_reader.pressed['B'] == True:
		print("B pressed")
		win.playsound("Sound-Examples/RickRoll1.wav")
	if win.keyboard_reader.pressed['A'] == True:
		print("A pressed")
	
	variables['toAdd'] += 0.01
	variables['x'] += variables['toAdd']
camera = Camera()

win = Window(displaySize=(1400,700),colour=(1,1,1))
k = KeyboardReader()
win.addKeyboardReader(k)
win.setCamera(camera)
text = Texture('testTexture.png')
cube = Object(Shapes.Cube(),[1,1,1],texture=text,Type=DRAWTYPE.SOLID)

win.addObj(cube)
var = {'x' : x, 'toAdd' : toAdd}
win.run(func=lambda: update(win,variables=var))

