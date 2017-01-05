import svgwrite as svg
from Circle import Circle

class SVGSaver(object):

    def __init__(self):
        self.circles = []
        self.linePoints = []


    def add_circle(self,circle):
        self.circles.append(circle)

    def add_all_circles(self,circle_list):
        self.circles.extend(circle_list)

    def add_line_point(self,p):
        self.linePoints.append(p)


    def save(self,file):
        drawing = svg.Drawing(file, size=(10, 10))
        for circle in self.circles:
            c = drawing.circle(*circle.get_svg_format(), fill='blue', opacity=0.5)
            c["id"] = circle.last
            drawing.add(c)

        drawing.save()

    def getXMLString(self):
        drawing = svg.Drawing(file, size=(10, 10))
        for circle in self.circles:
            c = drawing.circle(*circle.get_svg_format(), fill='blue', opacity=0.5)
            c["id"] = circle.last
            drawing.add(c)

        return drawing.tostring()





