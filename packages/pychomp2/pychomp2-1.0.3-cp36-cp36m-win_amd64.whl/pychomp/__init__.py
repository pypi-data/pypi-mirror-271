

""""""# start delvewheel patch
def _delvewheel_init_patch_1_1_4():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pychomp2.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pychomp2-1.0.3')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-pychomp2-1.0.3')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    ctypes.WinDLL(lib_path)


_delvewheel_init_patch_1_1_4()
del _delvewheel_init_patch_1_1_4
# end delvewheel patch

### __init__.py
### MIT LICENSE 2016 Shaun Harker
#
# Marcio Gameiro
# 2022-12-04

from pychomp._chomp import *
#from pychomp.Braids import *
from pychomp.CondensationGraph import *
from pychomp.FlowGradedComplex import *
from pychomp.TopologicalSort import *
from pychomp.DirectedAcyclicGraph import *
from pychomp.InducedSubgraph import *
from pychomp.TransitiveReduction import *
from pychomp.TransitiveClosure import *
from pychomp.Poset import *
from pychomp.StronglyConnectedComponents import *
from pychomp.DrawGradedComplex import *
from pychomp.CubicalHomology import *
from pychomp.DirectedGraph import *
