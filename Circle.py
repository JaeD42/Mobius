import math

class Circle(object):
    """"
    Class for Circles
    TODO:LINES ARE NOT YET SUPPORTED
    """

    def __init__(self,pos,r):
        self.pos=pos
        self.r=r

    def get_3_points(self,xAxisInv=1):
        """
        Returns 3 points on circle to define it
        :param xAxisInv:
        :return:
        """
        z1 = self.pos + xAxisInv * self.r
        z2 = self.pos + self.r * 1J
        z3 = self.pos - self.r *1J
        return [z1,z2,z3]

    def get_plottable(self):
        """
        Mini wrapper for easier access to artists
        :return:
        """
        return [self.pos.real,self.pos.imag,self.r]

    def get_boundary(self,res=360):
        """
        Returns res points on boundary of circle
        :param res:
        :return:
        """
        return [complex(math.cos(float(i)/res*2*math.pi),math.sin(float(i)/res*2*math.pi))*self.r-self.pos for i in range(res)]

    def get_inside_outside(self,num_vals=2500):
        """
        Returns num vals points that around the circle
        :param num_vals:
        :return:
        """
        side = int(num_vals**0.5)
        vals = [complex(float(2*i)/side,float(2*j)/side)*self.r*1.2 for i in range(-side/2,side/2) for j in range(-side/2,side/2)]
        inside = [i-self.pos for i in vals if abs(i)<self.r]
        outside = [i-self.pos for i in vals if abs(i)>self.r]
        return (inside,outside)

    @staticmethod
    def from_3_points(x,y,z):
        """
        Creates Circle given three points, tested with three points from Circle class
        :param x:
        :param y:
        :param z:
        :return:
        """
        AB=(y-x)
        AC=(z-x)
        BC=(z-y)



        #Calculate Radius using geometry and identities (trust me future me, it should work, but you can test)
        if abs(AB)==0 or abs(AC)==0 or abs(BC)==0 or 1.0-((AB.real*AC.real+AB.imag*AC.imag)/(abs(AB)*abs(AC)))**2 ==0:
            return Circle(x,0)
        else:
            R = 1.0/(2*(1.0/abs(BC)**2-
                        ((AB.real*AC.real+AB.imag*AC.imag)/(abs(AB)*abs(AC)*abs(BC)))**2)
                        **0.5)

        #Calculate center using geometry
        midP = AB/2+x
        midPDist = abs((R**2 - abs(AB)**2/4))**0.5
        center1A = midP + midPDist * (AB*1J/abs(AB))
        center1B = midP + midPDist * (AB * -1J / abs(AB))

        midP2 = AC / 2 + x
        midPDist2 = abs((R ** 2 - abs(AC) ** 2 / 4)) ** 0.5
        center2A = midP2 + midPDist2 * (AC*1J / abs(AC))
        center2B = midP2 + midPDist2 * (AC * -1J / abs(AC))

        if abs(center2A-center1A)<0.0001 or abs(center2A-center1B)<0.0001:
            return Circle(center2A,R)


        return Circle(center2B,R)

    def get_svg_format(self):
        return [(self.pos.real,self.pos.imag),self.r]

    def __repr__(self):
        return str((self.pos,self.r))
