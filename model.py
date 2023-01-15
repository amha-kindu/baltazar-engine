import numpy as np
import glm
from abc import abstractmethod, ABC



class Model(ABC):
    @abstractmethod
    def get_model_matrix(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self):
        pass
    
    @abstractmethod
    def dispose(self):
        pass

    @abstractmethod
    def get_vao(self):
        pass

    @abstractmethod
    def get_vertex_data(self):
        pass

    @abstractmethod
    def get_vbo(self):
        pass

    @abstractmethod
    def get_shader_program(self, shader_name):
        pass


class Cube(Model):
    def __init__(self, app) -> None:
        self.app = app
        self.ctx = app.context
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()

        self.on_init()

    def on_init(self):
        self.shader_program['m_proj'].write(self.app.camera.proj_mat)
        self.shader_program['m_view'].write(self.app.camera.view_mat)
        self.shader_program['m_model'].write(self.m_model)

    def get_model_matrix(self):
        m_model = glm.mat4()


        return m_model

    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0, 1, 0))
        self.shader_program['m_model'].write(m_model)

    def render(self):
        self.update()
        self.vao.render()

    def dispose(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
    
    def get_vao(self):
        return self.ctx.vertex_array(
            self.shader_program, 
            [
                (self.vbo, '3f', 'in_position')
            ]
        )

    def get_vertex_data(self):
        vertices = [
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
            (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]
        return self.get_data(vertices, indices)
    
    @staticmethod
    def get_data(vertices, indices):
        return np.array([
            vertices[ind] for triangle in indices for ind in triangle
        ], dtype=np.float32)

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        return self.ctx.buffer(vertex_data)

    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        return self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
