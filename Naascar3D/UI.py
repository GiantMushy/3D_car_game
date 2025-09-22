from OpenGL import GL
from Matrices import ProjectionMatrix, ModelMatrix
from Base3DObjects import *
from PixelText import *

class UI:
    def __init__(self, shader, vehicle, view_settings = {"aspect_x": 800, "aspect_y": 600, "viewport": (0,0,800,600)}):
        self.shader = shader
        self.view_settings = view_settings
        self.vehicle = vehicle

        self.modelMatrix = ModelMatrix()
        self.projection_ui = ProjectionMatrix()
        self.projection_ui.set_orthographic(0, view_settings["aspect_x"], 0, view_settings["aspect_y"], -1.0, 1.0)

        self.slowed_indicator = Square(size = 50.0, color = (1.0, 1.0, 0.0))
        self.disabled_indicator = Square(size = 50.0, color = (1.0, 0.0, 0.0))
        self.boosted_indicator = Square(size = 50.0, color = (0.0, 1.0, 0.0))

    def draw(self):
        # Switch to ortho for 2D UI
        self.shader.set_projection_view_matrix(self.projection_ui.get_matrix())

        GL.glDisable(GL.GL_DEPTH_TEST)

        # Ensure model matrix = identity for UI
        self.shader.set_model_matrix([1,0,0,0,
                                      0,1,0,0,
                                      0,0,1,0,
                                      0,0,0,1])
        
        if self.vehicle.slowed > 0.0:
            self.set_shader_and_matrix(50, self.view_settings["aspect_y"] - 50)
            self.slowed_indicator.draw(self.shader)

        if self.vehicle.disabled > 0.0:
            self.set_shader_and_matrix(150, self.view_settings["aspect_y"] - 50)
            self.disabled_indicator.draw(self.shader)

        if self.vehicle.boosted > 0.0:
            self.set_shader_and_matrix(250, self.view_settings["aspect_y"] - 50)
            self.boosted_indicator.draw(self.shader)

        GL.glEnable(GL.GL_DEPTH_TEST)

    def set_shader_and_matrix(self, tx, ty):
        self.modelMatrix.load_identity()
        self.modelMatrix.add_translation(tx, ty, 0.0)
        self.shader.set_model_matrix(self.modelMatrix.matrix)



# ----------------------------------------------------------------------------------------------------
# ----------------------------------------2D UI Objects-----------------------------------------------
# ----------------------------------------------------------------------------------------------------

class Square:
    def __init__(self, size = 1.0, color = (1.0, 1.0, 1.0)):
        self.size = size
        self.color = color

        half_size = size / 2.0
        self.positions = [
            -half_size, -half_size, 0.0,
            -half_size,  half_size, 0.0,
             half_size,  half_size, 0.0,
             half_size, -half_size, 0.0
        ]
        self.normals = [0.0, 0.0, 1.0] * 4
        self.indices = [0,1,2, 2,3,0]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.positions)
        shader.set_normal_attribute(self.normals)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, self.indices)
        
