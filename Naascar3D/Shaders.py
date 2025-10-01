from OpenGL import GL, error
from math import *
import sys
from Base3DObjects import *

class Shader3D:
    def __init__(self, use_stadium_lights=False):
        # Choose shader files based on lighting mode
        if use_stadium_lights:
            vert_file = "/stadium3D.vert"
            frag_file = "/stadium3D.frag"
        else:
            vert_file = "/simple3D.vert" 
            frag_file = "/simple3D.frag"
            
        vert_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + vert_file)
        GL.glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        GL.glCompileShader(vert_shader)
        result = GL.glGetShaderiv(vert_shader, GL.GL_COMPILE_STATUS)
        if (result != 1):
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(GL.glGetShaderInfoLog(vert_shader)))

        frag_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + frag_file)
        GL.glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        GL.glCompileShader(frag_shader)
        result = GL.glGetShaderiv(frag_shader, GL.GL_COMPILE_STATUS)
        if (result != 1):
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(GL.glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = GL.glCreateProgram()
        GL.glAttachShader(self.renderingProgramID, vert_shader)
        GL.glAttachShader(self.renderingProgramID, frag_shader)
        GL.glLinkProgram(self.renderingProgramID)
        result = GL.glGetProgramiv(self.renderingProgramID, GL.GL_LINK_STATUS)
        if (result != 1):
            print("Couldn't link shader program\nLink compilation Log:\n" + str(GL.glGetProgramInfoLog(self.renderingProgramID)))

        # Standard uniforms
        self.positionLoc = GL.glGetAttribLocation(self.renderingProgramID, "a_position")
        GL.glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = GL.glGetAttribLocation(self.renderingProgramID, "a_normal")
        GL.glEnableVertexAttribArray(self.normalLoc)

        self.colorLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_color")
        self.modelMatrixLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.projectionViewMatrixLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_projection_view_matrix")

        # Stadium lighting uniforms (only if using stadium lights)
        self.use_stadium_lights = use_stadium_lights
        if use_stadium_lights:
            self.lightPositionsLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_light_positions")
            self.lightColorsLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_light_colors")
            self.lightIntensitiesLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_light_intensities")

            self.lightPositionsLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_light_positions")
            self.lightColorsLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_light_colors")
            self.lightIntensitiesLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_light_intensities")
            # NEW: Material uniforms
            self.cameraPositionLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_camera_position")
            self.shininessLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_shininess")
            self.specularStrengthLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_specular_strength")


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

    def set_camera_position(self, camera_pos):
        """Set camera position for specular calculations"""
        if self.use_stadium_lights:
            GL.glUniform3f(self.cameraPositionLoc, camera_pos.x, camera_pos.y, camera_pos.z)

    def set_material_properties(self, shininess=32.0, specular_strength=0.0):
        """Set material shininess and specular strength"""
        if self.use_stadium_lights:
            GL.glUniform1f(self.shininessLoc, shininess)
            GL.glUniform1f(self.specularStrengthLoc, specular_strength)

    def set_stadium_lights(self, light_positions, light_colors, light_intensities):
        """Set the 4 stadium light parameters"""
        if not self.use_stadium_lights:
            return
            
        # Flatten position arrays for OpenGL
        pos_array = []
        for pos in light_positions:
            pos_array.extend([pos.x, pos.y, pos.z])
            
        color_array = []
        for color in light_colors:
            color_array.extend([color[0], color[1], color[2]])
        
        GL.glUniform3fv(self.lightPositionsLoc, 4, pos_array)
        GL.glUniform3fv(self.lightColorsLoc, 4, color_array) 
        GL.glUniform1fv(self.lightIntensitiesLoc, 4, light_intensities)