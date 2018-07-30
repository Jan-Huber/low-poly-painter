# TAG
TAG_VERTEX = "v"
TAG_EDGE = "e"
TAG_FACE = "f"

# COLOR
COLOR_DEFAULT = "#000000"

class Face:
    def __init__(self, edge1, edge2, edge3, frame, mesh):
        # Information
        self.id = -1
        self.color = COLOR_DEFAULT
        self.edges = (edge1, edge2, edge3)

        # Dependencies
        self.mesh = mesh
        self.frame = frame
        self.canvas = frame.canvas

        # Update
        self.draw()
        edge1.faces.append(self)
        edge2.faces.append(self)
        edge3.faces.append(self)
        coords = self.getCoordinates()
        self.getColorFromImage(coords)

    """ GENERAL """
    def draw(self):
        coords = self.getCoordinates()
        self.id = self.canvas.create_polygon(coords[0][0], coords[0][1],
                                             coords[1][0], coords[1][1],
                                             coords[2][0], coords[2][1],
                                             fill=self.color,
                                             tag=TAG_FACE,
                                             state=self.frame.faceState)
        self.canvas.tag_lower(self.id, TAG_EDGE)

    def getColorFromImage(self, coords):
        self.color = self.frame.color.fromImage(coords)
        self.canvas.itemconfig(self.id, fill=self.color)

    def move(self):
        coords = self.getCoordinates()
        self.canvas.coords(self.id, coords[0][0], coords[0][1],
                                    coords[1][0], coords[1][1],
                                    coords[2][0], coords[2][1])
        self.getColorFromImage(coords)


    def delete(self):
        queue = self.edges[:]
        for edge in queue:
            edge.faces.remove(self)

        self.mesh.faces.remove(self)
        self.canvas.delete(self.id)

    def getVertices(self):
        vert1 = self.edges[0].verts[0].coords
        vert2 = self.edges[0].verts[1].coords
        vert3 = self.edges[1].verts[0].coords
        if vert3 is vert1:
            vert3 = self.edges[1].verts[1].coords
        return [vert1, vert2, vert3]

    def getCoordinates(self):
        verts = self.getVertices()
        verts.sort(key = lambda vert: vert[1], reverse = False)

        if verts[0][1] == verts[1][1]:
            if verts[0][0] < verts[1][0]:
                verts[0], verts[1] = verts[1], verts[0]

        rot = (verts[1][1] - verts[0][1])*(verts[2][0] - verts[1][0])
        ate = (verts[2][1] - verts[1][1])*(verts[1][0] - verts[0][0])
        rotate = rot - ate

        if rotate < 0:
            verts[1], verts[2] = verts[2], verts[1]

        return verts
