from OpenGL import GL, error
from math import *
import sys
from Base3DObjects import *

class Shader3D:
    def __init__(self, use_stadium_lights=False):
        # Choose shader files based on lighting mode (3D vs UI)
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
            self.lightEnabledLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_light_enabled")
            
            # Material uniforms
            self.cameraPositionLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_camera_position")
            self.shininessLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_shininess")
            self.specularStrengthLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_specular_strength")

            # Moonlight Directional Light
            self.directionalLightDirLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_directional_light_direction")
            self.directionalLightColorLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_directional_light_color")
            self.directionalLightIntensityLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_directional_light_intensity")
            self.directionalLightEnabledLoc = GL.glGetUniformLocation(self.renderingProgramID, "u_directional_light_enabled")


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

    def set_all_lights(self, stadium_positions, stadium_colors, stadium_intensities, 
                       underglow_pos=None, underglow_color=(0.2, 0.6, 1.0), underglow_intensity=0.0):
        """Set all 5 lights (4 stadium + 1 underglow)"""
        if not self.use_stadium_lights:
            return
            
        # Prepare arrays for all 5 lights
        pos_array = []
        color_array = []
        intensity_array = []
        enabled_array = []
        
        # Add stadium lights (indices 0-3)
        for i in range(4):
            pos_array.extend([stadium_positions[i].x, stadium_positions[i].y, stadium_positions[i].z])
            color_array.extend([stadium_colors[i][0], stadium_colors[i][1], stadium_colors[i][2]])
            intensity_array.append(stadium_intensities[i])
            enabled_array.append(1)
        
        # Add underglow light (index 4)
        if underglow_pos:
            pos_array.extend([underglow_pos.x, underglow_pos.y, underglow_pos.z])
            color_array.extend([underglow_color[0], underglow_color[1], underglow_color[2]])
            intensity_array.append(underglow_intensity)
            enabled_array.append(1)
        else:
            pos_array.extend([0.0, 0.0, 0.0])
            color_array.extend([0.0, 0.0, 0.0])
            intensity_array.append(0.0)
            enabled_array.append(0)
        
        # Set all uniforms at once
        GL.glUniform3fv(self.lightPositionsLoc, 5, pos_array)
        GL.glUniform3fv(self.lightColorsLoc, 5, color_array)
        GL.glUniform1fv(self.lightIntensitiesLoc, 5, intensity_array)
        GL.glUniform1iv(self.lightEnabledLoc, 5, enabled_array)
        
    def set_directional_light(self, direction, color, intensity, enabled=True):
        """Set directional light (like sun/moon)"""
        if self.use_stadium_lights:
            GL.glUniform3f(self.directionalLightDirLoc, direction.x, direction.y, direction.z)
            GL.glUniform3f(self.directionalLightColorLoc, color[0], color[1], color[2])
            GL.glUniform1f(self.directionalLightIntensityLoc, intensity)
            GL.glUniform1i(self.directionalLightEnabledLoc, 1 if enabled else 0)