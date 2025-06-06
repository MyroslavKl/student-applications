//
// Created by anmode on 10.08.2024.
//

#ifndef FEM_ENGINE_MOUSE_H
#define FEM_ENGINE_MOUSE_H

#include <GLFW/glfw3.h>

/*
    mouse class to handle mouse callbacks
*/

class Mouse {
public:
    static void cursorPosCallback(GLFWwindow* window, double _x, double _y);
    static void mouseButtonCallback(GLFWwindow* window, int button, int action, int mods);
    static void mouseWheelCallback(GLFWwindow* window, double dx, double dy);

    static double getMouseX();
    static double getMouseY();

    static double getDX();
    static double getDY();

    static double getScrollDX();
    static double getScrollDY();

    static bool button(int button);
    static bool buttonChanged(int button);
    static bool buttonWentUp(int button);
    static bool buttonWentDown(int button);

private:
    static double x;
    static double y;

    static double lastX;
    static double lastY;

    static double dx;
    static double dy;

    static double scrollDx;
    static double scrollDy;

    static bool firstMouse;

    static bool buttons[GLFW_MOUSE_BUTTON_LAST+1];
    static bool buttonsChanged[GLFW_MOUSE_BUTTON_LAST+1];
};

#endif //FEM_ENGINE_MOUSE_H
