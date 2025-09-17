
from OpenGL import GL, error
from math import * # trigonometry

import sys

from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        GL.glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        GL.glCompileShader(vert_shader)
        result = GL.glGetShaderiv(vert_shader, GL.GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(GL.glGetShaderInfoLog(vert_shader)))

        frag_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        GL.glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        GL.glCompileShader(frag_shader)
        result = GL.glGetShaderiv(frag_shader, GL.GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(GL.glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = GL.glCreateProgram()
        GL.glAttachShader(self.renderingProgramID, vert_shader)
        GL.glAttachShader(self.renderingProgramID, frag_shader)
        GL.glLinkProgram(self.renderingProgramID)
        result = GL.glGetProgramiv(self.renderingProgramID, GL.GL_LINK_STATUS)
        if (result != 1): # shaders didn't link
            print("Couldn't link shader program\nLink compilation Log:\n" + str(GL.glGetProgramInfoLog(self.renderingProgramID)))

        self.positionLoc = GL.glGetAttribLocation(self.renderingProgramID, "a_position")
        GL.glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = GL.glGetAttribLocation(self.renderingProgramID, "a_normal")
        GL.glEnableVertexAttribArray(self.normalLoc)

        self.colorLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_color")

        self.modelMatrixLoc	= GL.glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.projectionViewMatrixLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_projection_view_matrix")


    def use(self):
        try:
            GL.glUseProgram(self.renderingProgramID)   
        except error.GLError:
            print(GL.glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        GL.glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_projection_view_matrix(self, matrix_array):
        GL.glUniformMatrix4fv(self.projectionViewMatrixLoc, 1, True, matrix_array)

    def set_position_attribute(self, vertex_array):
        GL.glVertexAttribPointer(self.positionLoc, 3, GL.GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, normal_array):
        GL.glVertexAttribPointer(self.normalLoc, 3, GL.GL_FLOAT, True, 0, normal_array)

    def set_solid_color(self, r, g, b, a = 1.0):
        GL.glUniform4f(self.colorLoc, r, g, b, a)