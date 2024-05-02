from classes import *
from OpenGL.arrays import vbo
from OpenGLContext.arrays import *



class Shader():
	def __init__(self):
		self.Vertex_Shader = shaders.compileShader("""
			#version 120
			void main(){
				gl_Position = gl_ModelViewPojectionMatrix * gl_Vertex;
			}
		 """, GL_VERTEX_SHADER)
		self.Fragment_Shader = shaders.compileShader("""
			#version 120
			void main() {
				gl_FragColor = vec4(0,1,0,1):
			}
		 """,GL_FRAGMENT_SHADER)
		self.shader = shaders.compileProgram(self.Vertex_Shader, self.Fragment_Shader)
		self.vbo = vbo.VBO(array([
			[0,1,0],
			[-1,-1,0],
			[1,-1,0],
			[2,-1,0],
			[4,-1,0],
			[4,1,0],
			[2,-1,0],
			[4,1,0],
			[2,1,0]
		 ],'f'))
	def Render(self):
		shaders.glUseProgram(self.shader)
		try:
			self.vbo.bind()
			try:
				glDrawArrays(GL_TRIANGLES,0,9)
			finally:
				self.vbo.unbind()
				glDisableClientState(GL_VERTEX_ARRAY)
		finally:
			shaders.glUseProgram(0)
if __name__ == "__main__":
	pass
