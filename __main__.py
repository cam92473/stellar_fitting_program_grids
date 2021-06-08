import numpy
import scipy.optimize as opt
import pandas as pd

class ChiSquared():
    def __init__(self):
        self.intro_gui()
        self.extract_measured_flux()
        self.sift()
        self.convert_to_AB()
        self.convert_to_bandflux()
        self.prepare_for_interpolation()
        self.minimize_chisq()
        self.display_results()
    
    def intro_gui(self):
        self.switch = False
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        mwin = tk.Tk()
        mwin.geometry("580x420+780+300")
        mwin.title("Enter filename")
        def collectfilename():
            from tkinter import messagebox
            if user_filename.get() == "":
                tk.messagebox.showinfo('Error', 'Please enter a filename')
            else:
                try:
                    import pandas as pd
                    self.measuredata = pd.read_csv("{}".format(user_filename.get(),delimiter=","))
                    if user_rownumber.get() > len(self.measuredata):
                        tk.messagebox.showinfo('Error', "Row specified is out of range.")
                    else:
                        self.switch = True
                        self.rownumber = user_rownumber.get()
                        self.gguess = user_gguess.get()
                        self.Tguess = user_Tguess.get()
                        self.Zguess = user_Zguess.get()
                        self.thetaguess = user_thetaguess.get()
                        self.ebvguess = user_ebvguess.get()
                        mwin.quit()
                except:
                    tk.messagebox.showinfo('Error', "Could not find file. Please place the file in the program folder and try again.")
        user_filename = tk.StringVar()
        enterfileneame = tk.Entry(mwin,textvariable = user_filename,width=64)
        enterfileneame.place(x=20,y=60)
        user_rownumber = tk.IntVar()
        enterrownumber = tk.Entry(mwin,textvariable=user_rownumber,width=10)
        enterrownumber.place(x=20,y=180)
        labelwhich = tk.Label(mwin,text="Which row?")
        labelwhich.place(x=20,y=150)
        labeltop = tk.Label(mwin,text="Please enter filename to be read: ")
        labeltop.place(x=20,y=30)
        labelbot = tk.Label(mwin,text="e.g. \"filter_magnitudes.csv\"")
        labelbot.place(x=20,y=90)
        user_gguess = tk.DoubleVar()
        user_Tguess = tk.DoubleVar()
        user_Zguess = tk.DoubleVar()
        user_thetaguess = tk.DoubleVar()
        user_ebvguess = tk.DoubleVar()
        labelg = tk.Label(mwin,text="log g").place(x=50,y=320)
        entryg = tk.Entry(mwin,textvariable=user_gguess,width=8)
        entryg.place(x=50,y=350)
        labelT = tk.Label(mwin,text="T/10000").place(x=150,y=320)
        entryT = tk.Entry(mwin,textvariable=user_Tguess,width=8)
        entryT.place(x=150,y=350)
        labelZ = tk.Label(mwin,text="Z").place(x=250,y=320)
        entryZ = tk.Entry(mwin,textvariable=user_Zguess,width=8)
        entryZ.place(x=250,y=350)
        labeltheta = tk.Label(mwin,text="θ_r/1e-12").place(x=350,y=320)
        entrytheta = tk.Entry(mwin,textvariable=user_thetaguess,width=8)
        entrytheta.place(x=350,y=350)
        labelebv = tk.Label(mwin,text="E(B-V").place(x=450,y=320)
        entryebv = tk.Entry(mwin,textvariable=user_ebvguess,width=8)
        entryebv.place(x=450,y=350)
        def gray():
            if entryg['state'] == tk.NORMAL:
                entryg['state'] = tk.DISABLED
                entryT['state'] = tk.DISABLED
                entryZ['state'] = tk.DISABLED
                entrytheta['state'] = tk.DISABLED
                entryebv['state'] = tk.DISABLED
            elif entryebv['state'] == tk.DISABLED:
                entryg['state'] = tk.NORMAL
                entryT['state'] = tk.NORMAL
                entryZ['state'] = tk.NORMAL
                entrytheta['state'] = tk.NORMAL
                entryebv['state'] = tk.NORMAL
        gobutton = tk.Button(mwin,text="Fit data",command = collectfilename,pady=10,padx=20,bd=3)
        gobutton.place(x=435,y=150)
        entryg.delete(0,10)
        entryg.insert(0,"4.5")
        entryT.delete(0,10)
        entryT.insert(0,"3.2")
        entryZ.delete(0,10)
        entryZ.insert(0,"0")
        entrytheta.delete(0,10)
        entrytheta.insert(0,".7368")
        entryebv.delete(0,10)
        entryebv.insert(0,"0.33")
        checked=tk.IntVar()
        checkbutton = tk.Checkbutton(mwin,text="Edit default guess (parameter vector)",variable=checked,command=gray)
        checkbutton.place(x=10,y=270)
        gray()

        mwin.mainloop()

    def extract_measured_flux(self):
        assert self.switch == True, "Program terminated"
        import pandas as pd
        import numpy as np

        raw_magnitudes = ["F148W_AB","F169M_AB","F172M_AB","N219M_AB","N279N_AB","f275w_vega","f336w_vega","f475w_vega","f814w_vega","f110w_vega","f160w_vega"]
        raw_errors = ["F148W_err","F169M_err","F172M_err","N219M_err","N279N_err","f275w_err","f336w_err","f475w_err","f814w_err","f110w_err","f160w_err"]
        self.raw_magnitudes_dict = {"F148W":[None,None],"F169M":[None,None],"F172M":[None,None],"N219M":[None,None],"N279N":[None,None],"f275w":[None,None],"f336w":[None,None],"f475w":[None,None],"f814w":[None,None],"f110w":[None,None],"f160w":[None,None]}

        for rm,re,key in zip(raw_magnitudes,raw_errors,self.raw_magnitudes_dict):
            try:
                self.raw_magnitudes_dict[key][0] = self.measuredata.at[self.rownumber,"{}".format(rm)].item()
                self.raw_magnitudes_dict[key][1] = self.measuredata.at[self.rownumber,"{}".format(re)].item()
            except:
                self.raw_magnitudes_dict[key][0] = -999
                self.raw_magnitudes_dict[key][1] = -999

    def sift(self):
        self.valid_raw_magnitudes = {}
        for key in self.raw_magnitudes_dict:
            if self.raw_magnitudes_dict[key][0] != -999:
                self.valid_raw_magnitudes[key] = [self.raw_magnitudes_dict[key][0],self.raw_magnitudes_dict[key][1]]

    def convert_to_AB(self):
        for key in self.valid_raw_magnitudes:
            if key == "f275w":
                self.valid_raw_magnitudes[key][0] -= -1.496
            elif key == "f336w":
                self.valid_raw_magnitudes[key][0] -= -1.188
            elif key == "f475w":
                self.valid_raw_magnitudes[key][0] -= 0.091
            elif key == "f814w":
                self.valid_raw_magnitudes[key][0] -= -0.427
            elif key == "f110w":
                self.valid_raw_magnitudes[key][0] -= -0.7595
            elif key == "f160w":
                self.valid_raw_magnitudes[key][0] -= -1.2514
        
        self.valid_AB_magnitudes = self.valid_raw_magnitudes
                        
    def convert_to_bandflux(self):
        for key in self.valid_AB_magnitudes:
            self.valid_AB_magnitudes[key][0] = (10**(-0.4*(48.60+self.valid_AB_magnitudes[key][0])))*10**26
            self.valid_AB_magnitudes[key][1] = self.valid_AB_magnitudes[key][0]*self.valid_AB_magnitudes[key][1]/1.0857
        self.filternames = []
        self.bandfluxes = []
        self.bandfluxerrors = []
        for key in self.valid_AB_magnitudes:
            self.filternames.append(key)
            self.bandfluxes.append(self.valid_AB_magnitudes[key][0])
            self.bandfluxerrors.append(self.valid_AB_magnitudes[key][1])

    def prepare_for_interpolation(self):
        import xarray as xr
        ds_disk = xr.open_dataset("saved_on_disk.nc")
        self.da = ds_disk.to_array()
        self.filternumbers = []
        self.avgwvlist = []
        for name in self.filternames:
            if name == "F148W":
                self.filternumbers.append(0)
                self.avgwvlist.append(150.2491)
            elif name == "F169M":
                self.filternumbers.append(1)
                self.avgwvlist.append(161.4697)
            elif name == "F172M":
                self.filternumbers.append(2)
                self.avgwvlist.append(170.856)
            elif name == "N219M":
                self.filternumbers.append(3)
                self.avgwvlist.append(199.1508)
            elif name == "N279N":
                self.filternumbers.append(4)
                self.avgwvlist.append(276.0)
            elif name == "f275w":
                self.filternumbers.append(5)
                self.avgwvlist.append(267.884375)
            elif name == "f336w":
                self.filternumbers.append(6)
                self.avgwvlist.append(336.8484)
            elif name == "f475w":
                self.filternumbers.append(7)
                self.avgwvlist.append(476.0)
            elif name == "f814w":
                self.filternumbers.append(8)
                self.avgwvlist.append(833.0)
            elif name == "f110w":
                self.filternumbers.append(9)
                self.avgwvlist.append(1096.7245)
            elif name == "f160w":
                self.filternumbers.append(10)
                self.avgwvlist.append(1522.1981)


    def interpolate(self,g,T,Z):
        interpolist = []
        interpolated = self.da.interp(Abundance = Z, Temperature = T, Log_of_surface_gravity = g)
        
        for i,filterno in enumerate(self.filternumbers):
            interpolist.append(interpolated.sel(Filter = filterno).data.item()*10**8*(self.avgwvlist[i]*10**-7)**2/(2.998*10**10)*10**26)
        return interpolist
    
    def extinction(self):
        extinctlist = []
        extinct_all = [5.52548923, 5.17258596, 5.0540947, 5.83766858, 3.49917568, 3.25288368, 1.95999799, 0.62151591, -1.44589933, -2.10914243, -2.51310314]
        for filterno in self.filternumbers:
            extinctlist.append(extinct_all[filterno])         
        return extinctlist

    def minichisqfunc(self,tup):
        g, T, Z, theta_r, E_bv = tup
        print("g,T,Z,theta_r,E_bv", g,T,Z,theta_r,E_bv)
        self.best_models = []
        for i in range(len(self.filternames)):
            #print("{}th interpolated: ".format(i), self.interpolate(g,T,Z)[i])
            #print("{}th extinction: ".format(i), self.extinction()[i])
            self.best_models.append(self.interpolate(g,10000*T,Z)[i]*(theta_r*1e-12)**2*10**(-0.4*(E_bv*(self.extinction()[i]+3.001))))
        return self.best_models

    def chisqfunc(self,tup):
        g, T, Z, theta_r, E_bv = tup
        print("g,T,Z,theta_r,E_bv: ", g,T,Z,theta_r,E_bv)
        models = []
        for i in range(len(self.filternames)):
            #print("{}th interpolated: ".format(i), self.interpolate(g,T,Z)[i])
            #print("{}th extinction: ".format(i), self.extinction()[i])
            models.append(self.interpolate(g,10000*T,Z)[i]*(theta_r*1e-12)**2*10**(-0.4*(E_bv*(self.extinction()[i]+3.001))))
        #print("models ",models)
        summands = []
        printbands = []
        for ind in range(len(self.filternames)):
            #printbands.append(self.bandfluxes[ind])
            #print("{}th bferror".format(ind),self.bandfluxerrors[ind])
            summands.append(((self.bandfluxes[ind] - models[ind])/self.bandfluxerrors[ind])**2)
        #print("band fluxes", printbands)
        #print("summands ",summands)
        chisq = sum(summands)
        print("chisq: ",chisq,"\n")
        return chisq

    def minimize_chisq(self):
        #default guess: 4.5, 3.2, 0, 0.7368, 0.33
        bnds = ((3.5,5),(.35,3.1),(-2.5,.5),(0.03,30),(0,1))
        x0 = numpy.array([self.gguess,self.Tguess,self.Zguess,self.thetaguess,self.ebvguess])
        self.result =  opt.minimize(self.chisqfunc, x0, bounds=bnds)
        print("result:\n",self.result)

    def display_results(self):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        mwin = tk.Tk()
        mwin.geometry("1460x900+250+20")
        mwin.title("Optimization results")
        
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')

        fig = Figure(figsize=(10,7))
        abc = fig.add_subplot(111)
        best_tup = (self.result.x[0],self.result.x[1],self.result.x[2],self.result.x[3],self.result.x[4])
        abc.scatter(self.avgwvlist,self.bandfluxes,color="orange")
        abc.set_xlabel("Wavelength [nm]")
        abc.set_ylabel("Flux [mJy]")
        #abc.set_title("{}".format(self.star_name))
        abc.errorbar(self.avgwvlist,self.bandfluxes,yerr=self.bandfluxerrors,fmt="o",color="orange")
        abc.plot(self.avgwvlist,self.minichisqfunc(best_tup),color="blue")
        
        canvas = FigureCanvasTkAgg(fig, master=mwin)
        canvas.get_tk_widget().pack(anchor=tk.E)
        canvas.draw()

        label1 = tk.Label(mwin,text="Average wavelength of each filter (x):")
        label1.place(x=50,y=20)
        textbox1 = tk.Text(mwin,height=6,width=35)
        for filtername,avgwv in zip(self.filternames,self.avgwvlist):
            textbox1.insert(tk.END,"{}       {}\n".format(filtername,avgwv))
        textbox1.place(x=50,y=50)
        label2 = tk.Label(mwin,text="Bandfluxes (y, orange):")
        label2.place(x=50,y=220)
        textbox2 = tk.Text(mwin,height=6,width=35)
        for filtername,bf in zip(self.filternames,self.bandfluxes):
            textbox2.insert(tk.END,"{}       {}\n".format(filtername,bf))
        textbox2.place(x=50,y=250)
        label3 = tk.Label(mwin,text="Bandflux errors:")
        label3.place(x=50,y=420)
        textbox3 = tk.Text(mwin,height=6,width=35)
        for filtername,bfe in zip(self.filternames,self.bandfluxerrors):
            textbox3.insert(tk.END,"{}       {}\n".format(filtername,bfe))
        textbox3.place(x=50,y=450)
        label4 = tk.Label(mwin,text="Model fluxes (y, blue):")
        label4.place(x=50,y=620)
        textbox4 = tk.Text(mwin,height=6,width=35)
        for filtername,mod in zip(self.filternames,self.best_models):
            textbox4.insert(tk.END,"{}       {}\n".format(filtername,mod))
        textbox4.place(x=50,y=650)
        groove = tk.Canvas(mwin,width=350,height=120,bd=4,relief=tk.RIDGE)
        groove.place(x=455,y=740)
        label5 = tk.Label(mwin,text="Lowest chi^2 value")
        label5.place(x=470,y=750)
        label5a = tk.Label(mwin,text="{}".format(self.result.fun),font=("Arial",14))
        label5a.place(x=520,y=795)
        ridge = tk.Canvas(mwin,width=600,height=200,bd=4,relief=tk.GROOVE)
        ridge.place(x=930,y=700)
        label6 = tk.Label(mwin,text="Best fit parameters",pady=15)
        label6.place(x=880,y=790)
        label7 = tk.Label(mwin,text="log g                   =          {}".format(self.result.x[0]))
        label7.place(x=1080,y=730)
        label8= tk.Label(mwin,text = "temperature       =          {}".format(self.result.x[1]*10000))
        label8.place(x=1080,y=760)
        label9 = tk.Label(mwin, text = "abundance         =           {}".format(self.result.x[2]))
        label9.place(x=1080,y=790)
        label10 = tk.Label(mwin,text="theta_r                =           {}".format(self.result.x[3]*10**(-12)))
        label10.place(x=1080,y=820)
        label11 = tk.Label(mwin,text="E(b-v)                 =           {}".format(self.result.x[4]))
        label11.place(x=1080,y=850)
        mwin.mainloop()



go = ChiSquared()