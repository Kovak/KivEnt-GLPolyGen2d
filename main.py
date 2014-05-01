from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Mesh, RenderContext, Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from random import randint, choice
from math import pi, cos, sin
import triangle
from numpy import array
from kivy.graphics.transformation import Matrix

class RegularPolygonRenderer(Widget):

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'poscolorshader.glsl'
        super(RegularPolygonRenderer, self).__init__(**kwargs) 
        
        self.draw_regular_polygon((400, 300), 2, 10, (1., 0., 0., 1.),
            {
            #Enter your level widths and colors here
            1: (50, (1., 0., 0., 1.)),
            2: (20, (1., 0., 0., 1.)),  
            })


    def draw_regular_polygon(self, pos, levels, sides, middle_color,
        radius_color_dict,):
        '''
        radius_color_dict = {'level#': (r, (r,g,b,a))}
        '''
        x, y = pos
        vertex_format = [
            ('vPosition', 2, 'float'),
            ('vColor', 4, 'float'),
            ]
        angle = 2 * pi / sides
        all_verts = []
        all_verts_a = all_verts.append
        all_verts_a(pos)
        r_total = 0
        i = 0
        for count in range(levels):
            level = i + 1
            r, color = radius_color_dict[level]
            for s in range(sides):
                all_verts_a((x + (r + r_total) * sin(s * angle), 
                    y + (r + r_total) * cos(s * angle)))
            r_total +=  r
        A = {'vertices':array(all_verts)}
        B = triangle.triangulate(A, 'qa200.')
        tri_indices = B['triangles']
        new_indices = []
        new_vertices = []
        tri_verts = B['vertices']
        nv_ex = new_vertices.extend
        new_ex = new_indices.extend
        color_choices = [(.5, 1., 0., 1.), (0., .3, .8, 1.)]
        for tri in tri_indices:
            new_ex((tri[0], tri[1], tri[2]))
        for tvert in tri_verts:
            nv_ex((tvert[0], tvert[1]))
            nv_ex(choice(color_choices))
        with self.canvas:
            self.mesh = Mesh(
                indices=new_indices,
                vertices=new_vertices,
                fmt=vertex_format,
                mode='triangles')


class RegularPolygonApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    RegularPolygonApp().run()
