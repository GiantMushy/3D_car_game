from OpenGL import GL
from Matrices import ProjectionMatrix, ModelMatrix
from Base3DObjects import *

class UI:
    def __init__(self, UI_Shader, Vehicle, Lap_counter, view_settings = {"aspect_x": 800, "aspect_y": 600, "viewport": (0,0,800,600)}):
        self.Shader = UI_Shader
        self.view_settings = view_settings
        self.Vehicle = Vehicle
        self.Lap_counter = Lap_counter

        self.modelMatrix = ModelMatrix()
        self.projection_ui = ProjectionMatrix()
        self.projection_ui.set_orthographic(0, view_settings["aspect_x"], 0, view_settings["aspect_y"], -1.0, 1.0)

        self.slowed_indicator = Square(size = 50.0, color = (1.0, 1.0, 0.0))
        self.disabled_indicator = Square(size = 50.0, color = (1.0, 0.0, 0.0))
        self.boosted_indicator = Square(size = 50.0, color = (0.0, 1.0, 0.0))
        self.lap_indicator = Hexagon(size = 30.0, color = (0.2, 0.5, 1.0))

    def draw(self):
        # Switch to ortho for 2D UI
        self.Shader.use()

        self.Shader.set_projection_view_matrix(self.projection_ui.get_matrix())

        GL.glDisable(GL.GL_DEPTH_TEST)

        # Ensure model matrix = identity for UI
        self.Shader.set_model_matrix([1,0,0,0,
                                      0,1,0,0,
                                      0,0,1,0,
                                      0,0,0,1])

        self.draw_pickups()
        self.draw_lap_counter()

        GL.glEnable(GL.GL_DEPTH_TEST)

    def draw_lap_counter(self):
        aspect_x = self.view_settings["aspect_x"]
        aspect_y = self.view_settings["aspect_y"]

        for n in range(self.Lap_counter.total_laps - self.Lap_counter.lap_counter):
            self.set_shader_and_matrix(aspect_x - 30 - (n * 40), aspect_y - 30)
            self.lap_indicator.draw(self.Shader)

    def draw_pickups(self):
        aspect_y = self.view_settings["aspect_y"]

        if self.Vehicle.slowed > 0.0:
            self.set_shader_and_matrix(50, aspect_y - 50)
            self.slowed_indicator.draw(self.Shader)

        if self.Vehicle.disabled > 0.0:
            self.set_shader_and_matrix(150, aspect_y - 50)
            self.disabled_indicator.draw(self.Shader)

        if self.Vehicle.boosted > 0.0:
            self.set_shader_and_matrix(250, aspect_y - 50)
            self.boosted_indicator.draw(self.Shader)

    def set_shader_and_matrix(self, tx, ty):
        self.modelMatrix.load_identity()
        self.modelMatrix.add_translation(tx, ty, 0.0)
        self.Shader.set_model_matrix(self.modelMatrix.matrix)

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

class Hexagon:
    def __init__(self, size = 1.0, color = (1.0, 1.0, 1.0)):
        self.size = size
        self.color = color

        half_size = size / 2.0
        quarter_size = size / 4.0
        self.positions = [
            -half_size, -quarter_size, 0.0,
            -half_size,  quarter_size, 0.0,
             0.0,       half_size,     0.0,
             half_size,  quarter_size, 0.0,
             half_size, -quarter_size, 0.0,
             0.0,      -half_size,     0.0
        ]
        self.normals = [0.0, 0.0, 1.0] * 6
        self.indices = [0,1,2, 2,3,4, 4,5,0, 0,2,4]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.positions)
        shader.set_normal_attribute(self.normals)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, self.indices)