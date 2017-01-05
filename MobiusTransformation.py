from Circle import Circle
import numpy as np
inf = np.inf

def isclose(a,b,e=10**-6):
    return abs(a-b)<e

class MobiusTrans(object):
    """
    Mobius Transformation Class
    """
    def __init__(self,a,b,c,d):
        """
        Init with 4 values, automatically divided to get det=1
        :param a:
        :param b:
        :param c:
        :param d:
        """
        det = (a*d-b*c + 0J)**0.5
        self.a=a/det
        self.b=b/det
        self.c=c/det
        self.d=d/det

    def __call__(self,z):
        """
        Call function, MobTrafs can be called with Circle class or complex numbers
        :param z:
        :return:
        """

        if type(z)==Circle:
            return Circle.from_3_points(*[self(i) for i in z.get_3_points()])
        if z==inf:
            if self.c==0:
                return inf
            else:
                return self.a/self.c

        if self.c*z+self.d==0:
            return inf

        return (self.a*z+self.b)/(self.c*z+self.d)

    def get_inverse(self):
        """
        Get inverse of MobTraf
        :return:
        """
        return MobiusTrans(self.d,-self.b,-self.c,self.a)

    def __eq__(self, other):
        if type(other)!=type(self):
            return False
        return isclose(self.a,other.a) and isclose(self.b,other.b) and isclose(self.c,other.c) and isclose(self.d,other.d)

    def __hash__(self):
        return (self.a,self.b,self.c,self.d).__hash__()

    def __mul__(self,other):
        return MobiusTrans(self.a*other.a+self.b*other.c,
                           self.a*other.b+self.b*other.d,
                           self.c*other.a+self.d*other.c,
                           self.c*other.b+self.d*other.d)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        s="%s  %s \n%s  %s"%(self.a,self.b,self.c,self.d)
        return s

    def __str__(self):
        return self.__repr__()

    def determinant(self):
        return self.a*self.d-self.b*self.c

    def get_fix_points(self):
        """
        Calculate Fix Points
        """
        disc = (self.a+self.d)**2-4
        res1 = self.a-self.d + disc**0.5
        res2 = self.a-self.d - disc**0.5
        if self.c==0:
            return [inf]
        res1 = res1/self.c
        res2 = res2/self.c

        return res1,res2

    def reduced(self):
        return MobiusTrans(self.a,self.b,self.c,self.d)

    @staticmethod
    def create_from_circles(self,C1,C2):
        """
        Work in progress, Problem is that this is not unique, so put on hold for now
        :param C1:
        :param C2:
        :return:
        """
        [z1,z2,z3]=C1.get_3_points()

        MT1 = MobiusTrans(z2-z3,-z1*(z2-z3),z2-z1,-z3*(z2-z1))

        [z1, z2, z3] = C2.get_3_points(xAxisInv=-1)
        print z3,z2,z1

        MT2 = MobiusTrans(z2 - z3, -z1 * (z2 - z3), z2 - z1, -z3 * (z2 - z1))

        return (MT2.get_inverse()*MT1).reduced()

    @staticmethod
    def create_from_triples(trip1,trip2):
        """
        Calculate MobTraf that sends trip1 to trip2
        :param trip1:
        :param trip2:
        :return:
        """
        MT1 = MobiusTrans(trip1[1]-trip1[2],-1*trip1[0]*(trip1[1]-trip1[2]),trip1[1]-trip1[0],-1*trip1[2]*(trip1[1]-trip1[0]))
        MT2 = MobiusTrans(trip2[1] - trip2[2], -1 * trip2[0] * (trip2[1] - trip2[2]), trip2[1] - trip2[0],
                          -1 * trip2[2] * (trip2[1] - trip2[0]))

        return (MT2.get_inverse()*MT1).reduced()


    def get_root(self):
        """
        Get (positive) root of MobTraf
        :return:
        """
        s=1
        t=(self.a+self.d+2)**0.5
        t=1/t
        return MobiusTrans(t * (self.a+s),t*self.b,t*self.c,t*(self.d+s))


    def get_vector_at_point(self,x,y):
        """
        Unnecessary I think, should be deleted
        :param x:
        :param y:
        :return:
        """
        z=x+y*1J
        return ((self.a-1)*z+self.b)/((self.c-1)*z+self.d) - z

    @staticmethod
    def GrandMa(ta, tb, other=False):
        ta = ta + 0J
        tb = tb + 0J
        l = 1
        if other:
            l = -1
        tab = (ta * tb) / 2 + l * ((ta * tb) ** 2 / 4 - ta ** 2 - tb ** 2) ** 0.5

        z = (tab - 2) * tb / (tb * tab - 2 * ta + 2J * tab)

        A = MobiusTrans(ta / 2,
                        (ta * tab - 2 * tb + 4J) / ((2 * tab + 4) * z),
                        (ta * tab - 2 * tb - 4J) * z / (2 * tab - 4),
                        ta / 2)
        B = MobiusTrans((tb - 2J) / 2,
                        tb / 2,
                        tb / 2,
                        (tb + 2J) / 2)

        return A, B

    @staticmethod
    def from_4_points(A,B,C,D,alpha=0.5,beta=0.5,gamma=0.5):
        w=abs(B-A)
        x=abs(C-B)
        y=abs(D-C)
        z=abs(A-D)
        print w,x,y,z
        if abs(w+y-x-z)>0.0001:
            return None

        minR_A = max([z-y,w-x,(w+z-abs(B-D))/2])
        maxR_A = min([(abs(C-A)+w-x)/2,(abs(C-A)+z-y)/2])
        print w,x,y,z
        print abs(B-D)
        print minR_A
        print maxR_A

        R_a = minR_A + alpha*(maxR_A-minR_A)
        R_b = w-R_a
        R_d = z-R_a
        R_c = x-R_b

        A_p = A + R_a * (B - A) / abs(B - A)
        A_q = A + R_a * (D - A) / abs(D - A)
        midTempA = A_p + beta * (A_q - A_p)
        A_mid = A + R_a * (midTempA - A) / abs(midTempA - A)

        B_p = B + R_b * (C - B) / abs(C - B)
        B_q = A_p
        midTempB = B_p + gamma * (B_q - B_p)
        B_mid = B + R_b * (midTempB - B) / abs(midTempB - B)

        C_p = C + R_c * (D - C) / abs(D - C)
        C_q = B_p
        C_mid = C + R_c * (A - C) / abs(A - C)

        D_p = A_q
        D_q = C_p
        D_mid = D + R_d * (B - D) / abs(B - D)

        MobTrafA = MobiusTrans.create_from_triples((A_p,A_mid,A_q),(C_q,C_mid,C_p))
        MobTrafB = MobiusTrans.create_from_triples((B_p, B_mid, B_q), (D_q, D_mid, D_p))

        CircA = Circle(A,R_a)
        CircB = Circle(B, R_b)
        CircC = Circle(C, R_c)
        CircD = Circle(D, R_d)

        return [MobTrafA,MobTrafB,CircA,CircB,CircC,CircD]





