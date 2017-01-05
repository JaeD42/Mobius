"""
Lots of tests and smaller defs for various crap

Good luck figuring this out :/

"""
import math
from MobiusTransformation import MobiusTrans
from Circle import Circle

def animatePoints(Trafo,points,cols,steps=8192,name="blabla.mp4",save=False):
    from matplotlib.animation import FuncAnimation
    import matplotlib.pyplot as plt



    class anim(object):
        """
        Inner Class, might be overkill
        """
        def __init__(self,traf,points,scat,cols):
            self.T=traf
            self.p=points
            self.scat = scat
            self.cols =cols
            self.size=10

        def update(self,it):
            self.p = [self.T(point) for point in self.p]
            self.scat.set_offsets(zip([po.real for po in self.p], [po.imag for po in self.p]))
            self.scat.set_sizes([self.size]*len(self.p))
            self.size*=0.999
            #cols = ['r', 'g', 'b', 'c']
            scat.set_color(self.cols)

    plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
    for i in range(int(math.log(steps)+0.5)):
        Trafo=Trafo.get_root()

    fig = plt.figure()
    ax = plt.axes(xlim=(-5, 5), ylim=(-5, 5))
    scat = ax.scatter([p.real for p in points],[p.imag for p in points])
    animClass = anim(Trafo,points,scat,cols)

    animation = FuncAnimation(fig,animClass.update,interval=10,frames=900)
    if save:
        animation.save(name, fps=60)
    plt.show()


def animateLimSet(TA,TB,startPoint,steps):
    from matplotlib.animation import FuncAnimation
    import matplotlib.pyplot as plt
    plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'

    class anim(object):
        def __init__(self,TA,TB,point,scat):
            self.TA=TA
            self.Ta=TA.get_inverse()
            self.TB=TB
            self.Tb=TB.get_inverse()
            self.Trafs = [self.TA,self.Ta,self.TB,self.Tb]
            self.points={i:[i(point)] for i in self.Trafs}
            self.inv = {self.TA:self.Ta,self.TB:self.Tb,self.Ta:self.TA,self.Tb:self.TB}
            self.scat=scat
            self.first=0
            self.called=False
            self.size=10

        def update(self,it):
            if self.first<2:
                self.first+=1
                return
            if self.called:
                di={}
                for traf in self.Trafs:
                    nPoints = set()
                    for trafLast in self.Trafs:
                        if not self.inv[traf]==trafLast:
                            nPoints = nPoints.union([traf(i) for i in self.points[trafLast]])
                    di[traf]=list(nPoints)
                self.points=di
            allPs = []
            self.called=True
            for i in self.points.values():
                allPs.extend(i)
            self.scat.set_offsets(zip([po.real for po in allPs], [po.imag for po in allPs]))
            self.scat.set_sizes([self.size for i in xrange(len(allPs))])
            cols = ['r','g','b','c']
            scat.set_color([cols[int(4*i/len(allPs))] for i in range(len(allPs))])
            self.size=float(self.size)/1.2

    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 2), ylim=(-2, 2))
    scat = ax.scatter([startPoint.real], [startPoint.imag])
    animClass = anim(TA,TB, startPoint, scat)

    animation = FuncAnimation(fig, animClass.update, interval=2000, frames=10)
    #animation.save('anim8.mp4', fps=1)
    plt.show()


def animateLimSetDeep(TA,TB,startPoint,steps,cutoff=15,save=False):
    from matplotlib.animation import FuncAnimation
    import matplotlib.pyplot as plt
    plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
    class closenesSet(object):
        def __init__(self,cutoff=1000):
            self.vals=[]
            self.cutoff=cutoff


        def addAll(self,list,dist=0.01):
            def distIter(val,list,minDist):
                yield abs(val)<self.cutoff
                for val2 in list:
                    yield abs(val-val2)>minDist
                yield True

            for val in list:
                if all(distIter(val,self.vals,dist)):
                    self.vals.append(val)
            #addList = [i for i in list if all(distIter(i,self.vals,dist))]
            #self.vals.extend(addList)

    class anim(object):
        def __init__(self,TA,TB,point,scat):
            self.TA=TA
            self.Ta=TA.get_inverse()
            self.TB=TB
            self.Tb=TB.get_inverse()
            self.Trafs = [self.TA,self.Ta,self.TB,self.Tb]
            self.points={i:[i(point)] for i in self.Trafs}
            self.inv = {self.TA:self.Ta,self.TB:self.Tb,self.Ta:self.TA,self.Tb:self.TB}
            self.scat=scat
            self.first=0
            self.called=False
            self.size=10

        def update(self,it):
            if self.first<2:
                self.first+=1
                return
            if self.called:
                di={}
                for traf in self.Trafs:
                    nPoints = closenesSet(cutoff)
                    for trafLast in self.Trafs:
                        if not self.inv[traf]==trafLast:
                            nPoints.addAll([traf(i) for i in self.points[trafLast]])
                    di[traf]=nPoints.vals
                self.points=di

            allPs = []
            self.called=True
            for i in self.points.values():
                allPs.extend(i)
            print it,len(allPs)
            self.scat.set_offsets(zip([po.real for po in allPs], [po.imag for po in allPs]))
            self.scat.set_sizes([self.size for i in xrange(len(allPs))])
            cols = ['r','g','b','c']
            scat.set_color([cols[int(4*i/len(allPs))] for i in range(len(allPs))])
            self.size=float(self.size)/1.2

    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 2), ylim=(-2,2))
    scat = ax.scatter([startPoint.real], [startPoint.imag])
    animClass = anim(TA,TB, startPoint, scat)

    animation = FuncAnimation(fig, animClass.update, interval=1000, frames=20)
    if save:
        animation.save('anim11.mp4', fps=1)
    plt.show()


p=0.3
dA1B1=2**0.5
dA2B2=2**0.5
A1 = Circle(complex(1,0),p*dA1B1)
B1 = Circle(complex(0,1),(1-p)*dA1B1)
B2 = Circle(complex(0,-1),dA2B2-p*dA1B1)
A2 = Circle(complex(-2,0),5**0.5-(dA2B2-p*dA1B1))

A1 = Circle(complex(2,0),1)
A2 = Circle(complex(-2,0),1)
B1 = Circle(complex(0,2),1)
B2 = Circle(complex(0,-2),1)

c=1
MTtest=MobiusTrans(1,2,2,1)
TA = MTtest.create_from_triples((c+1J,c+1+0J,c-1J),(-c-1J,-c+1+0J,-c+1J))
TB = MTtest.create_from_triples((-1+c*1J,c*1J+1J,1+c*1J),(-1-c*1J,-1J-c*1J,1-c*1J))
#TA,TB = GrandMa(1.87+0.1J,1.87-0.1J)
#TA,TB = GrandMa(2+0.5J,2+0.5J,other=False)

#ps = [complex(float(i)/10,float(j)/10) for i in range(-10,10) for j in range(-10,10)]
ps = [(complex(math.cos(float(i)/360*2*math.pi)-1,math.sin(float(i)/360*2*math.pi))) for i in range(360)]
#alls = [complex(float(i)/10,float(j)/10) for i in range(-12,12) for j in range(-12,12)]
#inner= [i-2 for i in alls if abs(i)<1 ]
#outer= [i-2 for i in alls if abs(i)>1 ]

cols = ['r']*(len(ps)/3)+['g']*(len(ps)/3)+['b']*(len(ps)/3)

#ps.extend(inner)
#ps.extend(outer)
#ps=A1.get_boundary(360)
#ps.extend(A2.get_boundary(360))
#ps.extend(B1.get_boundary(360))
#ps.extend(B2.get_boundary(360))


#TA = MTtest.create_from_triples((2+1J,3+0J,2-1J),(-2-1J,-1+0J,-2+1J))
animatePoints(TA.get_inverse(),ps,cols,name="animCircleCol.mp4",save=False)
#animateLimSetDeep(TA,TB,complex(0,0),10)
#print TA.get_fix_points()
#for i in range(5):
#    TA=TA.get_root()

#X, Y = np.meshgrid(np.arange(-10, 10, .2), np.arange(-10, 10, .2))
#vec = [[0 for i in range(len(X))] for j in range(len(X))]
#for i in range(len(X)):
#    for j in range(len(X)):
#        vec[i][j]=TA(X[i,j]+Y[i,j]*1J)-(X[i,j]+Y[i,j]*1J)



"""

import matplotlib.pyplot as plt

c1 = plt.Circle(A1.get_plottable()[:2],A1.r, fill=False)
c2 = plt.Circle(A2.get_plottable()[:2],A2.r, fill=False)
c3 = plt.Circle(B1.get_plottable()[:2],B1.r, fill=False)
c4 = plt.Circle(B2.get_plottable()[:2],B2.r, fill=False)
fig, ax = plt.subplots()

#ax.add_artist(c1)
#ax.add_artist(c2)
#ax.add_artist(c3)
#ax.add_artist(c4)

#vals = [complex((i-50.0)/25,(j-50.0)/25) for i in range(100) for j in range(100)]
#mobVals = [Ta(i) for i in vals]


#scatterCompList(mobVals,ax)
#scatterCompList(vals,ax)
#fP=findFixedPointsOfMatrixes(TA,TB,7)
#scatterCompList(fP,ax)
#print fP

vecField(X,Y,vec,ax)
ax.set_xlim(xmin=-10, xmax=10)
ax.set_ylim((-3,3))
plt.draw()
plt.show()
"""
