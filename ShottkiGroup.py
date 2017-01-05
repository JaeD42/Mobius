from MobiusTransformation import MobiusTrans as MobT
from Circle import Circle
from SvgSaver import SVGSaver
from collections import deque
from collections import Counter
class SchottkiGroup(object):

    def __init__(self,A,B):
        self.A=A
        self.B=B
        self.a=A.get_inverse()
        self.b=B.get_inverse()
        self.funcs = [self.A,self.B,self.a,self.b]
        self.opposite={self.A:self.a,self.B:self.b,self.a:self.A,self.b:self.B}

    def gen_limit_set(self,max_depth,epsilon,startCircle,path=None):
        saver = SVGSaver()
        counter = Counter()
        dfs = deque()
        startCircle.depth=0
        startCircle.last=None
        dfs.append(startCircle)
        while len(dfs)>0:
            circ = dfs.popleft()
            if circ.r<epsilon or circ.depth>=max_depth:
                if circ.r==0:
                    continue
                c=Circle(circ.pos,circ.r)
                c.depth=circ.depth
                c.last=self.funcs.index(circ.last)
                saver.add_circle(c)
                counter[circ.last]+=1
                continue

            for f in self.funcs:
                if not self.opposite[f] is circ.last:
                    nCirc = f(circ)
                    nCirc.last=f
                    nCirc.depth=circ.depth+1
                    dfs.appendleft(nCirc)
        print counter
        return saver


if __name__=="__main__":
    A,B = MobT.GrandMa(2+0.5J,2.5,other=True)

    for i in range(1):
        A,B,CA,CB,CC,CD = MobT.from_4_points(complex(-2,0),complex(0,1),complex(3,0),complex(0,-1),alpha=0.0)
        print CA,A(CA)

        print CB,A(CB)

        print CC,A(CC)

        print CD,A(CD)
        fileName="super"+str(i)+".svg"



        S = SchottkiGroup(A,B)

        saver = S.gen_limit_set(9,10**-8,Circle(20+20J,2))
        print max([c.r for c in saver.circles])
        maxCirc = None
        maxR = 0
        for c in saver.circles:
            if c.r>maxR:
                maxR=c.r
                maxCirc=c


        from Mobius.SvgManipulation import SVGContainer as Con

        container = Con(saver.getXMLString())


        def change(inp):
            res = []
            mul100 = ["cx", "cy"]
            for val in mul100:
                mul = 100
                res.append((val, mul * (float(inp[val])+5)))
            res.append(("r",max(0.5,float(inp["r"]))))
            if "id" in inp:
                if inp["id"] == "0":
                    res.append(("fill", "blue"))
                elif inp["id"] == "1":
                    res.append(("fill", "red"))
                elif inp["id"] == "2":
                    res.append(("fill", "green"))
                else:
                    res.append(("fill", "black"))
            else:
                print "here"
            # res.append(("fill","url(#radial)"))
                res.append(("r", float(inp["r"])*100))
            return res


        container.add_circle(CA, col='yellow')
        container.add_circle(CB, col='yellow')
        container.add_circle(CC, col='yellow')
        container.add_circle(CD, col='yellow')


        container.batch_change(change)
        container.change_property(container.tree.getroot(), "width", 1000)
        container.change_property(container.tree.getroot(), "height", 1000)

        container.save(fileName)


    C = maxCirc
    #C = Circle(0+0J,0.9)
    print C
    print A.get_inverse().get_fix_points()
    print A.get_inverse()(C)
    print B.get_inverse()(C)
    print A(C)
    print B(C)

