import math
from MobiusTransformation import MobiusTrans as MT
from Circle import Circle as C

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

#Create a Circle
C1=C(1+2J,4)
#Create a Mob Traf
Traf = MT(1+1J,2,-2+0.5J,1+2J)

#Animate
animatePoints(Traf,C1.get_boundary(res=360),cols=['r' for i in range(360)])