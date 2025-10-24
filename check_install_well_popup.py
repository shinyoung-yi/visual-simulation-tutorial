'''
Exactly same code as a block in `check_installed_well.ipynb` with
a different parameter value: POPUP_WINDOW = 1
'''

from typing import Union
import numpy as np
import matplotlib.pyplot as plt
import glfw
import OpenGL
import OpenGL.GL as GL
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
 
POPUP_WINDOW = 1
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
def main() -> Union[None, np.ndarray]:
 
    # initialize glfw
    if not glfw.init():
        return
    
    # https://www.reddit.com/r/opengl/comments/14oazju/version_330_is_not_supported_m1_mac/?tl=ko -->
    # https://www.glfw.org/faq.html#41---how-do-i-create-an-opengl-30-context
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3);
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3);
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE);
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE);

    if not POPUP_WINDOW:
        glfw.window_hint(glfw.VISIBLE, False)

    window = glfw.create_window(DISPLAY_WIDTH, DISPLAY_HEIGHT, "My OpenGL window", None, None)
 
    if not window:
        glfw.terminate()
        return
 
    glfw.make_context_current(window)
    #            positions        colors
    triangle = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                 0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                 0.0,  0.5, 0.0, 0.0, 0.0, 1.0]
 
    triangle = np.array(triangle, dtype = np.float32)
 
    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;
    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """
 
    fragment_shader = """
    #version 330
    in vec3 newColor;
    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """
    # https://stackoverflow.com/questions/62209242/pyopengl-test-program-getting-the-validation-failed-no-vertex-array-object-bou
    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)

    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL.GL_VERTEX_SHADER),
                                              OpenGL.GL.shaders.compileShader(fragment_shader, GL.GL_FRAGMENT_SHADER))
 
    VBO = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, VBO)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, 72, triangle, GL.GL_STATIC_DRAW)
 
    position = GL.glGetAttribLocation(shader, "position")
    GL.glVertexAttribPointer(position, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, GL.ctypes.c_void_p(0))
    GL.glEnableVertexAttribArray(position)
 
    color = GL.glGetAttribLocation(shader, "color")
    GL.glVertexAttribPointer(color, 3, GL.GL_FLOAT, GL.GL_FALSE, 24, GL.ctypes.c_void_p(12))
    GL.glEnableVertexAttribArray(color)
 
 
    GL.glUseProgram(shader)
 
    GL.glClearColor(0.2, 0.3, 0.2, 1.0)
    
    if POPUP_WINDOW:
        while not glfw.window_should_close(window):
            glfw.poll_events()
    
            GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
    
            glfw.swap_buffers(window)
        glfw.terminate()
    else:
        
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        image_buffer = GL.glReadPixels(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
        image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(DISPLAY_HEIGHT, DISPLAY_WIDTH, 3)

        glfw.destroy_window(window)
        return image
 
    
if POPUP_WINDOW:
    main()
else:
    plt.imshow(main());