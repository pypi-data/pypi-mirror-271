from setuptools import Extension, setup

ext = Extension(
    name='pylammpstrj',
    include_dirs=['include'],
    sources=[
        'src/atom.c',
        'src/bond.c',
        'src/box.c',
        'src/property.c',
        'src/read.c',
        'src/select.c',
        'src/skip.c',
        'src/trajectory.c',
        'src/trajectoryfile.c',
        'src/utils.c',
        'src/pyatom.c',
        'src/pybond.c',
        'src/pybox.c',
        'src/pylammpstrjmodule.c',
        'src/pytrajectory.c',
        'src/pytrajectoryfile.c',
        'src/pyutils.c'
    ],
    extra_compile_args=[
        '-g',
        '-O3',
        '-Wall',
        '-Wextra',
        '-fPIC',
        '-fopenmp'
    ],
    extra_link_args=['-fopenmp']
)

setup(ext_modules=[ext])
