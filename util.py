import sys, platform
import numpy as np
import open3d as o3d

# Used in later version? maybe?
# import vispy as vp
# import mitsuba as mi

def sys_info():
    return "\n".join([
        platform.platform(), sys.platform,
        "Python " + str(sys.version).replace('\n', ' '),
        f"{np.__version__ = }",
        f"{o3d.__version__ = }",
        # f"{vp.__version__ = }",
        # f"{mi.__version__ = }"
    ])

'''
########################################
# >>>       Math Functions         <<< #
########################################

'''
def rotx(radians: float) -> np.ndarray[np.float32]:
    return np.array([[1., 0., 0., 0.],
                     [0., np.cos(radians), -np.sin(radians), 0.],
                     [0., np.sin(radians), np.cos(radians), 0.],
                     [0., 0., 0., 1.]], dtype=np.float32)

def roty(radians: float) -> np.ndarray[np.float32]:
    return np.array([[np.cos(radians), 0., np.sin(radians), 0.],
                     [0., 1., 0., 0.],
                     [-np.sin(radians), 0., np.cos(radians), 0.],
                     [0., 0., 0., 1.]], dtype=np.float32)

def rotz(radians: float) -> np.ndarray[np.float32]:
    return np.array([[np.cos(radians), -np.sin(radians), 0., 0.],
                     [np.sin(radians), np.cos(radians), 0., 0.],
                     [0., 0., 1., 0.],
                     [0., 0., 0., 1.]], dtype=np.float32)

def translate(vec) -> np.ndarray[np.float32]:
    vec = np.asarray(vec)
    T = np.eye(4, dtype=np.float32)
    T[:3, 3] = vec
    return T