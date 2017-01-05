from lxml import etree
import svgwrite as svg

class SVGContainer(object):

    def __init__(self,tree):
        self.tree=etree.ElementTree(etree.fromstring(tree))

    @staticmethod
    def from_file(path):

        tree = etree.parse(path)
        return SVGContainer(tree.tostring())

    def change_property(self,elem,property,new_value):
        elem.set(property,str(new_value))

    def get_property(self,elem,property):
        return elem.get(property)

    def change_r(self,elem,r):
        self.change_property(elem,"r",r)

    def batch_change(self,func):
        """
        Function takes a dict of values and
        should return a list of tuples with properties and new values

        :param func:
        :return:
        """
        for elem in self.tree.iter("{http://www.w3.org/2000/svg}circle"):
            changes = func(elem.attrib)
            for prop,val in changes:
                self.change_property(elem,prop,val)

        for elem in self.tree.iter("circle"):
            changes = func(elem.attrib)
            for prop,val in changes:
                self.change_property(elem,prop,val)

    def save(self,file):
        with open(file,"w") as f:
            self.tree.write(f,pretty_print=True)

    def tostring(self):
        return etree.tostring(self.tree,pretty_print=True)


    def delete_elem(self,func):

        for elem in self.tree.iter("{http://www.w3.org/2000/svg}circle"):
            delete = func(elem.attrib)
            if delete:
                elem.getparent().remove(elem)

    def add_circle(self,Circle,col='blue',opac=0.5):
        c = svg.shapes.Circle(*Circle.get_svg_format(),fill=col,opacity=opac)
        self.tree.getroot().append(etree.fromstring(c.tostring()))


