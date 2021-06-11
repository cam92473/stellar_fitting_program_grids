import numpy
import scipy.optimize as opt
import pandas as pd

class ChiSquared():
    def __init__(self):
        self.intro_gui()
        self.extract_measured_flux()
        self.convert_to_AB()
        self.convert_to_bandflux()
        self.prepare_for_interpolation()
        self.minimize_chisq()
        self.save_output()
        self.display_all_results()

    
    def intro_gui(self):
        self.switch = False
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        mwin = tk.Tk()
        mwin.geometry("660x650+700+150")
        mwin.title("Stellar Fitting")
        mwin.resizable(0,0)

        def collectfilename():
            from tkinter import messagebox
            if user_filename.get() == "":
                tk.messagebox.showinfo('Error', 'Please enter a filename.')
                return None
            else:
                moveon = False

                if "," in user_rownumber.get():
                    rowlist = user_rownumber.get().split(',')
                    for elem in rowlist:
                        try:
                            rowint = int(elem)
                        except:
                            tk.messagebox.showinfo('Error', 'Please enter the number of rows with the correct syntax.')
                            return None
                        else:
                            introwlist = [int(i) for i in rowlist]
                            lowestelem = introwlist[0]
                            highestelem = introwlist[-1]
                            moveon = True

                elif ":" in user_rownumber.get():
                    rowlist = user_rownumber.get().split(':')
                    for elem in rowlist:
                        try:
                            rowint = int(elem)
                        except:
                            tk.messagebox.showinfo('Error', 'Please enter the number of rows with the correct syntax.')
                            return None
                        else:
                            import numpy as np
                            introwlist = np.arange(int(rowlist[0]),int(rowlist[-1])+1).tolist()
                            lowestelem = introwlist[0]
                            highestelem = introwlist[-1]
                            moveon = True
                
                else:
                    try:
                        rowint = int(user_rownumber.get())
                    except:
                        tk.messagebox.showinfo('Error', 'Please enter the number of rows with the correct syntax.')
                        return None
                    else:
                        introwlist = [rowint]
                        lowestelem = rowint
                        highestelem = rowint
                        moveon = True
                
                if moveon == True:
                    try:
                        import pandas as pd
                        self.measuredata = pd.read_csv("{}".format(user_filename.get(),delimiter=","))
                    except:
                        tk.messagebox.showinfo('Error', "Could not find file. Please place the file in the program folder and try again.")
                        return None
                    else:
                        if highestelem > len(self.measuredata)+1 or lowestelem < 2:
                            tk.messagebox.showinfo('Error', "Rows specified are out of range.")
                            return None
                        else:
                            if (checker2.get() == 1 and fluxname.get()[-4:] != ".csv") or (checker3.get() == 1 and chiname.get()[-4:] != ".csv"):
                                tk.messagebox.showinfo('Error', "The filenames specified are not allowed. Make sure to use the .csv extension.")
                                return None
                            elif checker4.get() == 1 and (imgname.get()[-4:] != ".png" and imgname.get()[-4:] != ".jpg"):
                                tk.messagebox.showinfo('Error', "The filenames specified are not allowed. Make sure to use the .png or .jpg extensions.")
                                return None
                            else:
                                try:
                                    a = int(fluxname.get()[0])
                                    b = int(chiname.get()[0])
                                    c = int(imgname.get()[0])
                                    return None
                                except:
                                    try:
                                        self.switch = True
                                        self.rows = [i-2 for i in introwlist]
                                        self.gguess1 = user_gguess1.get()
                                        self.Tguess1 = user_Tguess1.get()
                                        self.Zguess1 = user_Zguess1.get()
                                        self.thetaguess1 = user_thetaguess1.get()
                                        self.ebvguess1 = user_ebvguess1.get()

                                        self.dispresults = checker1.get()
                                        self.fluxresults = checker2.get()
                                        self.chiparams = checker3.get()
                                        self.saveplots = checker4.get()
                                        if checker2.get() == 1:
                                            self.fluxfilename = fluxname.get()
                                        if checker3.get() == 1:
                                            self.chifilename = chiname.get()
                                        if checker4.get() == 1:
                                            self.imgfilename = imgname.get()
                                        
                                        self.single_star = False
                                        self.double_star = False
                                        if user_Tguess2.get() == user_thetaguess2.get() == user_ebvguess2.get() == "N/A":
                                            self.single_star = True
                                        else:
                                            self.Tguess2 = float(user_Tguess2.get())
                                            self.thetaguess2 = float(user_thetaguess2.get())
                                            self.ebvguess2 = float(user_ebvguess2.get())
                                            self.double_star = True
                                    except:
                                            tk.messagebox.showinfo('Error', "One or more parameters seem to have been entered incorrectly. Please reenter the values and try again.")
                                            return None
                                    else:
                                        mwin.quit()
        user_filename = tk.StringVar()
        enterfileneame = tk.Entry(mwin,textvariable = user_filename,width=74)
        enterfileneame.place(x=20,y=60)
        user_rownumber = tk.StringVar()
        enterrownumberpack = tk.Frame(mwin)
        enterrownumberpack.place(x=20,y=190)
        enterrownumber = tk.Entry(enterrownumberpack,textvariable=user_rownumber,width=13)
        enterrownumber.pack(ipady=3)
        labelwhich = tk.Label(mwin,text="Read rows")
        labelwhich.place(x=20,y=160)
        from tkinter import messagebox
        def openrows():
            from tkinter import messagebox
            tk.messagebox.showinfo("Help","  •  Use csv row labelling (which should start at row 2)\n\n  •  Specify multiple rows with commas: 2,5,6\n\n  •  Specify a selection of rows with a colon: 3:8")
        whichbutton = tk.Button(mwin,text="?",font=("TimesNewRoman 8"),command = openrows)
        whichbutton.place(x=108,y=191)
        labeltop = tk.Label(mwin,text="Please enter filename to be read: ")
        labeltop.place(x=20,y=30)
        labelbot = tk.Label(mwin,text="e.g. \"filter_magnitudes.csv\"")
        labelbot.place(x=20,y=90)
        canvas2 = tk.Canvas(mwin,relief=tk.RIDGE,bd=2,width=395,height=270)
        canvas2.place(x=240,y=110)
        canvasline = tk.Canvas(mwin,bd=8,relief=tk.GROOVE,width=700,height=1000)
        canvasline.place(x=-20,y=400)
        user_gguess1 = tk.DoubleVar()
        user_Tguess1 = tk.DoubleVar()
        user_Zguess1 = tk.DoubleVar()
        user_thetaguess1 = tk.DoubleVar()
        user_ebvguess1 = tk.DoubleVar()
        ystar1labels = 480
        ystar1entries = 510
        ycheckbutton = 430
        labelg1 = tk.Label(mwin,text="log_g_hot").place(x=50,y=ystar1labels)
        entryg1 = tk.Entry(mwin,textvariable=user_gguess1,width=10)
        entryg1.place(x=50,y=ystar1entries)
        labelT1 = tk.Label(mwin,text="T_hot/10000").place(x=170,y=ystar1labels)
        entryT1 = tk.Entry(mwin,textvariable=user_Tguess1,width=10)
        entryT1.place(x=170,y=ystar1entries)
        labelZ1 = tk.Label(mwin,text="Z_hot").place(x=290,y=ystar1labels)
        entryZ1 = tk.Entry(mwin,textvariable=user_Zguess1,width=10)
        entryZ1.place(x=290,y=ystar1entries)
        labeltheta1 = tk.Label(mwin,text="θ_r_hot/1e-12").place(x=410,y=ystar1labels)
        entrytheta1 = tk.Entry(mwin,textvariable=user_thetaguess1,width=10)
        entrytheta1.place(x=410,y=ystar1entries)
        labelebv1 = tk.Label(mwin,text="E(B-V)_hot").place(x=530,y=ystar1labels)
        entryebv1 = tk.Entry(mwin,textvariable=user_ebvguess1,width=10)
        entryebv1.place(x=530,y=ystar1entries)

        ystar2labels = 560
        ystar2entries = 590
        user_Tguess2 = tk.StringVar()
        user_thetaguess2 = tk.StringVar()
        user_ebvguess2 = tk.StringVar()
        labelT2 = tk.Label(mwin,text="T_cool/10000").place(x=170,y=ystar2labels)
        entryT2 = tk.Entry(mwin,textvariable=user_Tguess2,width=10)
        entryT2.place(x=170,y=ystar2entries)
        labeltheta2 = tk.Label(mwin,text="θ_r_cool/1e-12").place(x=410,y=ystar2labels)
        entrytheta2 = tk.Entry(mwin,textvariable=user_thetaguess2,width=10)
        entrytheta2.place(x=410,y=ystar2entries)
        labelebv2 = tk.Label(mwin,text="E(B-V)_cool").place(x=530,y=ystar2labels)
        entryebv2 = tk.Entry(mwin,textvariable=user_ebvguess2,width=10)
        entryebv2.place(x=530,y=ystar2entries)
        
        starno_chosen = tk.StringVar()
        checked=tk.IntVar()

        def enable(howmany):
            entryg1['state'] = tk.NORMAL
            entryT1['state'] = tk.NORMAL
            entryZ1['state'] = tk.NORMAL
            entrytheta1['state'] = tk.NORMAL
            entryebv1['state'] = tk.NORMAL
            if howmany == "all":
                entryT2['state'] = tk.NORMAL
                entrytheta2['state'] = tk.NORMAL
                entryebv2['state'] = tk.NORMAL

        def disable(howmany):
            entryg1['state'] = tk.DISABLED
            entryT1['state'] = tk.DISABLED
            entryZ1['state'] = tk.DISABLED
            entrytheta1['state'] = tk.DISABLED
            entryebv1['state'] = tk.DISABLED
            if howmany == "all":
                entryT2['state'] = tk.DISABLED
                entrytheta2['state'] = tk.DISABLED
                entryebv2['state'] = tk.DISABLED


        def stuff_vals(useless):
            entrylist = [entryg1,entryT1,entryZ1,entrytheta1,entryebv1,entryT2,entrytheta2,entryebv2]
            if starno_chosen.get() == "     1-star fit     ":
                starlist1 = ["4.5","3.2","0","0.7368","0.33","N/A","N/A","N/A"]
                enable("all")
                for i,entry in enumerate(entrylist):
                    entry.delete(0,20)
                    entry.insert(0,"{}".format(starlist1[i]))
                disable("all")
                if checked.get() == 1:
                    enable("some")
            elif starno_chosen.get() == "     2-star fit     ":
                starlist2 = ["4.5","1.2","-1.0","0.088417","0.15","0.375","2.947242","0.15"]
                enable("all")
                for i,entry in enumerate(entrylist):
                    entry.delete(0,20)
                    entry.insert(0,"{}".format(starlist2[i]))
                disable("all")
                if checked.get() == 1:
                    enable("all")

        def gray():
            if starno_chosen.get() == "     1-star fit     ":
                if entryg1['state'] == tk.NORMAL:
                    disable("some")
                elif entryg1['state'] == tk.DISABLED:
                    enable("some")
            elif starno_chosen.get() == "     2-star fit     ":
                if entryg1['state'] == tk.NORMAL:
                    disable("all")
                elif entryg1['state'] == tk.DISABLED:
                    enable("all")
           
        starlabel = tk.Label(mwin,text="Fitting method").place(x=20,y=300)
        starno_chosen.set("     1-star fit     ")
        staroptions = ["     1-star fit     ","     2-star fit     "]
        starmenu = tk.OptionMenu(mwin,starno_chosen,*staroptions,command=stuff_vals)
        starmenu.place(x=20,y=330)
        gobutton = tk.Button(mwin,text="Fit data",font=("Arial",10),command = collectfilename,pady=15,padx=25,bd=3)
        gobutton.place(x=500,y=130)
        checker1 = tk.IntVar()
        checker2 = tk.IntVar()
        checker3 = tk.IntVar()
        checker4 = tk.IntVar()
        fluxname = tk.StringVar()
        chiname = tk.StringVar()
        imgname = tk.StringVar()

        def grent2():
            if buttentry2['state'] == tk.NORMAL:
                buttentry2.delete(0,30)
                buttentry2['state'] = tk.DISABLED
            elif buttentry2['state'] == tk.DISABLED:
                buttentry2['state'] = tk.NORMAL
                buttentry2.insert(tk.END,"flux_results.csv")
        def grent3():
            if buttentry3['state'] == tk.NORMAL:
                buttentry3.delete(0,30)
                buttentry3['state'] = tk.DISABLED
            elif buttentry3['state'] == tk.DISABLED:
                buttentry3['state'] = tk.NORMAL
                buttentry3.insert(tk.END,"chi_params.csv")
        def grent4():
            if buttentry4['state'] == tk.NORMAL:
                buttentry4.delete(0,30)
                buttentry4['state'] = tk.DISABLED
            elif buttentry4['state'] == tk.DISABLED:
                buttentry4['state'] = tk.NORMAL
                buttentry4.insert(tk.END,"plot_so_rowX.png")
                
        checkbutt1 = tk.Checkbutton(mwin,text="Display results",variable=checker1)
        checkbutt2 = tk.Checkbutton(mwin,text="Save resulting flux data",variable=checker2,command=grent2)
        checkbutt3 = tk.Checkbutton(mwin,text="Save chi^2 and minimized parameters",variable=checker3,command=grent3)
        checkbutt4 = tk.Checkbutton(mwin,text="Save plot images (1 per source X)",variable=checker4,command=grent4)
        buttentry2 = tk.Entry(mwin, textvariable = fluxname,width=20)
        buttentry3 = tk.Entry(mwin, textvariable = chiname,width=20)
        buttentry4 = tk.Entry(mwin,textvariable = imgname,width=20)
        buttentry2['state'] = tk.DISABLED
        buttentry3['state'] = tk.DISABLED
        buttentry4['state'] = tk.DISABLED
        checkbutt1.place(x=270,y=130)
        checkbutt2.place(x=270,y=175)
        checkbutt3.place(x=270,y=245)
        checkbutt4.place(x=270,y=315)
        buttentry2.place(x=275,y=205)
        buttentry3.place(x=275,y=275)
        buttentry4.place(x=275,y=345)
        #notelabel = tk.Label(mwin,font = "TkDefaultFont 7",text="*jpg is also allowed").place(x=450,y=351)
        checkbutt1.toggle()
        checkbutt2.toggle()
        checkbutt3.toggle()
        checkbutt4.toggle()
        grent2()
        grent3()
        grent4()
        checkbutton = tk.Checkbutton(mwin,text="Edit default guess (parameter vector)",variable=checked,command=gray)
        checkbutton.place(x=10,y=ycheckbutton)
        disable("all")
        stuff_vals(3)
        mwin.mainloop()

    def extract_measured_flux(self):
        assert self.switch == True, "Program terminated"
        import pandas as pd
        import numpy as np
        import tkinter as tk

        raw_columns = ["F148W_AB","F148W_err","F169M_AB","F169M_err","F172M_AB","F172M_err","N219M_AB","N219M_err","N279N_AB","N279N_err","f275w_vega","f275w_err","f336w_vega","f336w_err","f475w_vega","f475w_err","f814w_vega","f814w_err","f110w_vega","f110w_err","f160w_vega","f160w_err"]

        self.raw_magnitudes_frame = pd.DataFrame()
        for rawname in raw_columns:
            self.raw_magnitudes_frame["{}".format(rawname)] = ""

        savebadcols = []
        for rowno in self.rows:
            curr_rowdict = {}
            for colname in raw_columns:
                try:
                    curr_rowdict[colname] = self.measuredata.at[rowno,colname].item()
                except:
                    curr_rowdict[colname] = -999
                    savebadcols.append(colname)
            self.raw_magnitudes_frame.loc[self.raw_magnitudes_frame.shape[0]] = curr_rowdict

        savebadcols = list(dict.fromkeys(savebadcols))
        badstr = ""
        for badcol in savebadcols:
            badstr += "{} or ".format(badcol)
        badstr = badstr[:-4]

        if len(badstr) != 0:
            response = tk.messagebox.askquestion('Warning',"No entries found for {}. Do you wish to proceed?\n\n(These filters will not be fitted. If a single column is missing without its error or vice versa, you should double check the file for naming typos)".format(badstr))
            assert response == "yes", "Program terminated"

        for rowind,row in self.raw_magnitudes_frame.iterrows():
            for colind,colelement in enumerate(row):
                if colelement == -999:
                    self.raw_magnitudes_frame.iat[rowind,colind] = np.nan


    def convert_to_AB(self):
        self.ab_magnitudes_frame = self.raw_magnitudes_frame
        for col in self.ab_magnitudes_frame:
                if col == "f275w_vega":
                    self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-1.496))
                elif col == "f336w_vega":
                     self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-1.188))
                elif col == "f475w_vega":
                     self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - 0.091)
                elif col == "f814w_vega":
                     self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-0.427))
                elif col == "f110w_vega":
                     self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-0.7595))
                elif col == "f160w_vega":
                     self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-1.2514))
        
        self.ab_magnitudes_frame.rename(columns={"f275w_vega" : "f275w_AB", "f336w_vega" : "f336w_AB", "f475w_vega" : "f475w_AB", "f814w_vega" : "f814w_AB", "f110w_vega" : "f110w_AB", "f160w_vega" : "f160w_AB"},inplace=True)

    def convert_to_bandflux(self):
        self.filternames = ["F148W","F169M","F172M","N219M","N279N","f275w","f336w","f475w","f814w","f814w","f110w","f160w"]
        self.bandfluxes = pd.DataFrame()
        self.bandfluxerrors = pd.DataFrame()
        self.avgwvlist = [150.2491,161.4697,170.856,199.1508,276.0,267.884375,336.8484,476.0,833.0,1096.7245,1522.1981]
        self.allextinct = [5.52548923, 5.17258596, 5.0540947, 5.83766858, 3.49917568, 3.25288368, 1.95999799, 0.62151591, -1.44589933, -2.10914243, -2.51310314]

        for colind,col in enumerate(self.ab_magnitudes_frame):
            if colind%2 == 0:
                self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: (10**(-0.4*(48.60+x)))*10**26)
                self.bandfluxes["{}".format(col)] = self.ab_magnitudes_frame[col]
            elif colind%2 != 0:
                for rowind in range(len(self.ab_magnitudes_frame[col])):
                    self.ab_magnitudes_frame.iloc[rowind,colind] = self.ab_magnitudes_frame.iloc[rowind,colind-1]*self.ab_magnitudes_frame.iloc[rowind,colind]/1.0857
                self.bandfluxerrors["{}".format(col)] = self.ab_magnitudes_frame[col]
        


    def prepare_for_interpolation(self):
        import xarray as xr
        import numpy as np
        ds_disk = xr.open_dataset("saved_on_disk.nc")
        self.da = ds_disk.to_array()

    def interpolate(self,g,T,Z,valid_filters_this_row):
        interpolist = []
        interpolated = self.da.interp(Abundance = Z, Temperature = T, Log_of_surface_gravity = g)
        for valid_filter in valid_filters_this_row:
            interpolist.append(interpolated.sel(Filter = valid_filter).data.item()*10**8*(self.avgwvlist[valid_filter]*10**-7)**2/(2.998*10**10)*10**26)
        return interpolist
    
    def extinction(self,valid_filters_this_row):
        extinctlist = []
        for valid_filter in valid_filters_this_row:
            extinctlist.append(self.allextinct[valid_filter])
        return extinctlist

    def minichisqfunc_single(self,tup,valid_filters_this_row):
        g, T, Z, theta_r_sq, E_bv = tup
      
        best_models = []
        interpolist = self.interpolate(g,10000*T,Z,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            best_models.append(interpolist[i]*(theta_r_sq*1e-24)*10**(-0.4*(E_bv*(extinctolist[i]+3.001))))
        
        return best_models

    def minichisqfunc_double(self,tup,valid_filters_this_row):
        g1, T1, Z1, theta_r1_sq, E_bv1, T2, theta_r2_sq, E_bv2 = tup
      
        bestmodels1 = []
        interpolist1 = self.interpolate(g1,10000*T1,Z1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            bestmodels1.append(interpolist1[i]*(theta_r1_sq*1e-24)*10**(-0.4*(E_bv1*(extinctolist1[i]+3.001))))
        bestmodels2 = []
        interpolist2 = self.interpolate(2.5,10000*T2,-1.5,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            bestmodels2.append(interpolist2[i]*(theta_r2_sq*1e-24)*10**(-0.4*(E_bv2*(extinctolist2[i]+3.001))))
        
        return bestmodels1,bestmodels2


    def chisqfunc(self,tup,valid_filters_this_row,curr_row):
        g, T, Z, theta_r_sq, E_bv = tup
        print("Testing row {} with g1, T1, Z1, theta_r1_sq, E_bv1: ".format(self.rows[curr_row]+2), g,T,Z,theta_r_sq,E_bv)

        models = []
        interpolist = self.interpolate(g,10000*T,Z,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models.append(interpolist[i]*(theta_r_sq*1e-24)*10**(-0.4*(E_bv*(extinctolist[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)
        print("chisq: ",chisq,"\n")

        return chisq

    def chisqfunc2(self,tup,valid_filters_this_row,curr_row):
        g1, T1, Z1, theta_r1_sq, E_bv1, T2, theta_r2_sq, E_bv2 = tup
        print("Testing row {} with g1, T1, Z1, theta_r1_sq, E_bv1, T2, theta_r2_sq, E_bv2: ".format(self.rows[curr_row]+2), g1, T1, Z1, theta_r1_sq, E_bv1, T2, theta_r2_sq, E_bv2)

        models1 = []
        interpolist1 = self.interpolate(g1,10000*T1,Z1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(interpolist1[i]*(theta_r1_sq*1e-24)*10**(-0.4*(E_bv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(2.5,10000*T2,-1.5,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(interpolist2[i]*(theta_r2_sq*1e-24)*10**(-0.4*(E_bv2*(extinctolist2[i]+3.001))))

        summands = []
        printbands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i] - models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)
        print("chisq: ",chisq,"\n")
        return chisq

    def minimize_chisq(self):
        import numpy as np
        
        if self.single_star == True:
            #default guess: 4.5, 3.2, 0, 0.7368, 0.33
            bnds = ((3.5,5),(.35,3.1),(-2.5,.5),(0.03,30),(0,1))
            x0 = np.array([self.gguess1,self.Tguess1,self.Zguess1,self.thetaguess1**2,self.ebvguess1])
            self.results = []

            for curr_row in range(self.bandfluxes.shape[0]): 
                valid_filters_this_row = []
                for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
                    if np.isnan(bandflux) == False:
                        valid_filters_this_row.append(valid_ind)
                self.results.append(opt.minimize(self.chisqfunc, x0, args=(valid_filters_this_row,curr_row,), bounds=bnds))
            print("results:\n",self.results)
        
        elif self.double_star == True:
            #default guess: 4.5, 1.2, -1.0, 0.088417, 0.15, 0.375, 2.947242, 0.15  
            bnds = ((3.5,5),(.65,3.1),(-2.5,.5),(0.03,30),(0,1),(.35,.55),(.03,30),(0,1))
            x0 = np.array([self.gguess1,self.Tguess1,self.Zguess1,self.thetaguess1**2,self.ebvguess1,self.Tguess2,self.thetaguess2**2,self.ebvguess2])
            self.results = []

            for curr_row in range(self.bandfluxes.shape[0]):  
                valid_filters_this_row = []
                for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
                    if np.isnan(bandflux) == False:
                        valid_filters_this_row.append(valid_ind)
                self.results.append(opt.minimize(self.chisqfunc2, x0, args=(valid_filters_this_row,curr_row,), bounds=bnds))


    def display_all_results(self):
        if self.dispresults == 1:
            if self.single_star == True:
                for curr_row in range(self.bandfluxes.shape[0]): 
                    self.display_results_single(curr_row)
            elif self.double_star == True:
                for curr_row in range(self.bandfluxes.shape[0]): 
                    self.display_results_double(curr_row)

    def save_output(self):
        import pandas as pd

        if self.fluxresults == 1:
            import numpy as np
            import pandas as pd
            
            if self.single_star == True:

                models = self.bandfluxes.copy(deep=True)
                for curr_row in range(self.bandfluxes.shape[0]):
                    valid_filters_this_row = []
                    for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
                        if np.isnan(bandflux) == False:
                            valid_filters_this_row.append(valid_ind)

                    best_tup = (self.results[curr_row].x[0],self.results[curr_row].x[1],self.results[curr_row].x[2],self.results[curr_row].x[3],self.results[curr_row].x[4])
                    model = self.minichisqfunc_single(best_tup,valid_filters_this_row)
                    used = 0 
                    for colno,col in enumerate(models.loc[curr_row,:]):
                        if np.isnan(col) == False:
                            models.iat[curr_row,colno] = model[used]
                            used += 1
                         
                colnames = {"F148W_meas_flux [mJy]" : [], "F148W_err [mJy]" : [], "F148W_avg_wav [nm]" : [], "F148W_model_flux [mJy]" : [], "F169M_meas_flux [mJy]" : [], "F169M_err [mJy]" : [], "F169M_avg_wav [nm]" : [], "F169M_model_flux [mJy]" : [], "F172M_meas_flux [mJy]" : [], "F172M_err [mJy]" : [], "F172M_avg_wav [nm]" : [], "F172M_model_flux [mJy]" : [], "N219M_meas_flux [mJy]" : [], "N219M_err [mJy]" : [], "N219M_avg_wav [nm]" : [], "N219M_model_flux [mJy]" : [], "N279N_meas_flux [mJy]" : [], "N279N_err [mJy]" : [], "N279N_avg_wav [nm]" : [], "N279N_model_flux [mJy]" : [], "f275w_meas_flux [mJy]" : [], "f275w_err [mJy]" : [], "f275w_avg_wav [nm]" : [], "f275w_model_flux [mJy]" : [], "f336w_meas_flux [mJy]" : [], "f336w_err [mJy]" : [], "f336w_avg_wav [nm]" : [], "f336w_model_flux [mJy]" : [], "f475w_meas_flux [mJy]" : [], "f475w_err [mJy]" : [], "f475w_avg_wav [nm]" : [], "f475w_model_flux [mJy]" : [], "f814w_meas_flux [mJy]" : [], "f814w_err [mJy]" : [], "f814w_avg_wav [nm]" : [], "f814w_model_flux [mJy]" : [], "f110w_meas_flux [mJy]" : [], "f110w_err [mJy]" : [], "f110w_avg_wav [nm]" : [], "f110w_model_flux [mJy]" : [], "f160w_meas_flux [mJy]" : [], "f160w_err [mJy]" : [], "f160w_avg_wav [nm]" : [], "f160w_model_flux [mJy]" : []}
                fluxresultsdf = pd.DataFrame(colnames)
                for curr_row in range(self.bandfluxes.shape[0]):
                    rowdict = {"F148W_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,0], "F148W_err [mJy]" : self.bandfluxerrors.iat[curr_row,0], "F148W_avg_wav [nm]" : self.avgwvlist[0], "F148W_model_flux [mJy]" : models.iat[curr_row,0], "F169M_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,1], "F169M_err [mJy]" : self.bandfluxerrors.iat[curr_row,1], "F169M_avg_wav [nm]" : self.avgwvlist[1], "F169M_model_flux [mJy]" : models.iat[curr_row,1], "F172M_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,2], "F172M_err [mJy]" : self.bandfluxerrors.iat[curr_row,2], "F172M_avg_wav [nm]" : self.avgwvlist[2], "F172M_model_flux [mJy]" : models.iat[curr_row,2], "N219M_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,3], "N219M_err [mJy]" : self.bandfluxerrors.iat[curr_row,3], "N219M_avg_wav [nm]" : self.avgwvlist[3], "N219M_model_flux [mJy]" : models.iat[curr_row,3], "N279N_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,4], "N279N_err [mJy]" : self.bandfluxerrors.iat[curr_row,4], "N279N_avg_wav [nm]" : self.avgwvlist[4], "N279N_model_flux [mJy]" : models.iat[curr_row,4], "f275w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,5], "f275w_err [mJy]" : self.bandfluxerrors.iat[curr_row,5], "f275w_avg_wav [nm]" : self.avgwvlist[5], "f275w_model_flux [mJy]" : models.iat[curr_row,5], "f336w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,6], "f336w_err [mJy]" : self.bandfluxerrors.iat[curr_row,6], "f336w_avg_wav [nm]" : self.avgwvlist[6], "f336w_model_flux [mJy]" : models.iat[curr_row,6], "f475w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,7], "f475w_err [mJy]" : self.bandfluxerrors.iat[curr_row,7], "f475w_avg_wav [nm]" : self.avgwvlist[7], "f475w_model_flux [mJy]" : models.iat[curr_row,7], "f814w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,8], "f814w_err [mJy]" : self.bandfluxerrors.iat[curr_row,8], "f814w_avg_wav [nm]" : self.avgwvlist[8], "f814w_model_flux [mJy]" : models.iat[curr_row,8], "f110w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,9], "f110w_err [mJy]" : self.bandfluxerrors.iat[curr_row,9], "f110w_avg_wav [nm]" : self.avgwvlist[9], "f110w_model_flux [mJy]" : models.iat[curr_row,9], "f160w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,10], "f160w_err [mJy]" : self.bandfluxerrors.iat[curr_row,10], "f160w_avg_wav [nm]" : self.avgwvlist[10], "f160w_model_flux [mJy]" : models.iat[curr_row,10]}
                    fluxresultsdf =fluxresultsdf.append(rowdict,ignore_index=True)
                for curr_row in range(self.bandfluxes.shape[0]):
                    fluxresultsdf = fluxresultsdf.rename(index={curr_row:"Source at row {}".format(self.rows[curr_row]+2)})
                try:
                    fluxresultsdf.to_csv("{}".format(self.fluxfilename))
                except:
                    import tkinter as tk
                    from tkinter import messagebox
                    tk.messagebox.showerror('Error','An error occurred. Sometimes this can happen when trying to overwrite a file. Please remove output files from the program folder and try again.')  
            
            
            elif self.double_star == True:

                hotmodels = self.bandfluxes.copy(deep=True)
                coolmodels = self.bandfluxes.copy(deep=True)
                for curr_row in range(self.bandfluxes.shape[0]):
                    valid_filters_this_row = []
                    for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
                        if np.isnan(bandflux) == False:
                            valid_filters_this_row.append(valid_ind)

                    best_tup = (self.results[curr_row].x[0],self.results[curr_row].x[1],self.results[curr_row].x[2],self.results[curr_row].x[3],self.results[curr_row].x[4],self.results[curr_row].x[5],self.results[curr_row].x[6],self.results[curr_row].x[7])
                    hot,cool = self.minichisqfunc_double(best_tup,valid_filters_this_row)
                    usedhot = 0
                    usedcool = 0
                    for colno,col in enumerate(hotmodels.loc[curr_row,:]):
                        if np.isnan(col) == False:
                            hotmodels.iat[curr_row,colno] = hot[usedhot]
                            usedhot += 1
                    for colno,col in enumerate(coolmodels.loc[curr_row,:]):
                        if np.isnan(col) == False:
                            coolmodels.iat[curr_row,colno] = cool[usedcool]
                            usedcool += 1
                
                colnames = {"F148W_meas_flux [mJy]" : [], "F148W_err [mJy]" : [], "F148W_avg_wav [nm]" : [], "F148W_hot_flux" : [], "F148W_cool_flux" : [], "F169M_meas_flux [mJy]" : [], "F169M_err [mJy]" : [], "F169M_avg_wav [nm]" : [], "F169M_hot_flux [mJy]" : [], "F169M_cool_flux [mJy]" : [], "F172M_meas_flux [mJy]" : [], "F172M_err [mJy]" : [], "F172M_avg_wav [nm]" : [], "F172M_hot_flux [mJy]" : [], "F172M_cool_flux [mJy]" : [], "N219M_meas_flux [mJy]" : [], "N219M_err [mJy]" : [], "N219M_avg_wav [nm]" : [], "N219M_hot_flux [mJy]" : [], "N219M_cool_flux [mJy]" : [], "N279N_meas_flux [mJy]" : [], "N279N_err [mJy]" : [], "N279N_avg_wav [nm]" : [], "N279N_hot_flux [mJy]" : [], "N279N_cool_flux [mJy]" : [], "f275w_meas_flux [mJy]" : [], "f275w_err [mJy]" : [], "f275w_avg_wav [nm]" : [], "f275w_hot_flux [mJy]" : [], "f275w_cool_flux [mJy]" : [], "f336w_meas_flux [mJy]" : [], "f336w_err [mJy]" : [], "f336w_avg_wav [nm]" : [], "f336w_hot_flux [mJy]" : [], "f336w_cool_flux [mJy]" : [], "f475w_meas_flux [mJy]" : [], "f475w_err [mJy]" : [], "f475w_avg_wav [nm]" : [], "f475w_hot_flux [mJy]" : [], "f475w_cool_flux [mJy]" : [], "f814w_meas_flux [mJy]" : [], "f814w_err [mJy]" : [], "f814w_avg_wav [nm]" : [], "f814w_hot_flux [mJy]" : [], "f814w_cool_flux [mJy]" : [], "f110w_meas_flux [mJy]" : [], "f110w_err [mJy]" : [], "f110w_avg_wav [nm]" : [], "f110w_hot_flux [mJy]" : [], "f110w_cool_flux [mJy]" : [], "f160w_meas_flux [mJy]" : [], "f160w_err [mJy]" : [], "f160w_avg_wav [nm]" : [], "f160w_hot_flux [mJy]" : [], "f160w_cool_flux [mJy]" : []}
                fluxresultsdf = pd.DataFrame(colnames)
                for curr_row in range(self.bandfluxes.shape[0]):
                    rowdict = {"F148W_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,0], "F148W_err [mJy]" : self.bandfluxerrors.iat[curr_row,0], "F148W_avg_wav [nm]" : self.avgwvlist[0], "F148W_hot_flux" : hotmodels.iat[curr_row,0], "F148W_cool_flux" : coolmodels.iat[curr_row,0], "F169M_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,1], "F169M_err [mJy]" : self.bandfluxerrors.iat[curr_row,1], "F169M_avg_wav [nm]" : self.avgwvlist[1], "F169M_hot_flux [mJy]" : hotmodels.iat[curr_row,1], "F169M_cool_flux [mJy]" : coolmodels.iat[curr_row,1], "F172M_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,2], "F172M_err [mJy]" : self.bandfluxerrors.iat[curr_row,2], "F172M_avg_wav [nm]" : self.avgwvlist[2], "F172M_hot_flux [mJy]" : hotmodels.iat[curr_row,2], "F172M_cool_flux [mJy]" : coolmodels.iat[curr_row,2], "N219M_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,3], "N219M_err [mJy]" : self.bandfluxerrors.iat[curr_row,3], "N219M_avg_wav [nm]" : self.avgwvlist[3], "N219M_hot_flux [mJy]" : hotmodels.iat[curr_row,3], "N219M_cool_flux [mJy]" : coolmodels.iat[curr_row,3], "N279N_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,4], "N279N_err [mJy]" : self.bandfluxerrors.iat[curr_row,4], "N279N_avg_wav [nm]" : self.avgwvlist[4], "N279N_hot_flux [mJy]" : hotmodels.iat[curr_row,4], "N279N_cool_flux [mJy]" : coolmodels.iat[curr_row,4], "f275w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,5], "f275w_err [mJy]" : self.bandfluxerrors.iat[curr_row,5], "f275w_avg_wav [nm]" : self.avgwvlist[5], "f275w_hot_flux [mJy]" : hotmodels.iat[curr_row,5], "f275w_cool_flux [mJy]" : coolmodels.iat[curr_row,5], "f336w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,6], "f336w_err [mJy]" : self.bandfluxerrors.iat[curr_row,6], "f336w_avg_wav [nm]" : self.avgwvlist[6], "f336w_hot_flux [mJy]" : hotmodels.iat[curr_row,6], "f336w_cool_flux [mJy]" : coolmodels.iat[curr_row,6], "f475w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,7], "f475w_err [mJy]" : self.bandfluxerrors.iat[curr_row,7], "f475w_avg_wav [nm]" : self.avgwvlist[7], "f475w_hot_flux [mJy]" : hotmodels.iat[curr_row,7], "f475w_cool_flux [mJy]" : coolmodels.iat[curr_row,7], "f814w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,8], "f814w_err [mJy]" : self.bandfluxerrors.iat[curr_row,8], "f814w_avg_wav [nm]" : self.avgwvlist[8], "f814w_hot_flux [mJy]" : hotmodels.iat[curr_row,8], "f814w_cool_flux [mJy]" : coolmodels.iat[curr_row,8], "f110w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,9], "f110w_err [mJy]" : self.bandfluxerrors.iat[curr_row,9], "f110w_avg_wav [nm]" : self.avgwvlist[9], "f110w_hot_flux [mJy]" : hotmodels.iat[curr_row,9], "f110w_cool_flux [mJy]" : coolmodels.iat[curr_row,9], "f160w_meas_flux [mJy]" : self.bandfluxes.iat[curr_row,10], "f160w_err [mJy]" : self.bandfluxerrors.iat[curr_row,10], "f160w_avg_wav [nm]" : self.avgwvlist[10], "f160w_hot_flux [mJy]" : hotmodels.iat[curr_row,10], "f160w_cool_flux [mJy]" : coolmodels.iat[curr_row,10]}
                    fluxresultsdf =fluxresultsdf.append(rowdict,ignore_index=True)
                for curr_row in range(self.bandfluxes.shape[0]):
                    fluxresultsdf = fluxresultsdf.rename(index={curr_row:"Source at row {}".format(self.rows[curr_row]+2)})
                try:
                    fluxresultsdf.to_csv("{}".format(self.fluxfilename))
                except:
                    import tkinter as tk
                    from tkinter import messagebox
                    tk.messagebox.showerror('Error','An error occurred. Sometimes this can happen when trying to overwrite a file. Please remove output files from the program folder and try again.')         


        if self.chiparams == 1:
            
            if self.single_star == True:
                import math
                colnames = {'minimized chi^2' : [], 'log_g' : [], 'temperature' : [], 'abundance' : [], 'theta_r' : [], 'E(B-V)' : []}
                chiparamsdf = pd.DataFrame(colnames).copy(deep=True)
                for curr_row in range(self.bandfluxes.shape[0]):
                    rowdict = {'minimized chi^2' : self.results[curr_row].fun, 'log_g' : self.results[curr_row].x[0], 'temperature' : self.results[curr_row].x[1]*10000, 'abundance' : self.results[curr_row].x[2], 'theta_r' : math.sqrt(self.results[curr_row].x[3])*1e-12, 'E(B-V)' : self.results[curr_row].x[4]}
                    chiparamsdf = chiparamsdf.append(rowdict,ignore_index=True)
                for curr_row in range(self.bandfluxes.shape[0]):
                    chiparamsdf = chiparamsdf.rename(index={curr_row:"Source at row {}".format(self.rows[curr_row]+2)})
                try:
                    chiparamsdf.to_csv("{}".format(self.chifilename))
                except:
                    import tkinter as tk
                    from tkinter import messagebox
                    tk.messagebox.showerror('Error','An error occurred. Sometimes this can happen when trying to overwrite a file. Please remove output files from the program folder and try again.')         
            
            elif self.double_star == True:
                import math
                colnames = {'minimized chi^2' : [], 'log_g_hot' : [], 'temperature_hot' : [], 'abundance_hot' : [], 'theta_r_hot' : [], 'E(B-V)_hot' : [], 'temperature_cool' : [], 'theta_r_cool' : [], 'E(B-V)_cool' : []}
                chiparamsdf = pd.DataFrame(colnames).copy(deep=True)
                for curr_row in range(self.bandfluxes.shape[0]):
                    rowdict = {'minimized chi^2' : self.results[curr_row].fun, 'log_g_hot' : self.results[curr_row].x[0], 'temperature_hot' : self.results[curr_row].x[1]*10000, 'abundance_hot' : self.results[curr_row].x[2], 'theta_r_hot' : math.sqrt(self.results[curr_row].x[3])*1e-12, 'E(B-V)_hot' : self.results[curr_row].x[4], 'temperature_cool' : self.results[curr_row].x[5]*10000, 'theta_r_cool' : math.sqrt(self.results[curr_row].x[6])*1e-12, 'E(B-V)_cool' : self.results[curr_row].x[7]}
                    chiparamsdf = chiparamsdf.append(rowdict,ignore_index=True)
                for curr_row in range(self.bandfluxes.shape[0]):
                    chiparamsdf = chiparamsdf.rename(index={curr_row:"Source at row {}".format(self.rows[curr_row]+2)})
                try:
                    chiparamsdf.to_csv("{}".format(self.chifilename))
                except:
                    import tkinter as tk
                    from tkinter import messagebox
                    tk.messagebox.showerror('Error','An error occurred. Sometimes this can happen when trying to overwrite a file. Please remove output files from the program folder and try again.')         
            
    def display_results_single(self,curr_row):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        topw = tk.Toplevel()
        topw.geometry("1460x900+250+20")
        topw.title("Optimization results")
        topw.resizable(0,0)
        
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')
        import numpy as np

        valid_filters_this_row = []
        for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
            if np.isnan(bandflux) == False:
                valid_filters_this_row.append(valid_ind)
        
        valid_fluxes_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])

        valid_errors_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_errors_this_row.append(self.bandfluxerrors.iat[curr_row,valid_ind])    

        valid_avgwv_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_avgwv_this_row.append(self.avgwvlist[valid_ind])
    

        fig = Figure(figsize=(10.5,6))
        abc = fig.add_subplot(111)
        best_tup = (self.results[curr_row].x[0],self.results[curr_row].x[1],self.results[curr_row].x[2],self.results[curr_row].x[3],self.results[curr_row].x[4])
        abc.scatter(valid_avgwv_this_row,valid_fluxes_this_row,color="orange")
        abc.set_xlabel("Wavelength [nm]")
        abc.set_ylabel("Flux [mJy]")
        abc.set_title("Source at row {}".format(self.rows[curr_row]+2))
        abc.errorbar(valid_avgwv_this_row,valid_fluxes_this_row,yerr=valid_errors_this_row,fmt="o",color="orange")
        abc.plot(valid_avgwv_this_row,self.minichisqfunc_single(best_tup,valid_filters_this_row),color="blue")

        if self.saveplots == 1:
            saveimgname = self.imgfilename.replace("X","{}".format(self.rows[curr_row]+2))
            fig.savefig('{}'.format(saveimgname), bbox_inches='tight', dpi=150)

        canvas = FigureCanvasTkAgg(fig, master=topw)
        canvas.get_tk_widget().pack(anchor=tk.E)
        canvas.draw()

        label1 = tk.Label(topw,text="Average wavelength of each filter (x):")
        label1.place(x=50,y=20)
        textbox1 = tk.Text(topw,height=6,width=30)
        for filtername,avgwv in zip(self.filternames,valid_avgwv_this_row):
            textbox1.insert(tk.END,"{}      {}\n".format(filtername,avgwv))
        textbox1.place(x=50,y=50)
        label2 = tk.Label(topw,text="Bandfluxes (y, orange):")
        label2.place(x=50,y=220)
        textbox2 = tk.Text(topw,height=6,width=30)
        for filtername,bf in zip(self.filternames,valid_fluxes_this_row):
            textbox2.insert(tk.END,"{}      {}\n".format(filtername,format(bf,'.8e')))
        textbox2.place(x=50,y=250)
        label3 = tk.Label(topw,text="Bandflux errors:")
        label3.place(x=50,y=420)
        textbox3 = tk.Text(topw,height=6,width=30)
        for filtername,bfe in zip(self.filternames,valid_errors_this_row):
            textbox3.insert(tk.END,"{}      {}\n".format(filtername,format(bfe,'.8e')))
        textbox3.place(x=50,y=450)
        label4 = tk.Label(topw,text="Model fluxes (y, blue):")
        label4.place(x=50,y=620)
        textbox4 = tk.Text(topw,height=6,width=30)
        for filtername,mod in zip(self.filternames,self.minichisqfunc_single(best_tup,valid_filters_this_row)):
            textbox4.insert(tk.END,"{}      {}\n".format(filtername,format(mod,'.8e')))
        textbox4.place(x=50,y=650)
        groove = tk.Canvas(topw,width=350,height=120,bd=4,relief=tk.RIDGE)
        groove.place(x=435,y=655)
        label5 = tk.Label(topw,text="Lowest chi^2 value")
        label5.place(x=450,y=665)
        label5a = tk.Label(topw,text="{}".format(self.results[curr_row].fun),font=("Arial",14))
        label5a.place(x=500,y=710)
        ridge = tk.Canvas(topw,width=600,height=300,bd=4,relief=tk.GROOVE)
        ridge.place(x=925,y=600)
        label6 = tk.Label(topw,text="Best fit parameters",pady=15)
        label6.place(x=865,y=725)
        import math
        label7 = tk.Label(topw,text="log_g                     =          {}".format(format(self.results[curr_row].x[0],'.8e')))
        label7.place(x=1060,y=643)
        label8= tk.Label(topw,text = "temperature          =          {}".format(format(self.results[curr_row].x[1]*10000,'.8e')))
        label8.place(x=1060,y=691)
        label9 = tk.Label(topw, text = "abundance            =           {}".format(format(self.results[curr_row].x[2],'.8e')))
        label9.place(x=1060,y=739)
        label10 = tk.Label(topw,text="theta_r                   =           {}".format(format(math.sqrt(self.results[curr_row].x[3])*10**(-12),'.8e')))
        label10.place(x=1060,y=787)
        label11 = tk.Label(topw,text="E(b-v)                    =           {}".format(format(self.results[curr_row].x[4],'.8e')))
        label11.place(x=1060,y=835)
        def closethesource():
            topw.quit()
        byebyebutt = tk.Button(topw, bd=3, font="Arial 10", text="Next source",command=closethesource,padx=30,pady=5)
        byebyebutt.place(x=535,y=830)
        topw.mainloop()

    def display_results_double(self,curr_row):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        topw = tk.Toplevel()
        topw.geometry("1460x900+250+20")
        topw.title("Optimization results")
        topw.resizable(0,0)
        
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')
        import numpy as np

        valid_filters_this_row = []
        for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
            if np.isnan(bandflux) == False:
                valid_filters_this_row.append(valid_ind)
        
        valid_fluxes_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])

        valid_errors_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_errors_this_row.append(self.bandfluxerrors.iat[curr_row,valid_ind])    

        valid_avgwv_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_avgwv_this_row.append(self.avgwvlist[valid_ind])
    

        fig = Figure(figsize=(10.5,6))
        abc = fig.add_subplot(111)
        best_tup = (self.results[curr_row].x[0],self.results[curr_row].x[1],self.results[curr_row].x[2],self.results[curr_row].x[3],self.results[curr_row].x[4],self.results[curr_row].x[5],self.results[curr_row].x[6],self.results[curr_row].x[7])
        abc.scatter(valid_avgwv_this_row,valid_fluxes_this_row,color="orange")
        abc.set_xlabel("Wavelength [nm]")
        abc.set_ylabel("Flux [mJy]")
        abc.set_title("Source at row {}".format(self.rows[curr_row]+2))
        abc.errorbar(valid_avgwv_this_row,valid_fluxes_this_row,yerr=valid_errors_this_row,fmt="o",color="orange")
        hotmod = self.minichisqfunc_double(best_tup,valid_filters_this_row)[0]
        coolmod = self.minichisqfunc_double(best_tup,valid_filters_this_row)[1]
        abc.plot(valid_avgwv_this_row,hotmod,color="red")
        abc.plot(valid_avgwv_this_row,coolmod,color="blue")
        sumofmodels = [hotmod[i] + coolmod[i] for i in range(len(hotmod))]
        abc.plot(valid_avgwv_this_row,sumofmodels,color="limegreen")

        if self.saveplots == 1:
            saveimgname = self.imgfilename.replace("X","{}".format(self.rows[curr_row]+2))
            fig.savefig('{}'.format(saveimgname), bbox_inches='tight', dpi=150)

        canvas = FigureCanvasTkAgg(fig, master=topw)
        canvas.get_tk_widget().pack(anchor=tk.E)
        canvas.draw()

        label1 = tk.Label(topw,text="Average wavelength of each filter (x):")
        label1.place(x=50,y=20)
        textbox1 = tk.Text(topw,height=6,width=30)
        for filtername,avgwv in zip(self.filternames,valid_avgwv_this_row):
            textbox1.insert(tk.END,"{}      {}\n".format(filtername,avgwv))
        textbox1.place(x=50,y=50)
        label2 = tk.Label(topw,text="Bandfluxes (y, orange):")
        label2.place(x=50,y=195)
        textbox2 = tk.Text(topw,height=6,width=30)
        for filtername,bf in zip(self.filternames,valid_fluxes_this_row):
            textbox2.insert(tk.END,"{}      {}\n".format(filtername,format(bf,'.8e')))
        textbox2.place(x=50,y=225)
        label3 = tk.Label(topw,text="Bandflux errors:")
        label3.place(x=50,y=370)
        textbox3 = tk.Text(topw,height=6,width=30)
        for filtername,bfe in zip(self.filternames,valid_errors_this_row):
            textbox3.insert(tk.END,"{}      {}\n".format(filtername,format(bfe,'.8e')))
        textbox3.place(x=50,y=400)
        label4 = tk.Label(topw,text="Hot star model fluxes (y, red):")
        label4.place(x=50,y=545)
        textbox4 = tk.Text(topw,height=6,width=30)
        for filtername,mod in zip(self.filternames,self.minichisqfunc_double(best_tup,valid_filters_this_row)[0]):
            textbox4.insert(tk.END,"{}      {}\n".format(filtername,format(mod,'.8e')))
        textbox4.place(x=50,y=575)
        label5 = tk.Label(topw,text="Cool star model fluxes (y, blue):")
        label5.place(x=50,y=720)
        textbox5 = tk.Text(topw,height=6,width=30)
        for filtername,mod in zip(self.filternames,self.minichisqfunc_double(best_tup,valid_filters_this_row)[1]):
            textbox5.insert(tk.END,"{}      {}\n".format(filtername,format(mod,'.8e')))
        textbox5.place(x=50,y=750)
        groove = tk.Canvas(topw,width=350,height=120,bd=4,relief=tk.RIDGE)
        groove.place(x=435,y=655)
        label5 = tk.Label(topw,text="Lowest chi^2 value")
        label5.place(x=450,y=665)
        label5a = tk.Label(topw,text="{}".format(self.results[curr_row].fun),font=("Arial",14))
        label5a.place(x=500,y=710)
        ridge = tk.Canvas(topw,width=600,height=300,bd=4,relief=tk.GROOVE)
        ridge.place(x=925,y=600)
        label6 = tk.Label(topw,text="Best fit parameters",pady=15)
        label6.place(x=865,y=725)
        import math
        label7 = tk.Label(topw,text="log_g_hot                     =          {}".format(format(self.results[curr_row].x[0],'.8e')))
        label7.place(x=1060,y=623)
        label8= tk.Label(topw,text = "temperature_hot          =          {}".format(format(self.results[curr_row].x[1]*10000,'.8e')))
        label8.place(x=1060,y=656)
        label9 = tk.Label(topw, text = "abundance_hot            =           {}".format(format(self.results[curr_row].x[2],'.8e')))
        label9.place(x=1060,y=689)
        label10 = tk.Label(topw,text="theta_r_hot                   =           {}".format(format(math.sqrt(self.results[curr_row].x[3])*10**(-12),'.8e')))
        label10.place(x=1060,y=722)
        label11 = tk.Label(topw,text="E(b-v)_hot                    =           {}".format(format(self.results[curr_row].x[4],'.8e')))
        label11.place(x=1060,y=755)
        label12 = tk.Label(topw,text="temperature_cool        =           {}".format(format(self.results[curr_row].x[5],'.8e')))
        label12.place(x=1060,y=788)
        label13 = tk.Label(topw,text="theta_r_cool                 =           {}".format(format(math.sqrt(self.results[curr_row].x[6])*10**(-12),'.8e')))
        label13.place(x=1060,y=821)
        label14 = tk.Label(topw,text="E(b-v)_cool                  =           {}".format(format(self.results[curr_row].x[7],'.8e')))
        label14.place(x=1060,y=854)
        def closethesource():
            topw.quit()
        byebyebutt = tk.Button(topw, bd=3, font="Arial 10", text="Next source",command=closethesource,padx=30,pady=5)
        byebyebutt.place(x=535,y=830)
        topw.mainloop()


go = ChiSquared()