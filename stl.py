from __future__ import annotations

import numpy as np

from structures import Triangle, Object


def load_ascii(stl_path: str) -> Object:
    with open(stl_path, mode='r') as f:
        lines = f.readlines()

    # initialize the list of triangles
    triangles = []

    # initialize the current triangle and its color
    triangle = None
    color = None

    # iterate over the lines in the STL string
    for line in lines:
        # split the line into words
        words = line.split()

        # if the first word is 'facet' we are starting a new triangle
        if words[0] == 'facet':
            # create a new triangle
            triangle = Triangle(
                normal=np.array([float(words[2]), float(words[3]), float(words[4])]),
                vertices=[],
            )
        # if the first word is 'vertex' we are adding a new vertex to the triangle
        elif words[0] == 'vertex':
            # add the new vertex to the list of vertices
            triangle.vertices.append(np.array([float(words[1]), float(words[2]), float(words[3])]))
        # if the first word is 'endfacet' we have finished the current triangle
        elif words[0] == 'endfacet':
            # set the color of the triangle
            triangle.color = color
            # append the current triangle to the list of triangles
            triangles.append(triangle)
        # if the first word is 'color' we are setting the color of the triangle
        elif words[0] == 'color':
            # set the color of the triangle
            color = np.array([float(words[1]), float(words[2]), float(words[3])])

    return Object(triangles=triangles)


def load_binary(stl_path: str) -> Object:
    # read the binary STL file as a binary string
    with open(stl_path, 'rb') as f:
        stl_string = f.read()

    # initialize the list of triangles
    triangles = []

    # read the number of triangles from the binary string
    num_triangles = np.frombuffer(stl_string[80:84], np.uint32)[0]

    # initialize the current position in the binary string
    pos = 84

    # iterate over the triangles in the binary string
    for i in range(num_triangles):
        # read the normal vector of the triangle from the binary string
        normal = np.frombuffer(stl_string[pos:pos + 12], np.float32)
        pos += 12

        # read the vertices of the triangle from the binary string
        vertices = [
            np.frombuffer(stl_string[pos:pos + 12], np.float32),
            np.frombuffer(stl_string[pos + 12:pos + 24], np.float32),
            np.frombuffer(stl_string[pos + 24:pos + 36], np.float32),
        ]
        pos += 36

        # read the color of the triangle from the binary string
        color = np.frombuffer(stl_string[pos:pos + 2], np.uint16)
        pos += 2

        # create a new triangle with the parsed data
        triangle = Triangle(normal=normal, vertices=vertices, color=color)

        # append the triangle to the list of triangles
        triangles.append(triangle)

    return Object(triangles=triangles)


def load(stl_path: str, binary: bool = True) -> Object:
    if binary:
        return load_binary(stl_path)
    else:
        return load_ascii(stl_path)
