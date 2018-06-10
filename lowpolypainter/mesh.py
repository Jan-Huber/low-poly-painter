# TODO: Add better function to insert new faces
# TODO: Delete vertecies or faces one by one

"""
Mesh Class

Description:
Stores mesh of vertices, which connections are stored as faces.
Points and tris can be added and removed from the mesh.
"""

class Mesh(object):

    def __init__(self, width, height):
        self.faces = []
        self.vertices = []
        self.width = width
        self.height = height

    # Adds vertex to mesh
    def addVertex(self, x, y):
        # Create Vertex
        vertex = Vertex(x, y)
        self.vertices.append(vertex)

    # Adds face to mesh
    # (!) Faces should be sorted anticlockwise
    def addFace(self, vertexIndex1, vertexIndex2, vertexIndex3, color):

        # Sort vertices anticlockwise
        verticesIndex = [vertexIndex1, vertexIndex2, vertexIndex3]
        verticesIndex.sort(key = lambda i: self.vertices[i].y, reverse = False)

        # Current vertices sorted by y
        v1 = self.vertices[verticesIndex[0]]
        v2 = self.vertices[verticesIndex[1]]
        v3 = self.vertices[verticesIndex[2]]

        # Calculate slope for v2 and v3 to v1
        mv2v1 = (v2.x - v1.x) / float(v2.y - v1.y) if (v2.y - v1.y) != 0 else 0
        mv3v1 = (v3.x - v1.x) / float(v3.y - v1.y) if (v3.y - v1.y) != 0 else 0

        # Sort by x value 
        if mv2v1 > mv3v1:
            verticesIndex[1], verticesIndex[2] = verticesIndex[2], verticesIndex[1]

        # Create Face
        face = Face(verticesIndex[0], verticesIndex[1], verticesIndex[2], color)
        self.faces.append(face)


    # Deletes all vertecies and faces
    def clear(self):
        self.faces = []
        self.vertices = []


"""
Vertex Class

Description:
Stores a vertex of the mesh, which contains and x and y coordinate.
"""

class Vertex(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y


"""
Face Class

Description:
Stores faces of the mesh, which contains three vertecies and a color.
"""

class Face(object):

    def __init__(self, vertexPos1, vertexPos2, vertexPos3, color):
        self.vertices = [vertexPos1, vertexPos2, vertexPos3]
        self.color = color