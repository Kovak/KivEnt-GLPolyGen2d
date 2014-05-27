from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Mesh, RenderContext, Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from random import randint, choice, random, randrange
from math import pi, cos, sin
import triangle
from numpy import array
from kivy.graphics.transformation import Matrix

class RegularPolygonRenderer(Widget):

    def __init__(self, **kwargs):
        self.canvas = RenderContext(use_parent_projection=True)
        self.canvas.shader.source = 'poscolorshader.glsl'
        super(RegularPolygonRenderer, self).__init__(**kwargs) 
        self.color_vertex_map = {}
        self.draw_regular_polygon((300, 200), 1, 40, (1., 1., 1., 1.),
            {
            #Enter your level widths and colors here
            1: (250., (.5, .6, 0., 1.), 0.),
            2: (10., (.2, 1., 0., 1.), 0.0),
            3: (30., (0.2, 1., 0., 0.), 0.0),  
            })


    def draw_regular_polygon(self, pos, levels, sides, middle_color,
        radius_color_dict,):
        '''
        radius_color_dict = {'level#': (r, (r,g,b,a))}
        '''
        level_colors = []
        for key in radius_color_dict:
            color = radius_color_dict[key][1]
            if color[3] != 0.0:
                level_colors.append(color)
        color_average = [0., 0., 0., 0.]
        num_colors = 0
        for color in level_colors:
            num_colors += 1
            for i in range(4):
                color_average[i] += color[i]
            
            
        print color_average

        color_vertex_map = self.color_vertex_map
        x, y = pos
        vertex_format = [
            ('vPosition', 2, 'float'),
            ('vColor', 4, 'float'),
            ]
        angle = 2 * pi / sides
        all_verts = []
        all_verts_a = all_verts.append
        color_vertex_map[pos] = middle_color
        r_total = 0
        i = 0
        for count in range(levels):
            level = i + 1
            print level
            r, color, offset = radius_color_dict[level]
            for s in range(sides):
                if offset != 0.:
                    r_off_x = randrange(-offset, offset)
                    r_off_y = randrange(-offset, offset)
                else:
                    r_off_x = 0
                    r_off_y = 0
                new_pos = (x + (r + r_total) * sin(s * angle) + r_off_x, 
                    y + (r + r_total) * cos(s * angle) + r_off_y)
                all_verts_a(new_pos)
                color_vertex_map[new_pos] = color
            r_total +=  r
            i += 1
        A = {'vertices':array(all_verts)}
        B = triangle.triangulate(A, 'cqa75YY')
        tri_indices = B['triangles']
        new_indices = []
        new_vertices = []
        tri_verts = B['vertices']
        nv_ex = new_vertices.extend
        new_ex = new_indices.extend
        for tri in tri_indices:
            new_ex((tri[0], tri[1], tri[2]))
        for tvert in tri_verts:
            t_pos = (tvert[0], tvert[1])
            new_color = (-1., -1., -1., 0.)
            if t_pos in color_vertex_map:
                new_color = color_vertex_map[t_pos]
            nv_ex(t_pos)
            nv_ex(new_color)
        with self.canvas:
            self.mesh = Mesh(
                indices=new_indices,
                vertices=new_vertices,
                fmt=vertex_format,
                source='planetgradient.png',
                mode='triangles')


class RegularPolygonApp(App):

    def build(self):
        pass

if __name__ == '__main__':
    RegularPolygonApp().run()
