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
        vertices = []
        indices = []
        ie = indices.extend
        ex = vertices.extend
        #Add the center point and its color to get started
        ex(pos)
        ex(middle_color)
        all_verts = []
        all_verts_a = all_verts.append
        all_verts_a(pos)
        vert_dict = {}
        r_total = 0
        i = 0
        all_verts = []
        all_vert_a = all_verts.append
        for count in range(levels):
            
            level = i + 1
            print i, level
            vert_dict[level] = verts = []
            r, color = radius_color_dict[level]
            vert_a = verts.append
            for s in range(sides):
                vert_a((x + (r + r_total) * sin(s * angle), 
                    y + (r + r_total) * cos(s * angle)))
                all_vert_a((x + (r + r_total) * sin(s * angle), 
                    y + (r + r_total) * cos(s * angle)))
            r_total +=  r
            c = 1 #side number we are on in loop
            if level == 1:
                for each in verts:
                    ex(each)
                    ex(color)
                    if c < level*sides:
                        ie([c, 0, c+1])
                    else:
                        ie([c, 0, 1])
                    c += 1
            else:
                for each in verts:
                    ex(each)
                    ex(color)
                    offset = sides*(i-1)
                    if c < sides:
                        ie([c+sides+offset, c+sides+1+offset, c+offset, 
                            c+offset, c+1+offset, c+sides+1+offset])
                    else:
                        ie([c+sides+offset, sides+1+offset, sides+offset, 
                            sides+offset, 1+offset, sides+1+offset])
                    c += 1
            i += 1
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