#include "Header.h"

#include <GLFW/glfw3.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <iostream>

#define ECG_DATA_BUFFER_SIZE  1000
float g_ratio;

typedef struct
{
    GLfloat x, y, z; // position
    GLfloat r, g, b, a; // color
} Vertex;

typedef struct
{
    GLfloat x, y, z;
} Data;


void DrawLineSegment(Vertex a_vertex1, Vertex a_vertex2, GLfloat a_width = 1.0f)
{
    glLineWidth(a_width);
    glBegin(GL_LINES);
    glColor4f(a_vertex1.r, a_vertex1.g, a_vertex1.b, a_vertex1.a);
    glVertex3f(a_vertex1.x, a_vertex1.y, a_vertex1.z);
    glColor4f(a_vertex2.r, a_vertex2.g, a_vertex2.b, a_vertex2.a);
    glVertex3f(a_vertex2.x, a_vertex2.y, a_vertex2.z);
    glEnd();
}

void DrawGrid(GLfloat a_width, GLfloat a_height, GLfloat a_gridWidth)
{
    // Horizontal lines
    for (float i = -a_height; i < a_height; i += a_gridWidth)
    {
        Vertex l_vertex1 = { -a_width, i, 0.0f, 1.0f, 1.0f, 1.0f, 1.0f };
        Vertex l_vertex2 = { a_width, i, 0.0f, 1.0f, 1.0f, 1.0f, 1.0f };
        DrawLineSegment(l_vertex1, l_vertex2);
    }

    // Vertical lines
    for (float i = -a_width; i < a_width; i += a_gridWidth)
    {
        Vertex l_vertex1 = { i, -a_height, 0.0f, 1.0f, 1.0f, 1.0f, 1.0f };
        Vertex l_vertex2 = { i, a_height, 0.0f, 1.0f, 1.0f, 1.0f, 1.0f };
        DrawLineSegment(l_vertex1, l_vertex2);
    }
}











void PlotECGData(int a_offset, int a_size, float a_offsetY, float a_scale)
{
    // space between samples
    const float l_space = 0.1f / a_size * g_ratio;
    // inital position of the first vertex to render
    float l_pos = -a_size * l_space / 2.0f;
    // set line width
    glPointSize(5.00);
    glBegin(GL_POINTS);

    for (size_t i = a_offset; i < a_size + a_offset; ++i)
    {
        const float l_data = data_ecg[i] + a_offsetY;
        glVertex3f(l_pos, l_data, 0.0f);
        if (l_data < 0.501 && l_data>0.0) {

            glColor4f(0.99f, l_data, 0.00f, 0.8f);


        }
        if (l_data > 0.500 && l_data > 1.01) {

            glColor4f(l_data, 0.99f, 0.0f, 0.8f);


        }

        l_pos += l_space;
    }
    glEnd();
}

void ECGDemo(int a_counter)
{
    const int l_dataSize = ECG_DATA_BUFFER_SIZE;
    // Emulate the presence of multiple ECG leads (just for demo/ display purposes)
    PlotECGData(a_counter, l_dataSize * 0.5, -0.5f, 0.1f);

}

int main(int argc, char const* argv[])
{
    GLFWwindow* l_window;
    if (!glfwInit())
    {
        exit(EXIT_FAILURE);
    }

    const int WINDOW_WIDTH = 1080;
    const int WINDOW_HEIGHT = 480;

    l_window = glfwCreateWindow(WINDOW_WIDTH, WINDOW_HEIGHT, "Chapter 2", NULL, NULL);
    if (!l_window)
    {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    // Make sure window is on the current calling thread
    glfwMakeContextCurrent(l_window);

    // Enable anti-aliasing and smoothing
    glEnable(GL_POINT_SMOOTH);
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    float l_counter = 0;
    while (!glfwWindowShouldClose(l_window))
    {
        // Set up the viewport (using the width and height of the window) and clear the screen color buffer:
        int l_width, l_height;

        glfwGetFramebufferSize(l_window, &l_width, &l_height);
        g_ratio = (float)l_width / (float)l_height;

        //glViewport(0, 0, l_width, l_height);
        glClear(GL_COLOR_BUFFER_BIT);

        // Set up the camera matrix.
        // Note that further details on the camera model will be discussed in Chapter 3, Interactive 3D Data Visualization:
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();

        // Orthographic Projection
        //glOrtho(-g_ratio, g_ratio, -1.0f, 1.0f, 1.0f, -1.0f);
        //glMatrixMode(GL_MODELVIEW);
        //glLoadIdentity();
        //glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        // Draw
        DrawGrid(5.0f, 1.0f, 0.1f);
        //if (l_counter > 5000)
        //{
         //   l_counter = 0;
        //}
        //l_counter += 5;
        // run the demo visualizer
        ECGDemo(l_counter);


        // Swap the front and back buffers (GLFW uses double buffering) to update the screen
        glfwSwapBuffers(l_window);

        // process the event queue (such as keyboard inputs) to avoid lock-up:
        glfwPollEvents();
    }

    // Release the memory and terminate the GLFW library.
    glfwDestroyWindow(l_window);
    glfwTerminate();

    exit(EXIT_SUCCESS);
}

