from os import environ, remove
from os.path import dirname, join, isfile
from distutils.core import setup
from distutils.extension import Extension
try:
    from Cython.Distutils import build_ext
    have_cython = True
except ImportError:
    have_cython = False


if have_cython:
    if isfile('glpolygen2d.c'):
        remove('glpolygen2d.c')
    glpolygen2d_files = [
    'glpolygen2d.pyx',
        ]
    cmdclass = {'build_ext': build_ext}
else:
    glpolygen2d_files = [
	'glpolygen2d.c',
	]
    cmdclass = {}

ext = Extension('glpolygen2d',
    glpolygen2d_files, include_dirs=[],
    extra_compile_args=['-std=c99', '-ffast-math'])

if environ.get('READTHEDOCS', None) == 'True':
    ext.pyrex_directives = {'embedsignature': True}

setup(
    name='glpolygen2d',
    description='''A game engine for the Kivy Framework. 
        https://github.com/Kovak/glpolygen2d for more info.''',
    author='Jacob Kovac',
    author_email='kovac1066@gmail.com',
    cmdclass=cmdclass,
    ext_modules=[ext])
