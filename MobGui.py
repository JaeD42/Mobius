import Tkinter as tk
from ShottkiGroup import SchottkiGroup as SG
from MobiusTransformation import MobiusTrans as MobT


class MobGui(object):

    def __init__(self,points):
        self.root = tk.Tk()
        self.root.wm_title("Limit Set Visualisation")
        self.size=500

        self.points=points
        self.depth=1


        self.last_circs=[]
        self.canvas=tk.Canvas(self.root,height=self.size,width=self.size)

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.pack()
        self.accuracy = 0.01
        self.alphaScale = tk.Scale(self.root, from_=0, to=1,resolution=self.accuracy, length=self.size-50, orient=tk.HORIZONTAL,command=self.on_scale_change)
        self.alphaScale.set(0.5)
        self.alphaScale.pack()


        self.betaScale = tk.Scale(self.root, from_= self.accuracy, to=1-self.accuracy,resolution=self.accuracy, length=self.size-50, orient=tk.HORIZONTAL,command=self.on_scale_change)
        self.betaScale.set(0.5)
        self.betaScale.pack()

        self.gammaScale = tk.Scale(self.root, from_=self.accuracy, to=1-self.accuracy,resolution=self.accuracy, length=self.size-50, orient=tk.HORIZONTAL,command=self.on_scale_change)
        self.gammaScale.set(0.5)
        self.gammaScale.pack()

        self.only_lim = tk.IntVar()
        self.only_lim_but = tk.Checkbutton(self.root, text="Only Limset", variable=self.only_lim, command=self.on_scale_change)
        self.only_lim_but.pack()

        self.MobTrafFrame = tk.Frame(self.root)
        #self.MobTrafFrame.grid(row=2,column=2)
        self.a_entry = tk.Entry(self.MobTrafFrame)
        self.a_entry.grid(row=0,column=0)

        self.b_entry = tk.Entry(self.MobTrafFrame)
        self.b_entry.grid(row=0, column=1)

        self.c_entry = tk.Entry(self.MobTrafFrame)
        self.c_entry.grid(row=1, column=0)

        self.d_entry = tk.Entry(self.MobTrafFrame)
        self.d_entry.grid(row=1, column=1)

        self.apply_traf = tk.IntVar()
        self.apply_traf_but = tk.Checkbutton(self.MobTrafFrame,text="Apply add Traf", variable=self.apply_traf, command=self.on_scale_change)
        self.apply_traf_but.grid(row=1,column=2)

        self.MobTrafFrame.pack()

    def on_vals_change(self,*new_val):
        self.canvas.delete("all")
        self.new_shifts=True
        self.draw_lim_set()

    def on_scale_change(self,*new_val):
        self.canvas.delete("all")
        self.draw_lim_set()


    def click(self,arg):
        self.depth+=1
        self.draw_lim_set()

    def draw_lim_set(self,start_over=True):

        A, B, CA, CB, CC, CD = MobT.from_4_points(*self.points,alpha=float(self.alphaScale.get()),beta=float(self.betaScale.get()),gamma=float(self.gammaScale.get()))
        if start_over:
            self.canvas.delete("all")
            circs=[CA,CB,CC,CD]
            depth=self.depth
        else:
            circs=self.last_circs
            depth=1
        shottki = SG(A,B)
        ETraf=MobT(1,0,0,1)
        if self.apply_traf.get():
            ETraf = MobT(complex(self.a_entry.get()),
                         complex(self.b_entry.get()),
                         complex(self.c_entry.get()),
                         complex(self.d_entry.get()))


        if self.only_lim.get():
            saver = shottki.gen_limit_set(self.depth,10**-4,circs)
        else:
            saver = shottki.iterate_lim_set(depth,circs,epsilon=0.01)



        minx = 10 ** 5
        maxx = -10 ** 5
        miny = minx
        maxy = maxx

        for circ in saver.circles:

            c = ETraf(circ)
            if c.pos.real - c.r < minx:
                minx = c.pos.real - c.r
            if c.pos.real + c.r > maxx:
                maxx = c.pos.real + c.r
            if c.pos.imag - c.r < miny:
                miny = c.pos.imag - c.r
            if c.pos.imag + c.r > maxy:
                maxy = c.pos.imag + c.r

        scale = self.size / max(maxx - minx, maxy - miny)

        for circ in saver.circles:
            circ=ETraf(circ)
            x=(circ.pos.real-minx)*scale + (self.size-(maxx-minx)*scale)/2
            y=(circ.pos.imag-miny)*scale + (self.size-(maxy-miny)*scale)/2
            r=circ.r*scale
            #print (x,y,r)
            self.canvas.create_oval(x-r,y-r,x+r,y+r,fill="yellow",stipple="gray25")
        self.last_circs=saver.circles
        self.canvas.pack()

    def start(self):
        self.root.mainloop()


A, B, CA, CB, CC, CD = MobT.from_4_points(complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1),
                                                  alpha=0.5)

G = MobGui([complex(1, 0), complex(0, 1), complex(-1, 0), complex(0, -1)])



G.start()