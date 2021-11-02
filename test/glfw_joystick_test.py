import glfw
from ctypes import byref, CDLL, POINTER, c_float, c_int

def main():
    # Initialize the library
    if not glfw.init():
        return

    JOYSTICK_NUMBER = 0
    joystick_present = glfw.joystick_present(JOYSTICK_NUMBER)
    print(u"joystick_present %s", joystick_present)
    joystick_name = glfw.get_joystick_name(0)
    print(u"joystick_name %s", joystick_present)
    joystick_axis_0 = glfw.get_joystick_axes(0)
    print(u"joystick_axis_0 %s", joystick_axis_0)
    joystick_axis_1 = glfw.get_joystick_axes(1)
    print(u"joystick_axis_1 %s", joystick_axis_1)
    joystick_axis_2 = glfw.get_joystick_axes(2)
    print(u"joystick_axis_2 %s", joystick_axis_2)
    joystick_axis_3 = glfw.get_joystick_axes(3)
    print(u"joystick_axis_3 %s", joystick_axis_3)
    joystick_axis_4 = glfw.get_joystick_axes(4)
    print(u"joystick_axis_4 %s", joystick_axis_4)
    joystick_axis_5 = glfw.get_joystick_axes(5)
    print(u"joystick_axis_5 %s", joystick_axis_5)


    if joystick_present == 1:
        cnt = c_int(0) # must be of type c_int!
        t, count = glfw.get_joystick_axes(JOYSTICK_NUMBER)
       





    glfw.terminate()

if __name__ == "__main__":
    main()