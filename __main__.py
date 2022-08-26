import scipy.optimize as opt
import pandas as pd

class ChiSquared():
    def __init__(self):
        self.filenamevar = ""
        self.chosenstar = "     1-star fit     "
        self.checkedset= 0
        self.checked2set = 0
        self.checked3set = 0
        self.checked4set = 0
        self.checker1set = 1
        self.checker2set = 1
        self.checker3set = 1
        self.checker4set = 1
        self.checker5set = 0
        self.slidervalset = 0
        self.sliderval2set = 0
        self.rownumberset = ""
        self.sliderstringset = "log-log axes"
        self.sliderstring2set = "optimizer"
        self.model_chosen_set = "UVIT_HST"
        self.ulmethset = "Standard"
        self.starlist1 = ["0.03","30","N/A","N/A"]
        self.starlist2 = ["0.03","30","0.03","30"]
        self.stardict1 = [["3.5","5","1"],[".35","3.1","1"],["-2.5",".5","1"],["0.07","1","1"],["N/A","N/A","N/A"],["N/A","N/A","N/A"]]
        self.stardict2 = [["3.5","5","1"],[".65","3.1","1"],["-2.5",".5","1"],["0.07","1","1"],[".35",".55","1"],["0.07","1","1"]]
        while True:
            self.intro_gui()
            self.buildGrid()
            self.extract_measured_flux()
            self.convert_to_AB()
            self.convert_to_bandflux()
            self.prepare_for_interpolation()
            self.minimize_chisq()
            self.find_param_errors()
            self.display_all_results()
            self.save_output()

    ##orange

    def intro_gui(self):
        self.switch = False
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        mwin = tk.Tk()
        mwin.geometry("1225x700+520+150")
        mwin.title("Stellar Fitting")
        mwin.config(bg='alice blue')
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
                        self.filenamevar = user_filename.get()
                    except:
                        tk.messagebox.showinfo('Error', "Could not find file. Please place the file in the program folder and try again.")
                        return None
                    else:
                        if highestelem > len(self.measuredata)+1 or lowestelem < 2:
                            tk.messagebox.showinfo('Error', "Rows specified are out of range.")
                            return None
                        if (checker2.get() == 1 and weightedmeanvarname.get()[-4:] != ".csv") or (checker3.get() == 1 and gridname.get()[-4:] != ".csv"):
                            tk.messagebox.showinfo('Error', "The filenames specified are not allowed. Make sure to use the .csv extension.")
                            return None
                        elif checker4.get() == 1 and (imgname.get()[-4:] != ".png" and imgname.get()[-4:] != ".jpg"):
                            tk.messagebox.showinfo('Error', "The filenames specified are not allowed. Make sure to use the .png or .jpg extensions.")
                            return None
                        else:
                            try:
                                a = int(weightedmeanvarname.get()[0])
                                b = int(gridname.get()[0])
                                c = int(imgname.get()[0])
                                return None
                            except:
                                try:
                                    self.switch = True
                                    self.rows = [i-2 for i in introwlist]
                                    self.rownumberset = user_rownumber.get()

                                    self.dispresults = checker1.get()
                                    self.weightedmeanvarresults = checker2.get()
                                    self.gridresults = checker3.get()
                                    self.saveplots = checker4.get()
                                    self.plotscale = currentsliderval.get()
                                    self.solvemethod = currentsliderval2.get()
                                    self.checker1set = checker1.get()
                                    self.checker2set = checker2.get()
                                    self.checker3set = checker3.get()
                                    self.checker4set = checker4.get()
                                    self.checker5set = checker5.get()
                                    self.checkedset = checked.get()
                                    self.checked2set = checked2.get()
                                    self.slidervalset = currentsliderval.get()
                                    self.sliderstringset = sliderstring.get()
                                    self.sliderval2set = currentsliderval2.get()
                                    self.sliderstring2set = sliderstring2.get()

                                    self.model_chosen = user_model_cho.get()
                                    self.model_chosen_set = user_model_cho.get()

                                    if checker2.get() == 1:
                                        self.weightedmeanvarname = weightedmeanvarname.get()
                                    if checker3.get() == 1:
                                        self.gridname = gridname.get()
                                    if checker4.get() == 1:
                                        self.imgfilename = imgname.get()
                                    if checker5.get() == 1:
                                        self.silent = True
                                    else:
                                        self.silent = False
                                    
                                    self.single_star = False
                                    self.double_star = False
                                    self.chosenstar = starno_chosen.get()

                                    if starno_chosen.get() == "     1-star fit     ":
                                        self.single_star = True
                                        self.thetabound1lo = float(user_thetabound1lo.get())
                                        self.thetabound1hi = float(user_thetabound1hi.get())

                                        self.g1lowest = float(user_g1lowest.get())
                                        self.g1highest = float(user_g1highest.get())
                                        self.g1num = int(user_g1num.get())
                                        if self.g1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.T1lowest = float(user_T1lowest.get())
                                        self.T1highest = float(user_T1highest.get())
                                        self.T1num = int(user_T1num.get())
                                        if self.T1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.Z1lowest = float(user_Z1lowest.get())
                                        self.Z1highest = float(user_Z1highest.get())
                                        self.Z1num = int(user_Z1num.get())
                                        if self.Z1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.ebv1lowest = float(user_ebv1lowest.get())
                                        self.ebv1highest = float(user_ebv1highest.get())
                                        self.ebv1num = int(user_ebv1num.get())
                                        if self.ebv1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')

                                        self.starlist1[0] = user_thetabound1lo.get()
                                        self.starlist1[1] = user_thetabound1hi.get()
                                        if user_model_cho.get() == "UVIT_HST":
                                            self.stardict1[0][0] = user_g1lowest.get()
                                            self.stardict1[0][1] = user_g1highest.get()
                                            self.stardict1[0][2] = user_g1num.get()
                                            self.stardict1[1][0] = user_T1lowest.get()
                                            self.stardict1[1][1] = user_T1highest.get()
                                            self.stardict1[1][2] = user_T1num.get()
                                            self.stardict1[2][0] = user_Z1lowest.get()
                                            self.stardict1[2][1] = user_Z1highest.get()
                                            self.stardict1[2][2] = user_Z1num.get()
                                            self.stardict1[3][0] = user_ebv1lowest.get()
                                            self.stardict1[3][1] = user_ebv1highest.get()
                                            self.stardict1[3][2] = user_ebv1num.get()

                                    elif starno_chosen.get() == "     2-star fit     ":
                                        self.double_star = True

                                        self.thetabound1lo = float(user_thetabound1lo.get())
                                        self.thetabound1hi = float(user_thetabound1hi.get())
                                        self.thetabound2lo = float(user_thetabound2lo.get())
                                        self.thetabound2hi = float(user_thetabound2hi.get())

                                        self.g1lowest = float(user_g1lowest.get())
                                        self.g1highest = float(user_g1highest.get())
                                        self.g1num = int(user_g1num.get())
                                        if self.g1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.T1lowest = float(user_T1lowest.get())
                                        self.T1highest = float(user_T1highest.get())
                                        self.T1num = int(user_T1num.get())
                                        if self.T1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.Z1lowest = float(user_Z1lowest.get())
                                        self.Z1highest = float(user_Z1highest.get())
                                        self.Z1num = int(user_Z1num.get())
                                        if self.Z1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.ebv1lowest = float(user_ebv1lowest.get())
                                        self.ebv1highest = float(user_ebv1highest.get())
                                        self.ebv1num = int(user_ebv1num.get())
                                        if self.ebv1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.Tbound2lo = float(user_Tbound2lo.get())
                                        self.Tbound2hi = float(user_Tbound2hi.get())
                                        self.T2num = int(user_T2num.get())
                                        if self.T2num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.ebvbound2lo = float(user_ebvbound2lo.get())
                                        self.ebvbound2hi = float(user_ebvbound2hi.get())
                                        self.ebv2num = int(user_ebv2num.get())
                                        if self.ebv2num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')

                                        self.starlist2[0] = user_thetabound1lo.get()
                                        self.starlist2[1] = user_thetabound1hi.get()
                                        self.starlist2[2] = user_thetabound2lo.get()
                                        self.starlist2[3] = user_thetabound2hi.get()
                                        if user_model_cho.get() == "UVIT_HST":
                                            self.stardict2[0][0] = user_g1lowest.get()
                                            self.stardict2[0][1] = user_g1highest.get()
                                            self.stardict2[0][2] = user_g1num.get()
                                            self.stardict2[1][0] = user_T1lowest.get()
                                            self.stardict2[1][1] = user_T1highest.get()
                                            self.stardict2[1][2] = user_T1num.get()
                                            self.stardict2[2][0] = user_Z1lowest.get()
                                            self.stardict2[2][1] = user_Z1highest.get()
                                            self.stardict2[2][2] = user_Z1num.get()
                                            self.stardict2[3][0] = user_ebv1lowest.get()
                                            self.stardict2[3][1] = user_ebv1highest.get()
                                            self.stardict2[3][2] = user_ebv1num.get()
                                            self.stardict2[4][0] = user_Tbound2lo.get()
                                            self.stardict2[4][1] = user_Tbound2hi.get()
                                            self.stardict2[4][2] = user_T2num.get()
                                            self.stardict2[5][0] = user_ebvbound2lo.get()
                                            self.stardict2[5][1] = user_ebvbound2hi.get()
                                            self.stardict2[5][2] = user_ebv2num.get()

                                except Exception as e:
                                    print(e)
                                    tk.messagebox.showinfo('Error', "One or more parameters seem to have been entered incorrectly. Please reenter the values and try again.")
                                    return None
                                else:
                                    mwin.destroy()

        starno_chosen = tk.StringVar()
        checked=tk.IntVar()
        checked.set(self.checkedset)
        user_rownumber = tk.StringVar()
        user_rownumber.set(self.rownumberset)
        enterrownumberpack = tk.Frame(mwin)
        enterrownumberpack.place(x=37,y=110)
        enterrownumber = tk.Entry(enterrownumberpack,textvariable=user_rownumber,width=15)
        enterrownumber.pack(ipady=3)
        labelwhich = tk.Label(mwin,text="Read rows", bg="alice blue")
        labelwhich.place(x=39,y=80)
        def openrows():
            from tkinter import messagebox
            tk.messagebox.showinfo("Help","  •  Use csv row labelling (which should start at row 2)\n\n  •  Specify multiple rows with commas: 2,5,6\n\n  •  Specify a selection of rows with a colon: 3:8")
        whichbutton = tk.Button(mwin,text="?",font=("TimesNewRoman 8"),command = openrows)
        whichbutton.place(x=140,y=111)
        canvas2 = tk.Canvas(mwin,relief=tk.RIDGE,bd=2,width=330,height=320,bg='azure2')
        canvas2.place(x=310,y=110)
        canvasline = tk.Canvas(mwin,bd=3,relief=tk.GROOVE,width=680,height=1000,bg='mint cream')
        canvasline.place(x=-20,y=450)
        canvasline2 = canvasline = tk.Canvas(mwin,bd=3,relief=tk.GROOVE,width=680,height=1000,bg='lavender')
        canvasline2.place(x=660,y=110)

        user_thetabound1lo = tk.DoubleVar()
        user_thetabound1hi = tk.DoubleVar()
        user_thetabound2lo = tk.DoubleVar()
        user_thetabound2hi = tk.DoubleVar()

        ystar1labels = 530
        ystar1entries = 560
        ystar2labels = 610
        ystar2entries = 640
        ycheckbutton = 480

        lowerboundlabel = tk.Label(mwin,text="Lower bound",font="Arial 10 underline",bg="mint cream")
        lowerboundlabel.place(x=320,y=ystar1labels)
        upperboundlabel = tk.Label(mwin,text="Upper bound",font="Arial 10 underline",bg="mint cream")
        upperboundlabel.place(x=450,y=ystar1labels)

        label1 = tk.Label(mwin,text="θ_r_hot/1e-12",bg="mint cream")
        label1.place(x=50,y=ystar1labels+30)
        label2 = tk.Label(mwin,text="θ_r_cool/1e-12",bg="mint cream")
        label2.place(x=50,y=ystar2labels+30)

        entrylowerbound1 = tk.Entry(mwin,textvariable=user_thetabound1lo,width=12)
        entrylowerbound1.place(x=320,y=ystar1entries)
        entryupperbound1 = tk.Entry(mwin,textvariable=user_thetabound1hi,width=12)
        entryupperbound1.place(x=450,y=ystar1entries)

        entrylowerbound2 = tk.Entry(mwin,textvariable=user_thetabound2lo,width=12)
        entrylowerbound2.place(x=320,y=ystar2entries)
        entryupperbound2 = tk.Entry(mwin,textvariable=user_thetabound2hi,width=12)
        entryupperbound2.place(x=450,y=ystar2entries)
        


        def enable(howmany):
            entrylowerbound1['state'] = tk.NORMAL
            entryupperbound1['state'] = tk.NORMAL
            if howmany == "all":
                entrylowerbound2['state'] = tk.NORMAL
                entryupperbound2['state'] = tk.NORMAL

        def disable(howmany):
            entrylowerbound1['state'] = tk.DISABLED
            entryupperbound1['state'] = tk.DISABLED
            if howmany == "all":
                entrylowerbound2['state'] = tk.DISABLED
                entryupperbound2['state'] = tk.DISABLED


        def stuff_vals():
            entrylist = [entrylowerbound1,entryupperbound1,entrylowerbound2,entryupperbound2]
            if starno_chosen.get() == "     1-star fit     ":
                enable("all")
                for i,entry in enumerate(entrylist):
                    entry.delete(0,20)
                    entry.insert(0,"{}".format(self.starlist1[i]))
                disable("all")
                if checked.get() == 1:
                    enable("some")
            elif starno_chosen.get() == "     2-star fit     ":
                enable("all")
                for i,entry in enumerate(entrylist):
                    entry.delete(0,20)
                    entry.insert(0,"{}".format(self.starlist2[i]))
                disable("all")
                if checked.get() == 1:
                    enable("all")
        
        def openinfo():
            info = tk.Toplevel()
            info.geometry("900x560+600+250")
            info.title("Info")
            info.config(bg="white")
            infolabel = tk.Label(info,bg="white",wraplength=800,justify=tk.LEFT,text="  This program uses chi-square minimization to find the best fit between the inputted flux data and a model flux function, whose form is specified by either 5 or 8 parameters, depending on the type of model selected (1-star or 2-star). For the single-star model, the model flux is determined at each data point in the input file (i.e. at each specified filter) by the log of the surface gravity log_g, the temperature T, the solar abundance (metallicity) Z, the stellar angular radius theta_r, and the interstellar reddening E(B-V). For the two-star model an additional three parameters are used to describe the cooler star: T_cool, theta_r_cool, and E_bv_cool, while the original five are relabeled with hot subscripts. In both models, theta_r appears as a quadratic term, while log_g, T, and Z are used to interpolate a flux value from a pre-existing data array that provides the \"filtered intrinsic model flux\" through each filter, given a point in those three coordinates. The filtered instrinsic model fluxes at each node (11-filter set) in the array were calculated beforehand using a similar array that provided the intrisic flux at each wavelength; namely, the calculations were done by integrating these intrinsic fluxes over the wavelengths of each filter (while also weighting by a model filter function). The final intrinsic filtered model flux (as a function of log_g, T, and Z, as well as the filter chosen) is a linear term in the current calculation. The final parameter, E(B-V), appears, along with a filter-dependent extinction factor k(λ-V), in a 10^(-0.4*E(B-V)(k(λ-V)-R_V)) term. (R_V is a constant, a parameter of the pre-calculated average extinction curve.)\n\n  If the model desired is single-star, one of these model calculations is done, wheras if the model is two-star, two of the calculations are done, with the cool-star calculation using the three new parameters. (The \"missing\" two are provided as constants in the program.) A chi-square minimization is performed, which in the two-star model involves finding the difference at every datapoint (filter) between the inputted data flux and the sum of the model fluxes for the hot and cool stars. The Python code used for the minimization process is Scipy's optimize.minimize (using the default method, with bounds and inital parameter guesses specified in this interface by the user). Errors for the best-fit parameters are found after the best fit is found, by varying the individual parameters about their best-fit values while fixing the others and stamping an upper error bound and a lower error bound when the chi-square value changes by 4.72 (for the single-star model) or by 9.14 (for the two-star model).")
            infolabel.place(x=50,y=30)
            info.mainloop()
        helpgobutton = tk.Button(mwin,text="Info",font=("Arial",10),command = openinfo,pady=10,padx=35,bd=2)
        helpgobutton.place(x=715,y=30)

        checker1 = tk.IntVar()
        checker1.set(self.checker1set)
        checker2 = tk.IntVar()
        checker2.set(self.checker2set)
        checker3 = tk.IntVar()
        checker3.set(self.checker3set)
        checker4 = tk.IntVar()
        checker4.set(self.checker4set)
        checker5 = tk.IntVar()
        checker5.set(self.checker5set)
        sliderstring = tk.StringVar()
        currentsliderval = tk.IntVar()
        currentsliderval.set(self.slidervalset)
        sliderstring.set(self.sliderstringset)
        sliderstring2 = tk.StringVar()
        currentsliderval2 = tk.IntVar()
        currentsliderval2.set(self.sliderval2set)
        sliderstring2.set(self.sliderstring2set)
        weightedmeanvarname = tk.StringVar()
        gridname = tk.StringVar()
        imgname = tk.StringVar()
        sliderstring.set(self.sliderstringset)
        def changesliderstring(useless):
            if currentsliderval.get() == 1:
                sliderstring.set(" linear axes  ")
            elif currentsliderval.get() == 0:
                sliderstring.set("log-log axes")
        def changesliderstring2(useless):
            if currentsliderval2.get() == 1:
                sliderstring2.set("  analytic ")
            elif currentsliderval2.get() == 0:
                sliderstring2.set("optimizer")
        
        def grent1():
            if plotslider['state'] == tk.NORMAL:
                plotslider['state'] = tk.DISABLED
                sliderstring.set("                     ")
                sliderlabel.config(bg="gray95")
            elif plotslider['state'] == tk.DISABLED:
                plotslider['state'] = tk.NORMAL
                sliderlabel.config(bg="white")
                if currentsliderval.get() == 1:
                    sliderstring.set(" linear axes  ")
                elif currentsliderval.get() == 0:
                    sliderstring.set("log-log axes")

        def grent2():
            if buttentry2['state'] == tk.NORMAL:
                buttentry2.delete(0,30)
                buttentry2['state'] = tk.DISABLED
            elif buttentry2['state'] == tk.DISABLED:
                buttentry2['state'] = tk.NORMAL
                buttentry2.insert(tk.END,"weighted_meanvar.csv")
        def grent3():
            if buttentry3['state'] == tk.NORMAL:
                buttentry3.delete(0,30)
                buttentry3['state'] = tk.DISABLED
            elif buttentry3['state'] == tk.DISABLED:
                buttentry3['state'] = tk.NORMAL
                buttentry3.insert(tk.END,"params_grid.csv")
        def grent4():
            if buttentry4['state'] == tk.NORMAL:
                buttentry4.delete(0,30)
                buttentry4['state'] = tk.DISABLED
            elif buttentry4['state'] == tk.DISABLED:
                buttentry4['state'] = tk.NORMAL
                buttentry4.insert(tk.END,"plot_so_rowX.png")
                
        plotslider = tk.Scale(mwin,from_=0,to=1,orient=tk.HORIZONTAL,showvalue=0,length=65,width=25,variable=currentsliderval, command=changesliderstring)
        plotslider.place(x=470,y=165)
        grayframe = tk.Frame(mwin,bg="gray95",bd=3)
        grayframe.place(x=350,y=165)
        sliderlabel = tk.Label(grayframe,textvariable=sliderstring,padx=5,bg='white')
        sliderlabel.pack()
        if currentsliderval.get() == 0:
            plotslider.set(0)
        if currentsliderval == 1:
            plotslider.set(1)
        solvelabel = tk.Label(mwin,text="Solve method",bg='alice blue')
        solvelabel.place(x=40,y=170)
        plotslider2 = tk.Scale(mwin,from_=0,to=1,orient=tk.HORIZONTAL,showvalue=0,length=65,width=25,variable=currentsliderval2, command=changesliderstring2)
        plotslider2.place(x=40,y=205)
        grayframe2 = tk.Frame(mwin,bg="gray95",bd=3)
        grayframe2.place(x=120,y=205)
        sliderlabel2 = tk.Label(grayframe2,textvariable=sliderstring2,padx=5,bg='white')
        sliderlabel2.pack()
        if currentsliderval2.get() == 0:
            plotslider2.set(0)
        if currentsliderval2 == 1:
            plotslider2.set(1)
        checkbutt1 = tk.Checkbutton(mwin,text="Display results",variable=checker1,command=grent1,bg='azure2')
        checkbutt2 = tk.Checkbutton(mwin,text="Save weighted mean and variance data",variable=checker2,command=grent2,bg='azure2')
        checkbutt3 = tk.Checkbutton(mwin,text="Save parameter grids",variable=checker3,command=grent3,bg='azure2')
        checkbutt4 = tk.Checkbutton(mwin,text="Save plot images (1 per source X)",variable=checker4,command=grent4,bg='azure2')
        checkbutt5 = tk.Checkbutton(mwin,text="Run silently",variable=checker5,bg='alice blue')
        checkbutt1.place(x=340,y=130)
        checkbutt2.place(x=340,y=220)
        checkbutt3.place(x=340,y=290)
        checkbutt4.place(x=340,y=360)
        checkbutt5.place(x=1020,y=35)
        buttentry2 = tk.Entry(mwin, textvariable = weightedmeanvarname, width=26)
        buttentry3 = tk.Entry(mwin, textvariable = gridname,width=26)
        buttentry4 = tk.Entry(mwin,textvariable = imgname,width=26)
        buttentry2.place(x=345,y=250)
        buttentry3.place(x=345,y=320)
        buttentry4.place(x=345,y=390)
        if checker2.get() == 0:
            buttentry2['state'] = tk.DISABLED
        if checker3.get() == 0:
            buttentry3['state'] = tk.DISABLED
        if checker4.get() == 0:
            buttentry4['state'] = tk.DISABLED

        user_g1lowest = tk.DoubleVar()
        user_g1highest = tk.DoubleVar()
        user_g1num = tk.IntVar()
        user_T1lowest = tk.DoubleVar()
        user_T1highest = tk.DoubleVar()
        user_T1num = tk.IntVar()
        user_Z1lowest = tk.DoubleVar()
        user_Z1highest = tk.DoubleVar()
        user_Z1num = tk.IntVar()
        user_ebv1lowest = tk.DoubleVar()
        user_ebv1highest = tk.DoubleVar()
        user_ebv1num = tk.IntVar()
        user_Tbound2lo = tk.DoubleVar()
        user_Tbound2hi = tk.DoubleVar()
        user_T2num = tk.IntVar()
        user_ebvbound2lo = tk.DoubleVar()
        user_ebvbound2hi = tk.DoubleVar()
        user_ebv2num = tk.IntVar()
        xstarbentrieslo = 830
        xstarbentrieshi = 950
        xstarbentriesnum = 1070
        def infopopup():
            from tkinter import messagebox
            tk.messagebox.showinfo("Help","Values are evenly spaced, starting from the lowest value and including the highest value.")
        infobutton = tk.Button(mwin,text=" ? ",font=("TimesNewRoman 8"),command = infopopup)
        infobutton.place(x=xstarbentriesnum+100,y=180)
        lwbound = tk.Label(mwin,text="Lowest value",font="Arial 10 underline",bg="lavender")
        lwbound.place(x=xstarbentrieslo-7,y=180)
        upbound = tk.Label(mwin,text="Highest value",font = "Arial 10 underline",bg="lavender")
        upbound.place(x=xstarbentrieshi-7,y=180)
        numberr = tk.Label(mwin,text="No. of values",font = "Arial 10 underline",bg="lavender")
        numberr.place(x=xstarbentriesnum-7,y=180)
        labelbg1 = tk.Label(mwin,text="",bg="lavender")
        labelbg1.place(x=xstarbentrieslo-130,y=230)
        entrybg1lo = tk.Entry(mwin,textvariable=user_g1lowest,width=10)
        entrybg1lo.place(x=xstarbentrieslo,y=230)
        entrybg1hi = tk.Entry(mwin,textvariable=user_g1highest,width=10)
        entrybg1hi.place(x=xstarbentrieshi,y=230)
        entrybg1num = tk.Entry(mwin,textvariable=user_g1num,width=10)
        entrybg1num.place(x=xstarbentriesnum,y=230)
        labelbT1 = tk.Label(mwin,text="",bg="lavender")
        labelbT1.place(x=xstarbentrieslo-130,y=290)
        entrybT1lo = tk.Entry(mwin,textvariable=user_T1lowest,width=10)
        entrybT1lo.place(x=xstarbentrieslo,y=290)
        entrybT1hi = tk.Entry(mwin,textvariable=user_T1highest,width=10)
        entrybT1hi.place(x=xstarbentrieshi,y=290)
        entrybT1num = tk.Entry(mwin,textvariable=user_T1num,width=10)
        entrybT1num.place(x=xstarbentriesnum,y=290)
        labelbZ1 = tk.Label(mwin,text="",bg="lavender")
        labelbZ1.place(x=xstarbentrieslo-130,y=350)
        entrybZ1lo = tk.Entry(mwin,textvariable=user_Z1lowest,width=10)
        entrybZ1lo.place(x=xstarbentrieslo,y=350)
        entrybZ1hi = tk.Entry(mwin,textvariable=user_Z1highest,width=10)
        entrybZ1hi.place(x=xstarbentrieshi,y=350)
        entrybZ1num = tk.Entry(mwin,textvariable=user_Z1num,width=10)
        entrybZ1num.place(x=xstarbentriesnum,y=350)
        labelbebv1 = tk.Label(mwin,text="",bg="lavender")
        labelbebv1.place(x=xstarbentrieslo-130,y=410)
        entrybebv1lo = tk.Entry(mwin,textvariable=user_ebv1lowest,width=10)
        entrybebv1lo.place(x=xstarbentrieslo,y=410)
        entrybebv1hi = tk.Entry(mwin,textvariable=user_ebv1highest,width=10)
        entrybebv1hi.place(x=xstarbentrieshi,y=410)
        entrybebv1num = tk.Entry(mwin,textvariable=user_ebv1num,width=10)
        entrybebv1num.place(x=xstarbentriesnum,y=410)
        labelbT2 = tk.Label(mwin,text="",bg="lavender")
        labelbT2.place(x=xstarbentrieslo-130,y=470)
        entrybT2lo = tk.Entry(mwin,textvariable=user_Tbound2lo,width=10)
        entrybT2lo.place(x=xstarbentrieslo,y=470)
        entrybT2hi = tk.Entry(mwin,textvariable=user_Tbound2hi,width=10)
        entrybT2hi.place(x=xstarbentrieshi,y=470)
        entrybT2num = tk.Entry(mwin,textvariable=user_T2num,width=10)
        entrybT2num.place(x=xstarbentriesnum,y=470)
        labelbebv2 = tk.Label(mwin,text="",bg="lavender")
        labelbebv2.place(x=xstarbentrieslo-130,y=530)
        entrybebv2lo = tk.Entry(mwin,textvariable=user_ebvbound2lo,width=10)
        entrybebv2lo.place(x=xstarbentrieslo,y=530)
        entrybebv2hi = tk.Entry(mwin,textvariable=user_ebvbound2hi,width=10)
        entrybebv2hi.place(x=xstarbentrieshi,y=530)
        entrybebv2num = tk.Entry(mwin,textvariable=user_ebv2num,width=10)
        entrybebv2num.place(x=xstarbentriesnum,y=530)
        
        checked2=tk.IntVar()
        checked2.set(self.checked2set)

        def enable2(howmany):
            entrybg1lo['state'] = tk.NORMAL
            entrybg1hi['state'] = tk.NORMAL
            entrybg1num['state'] = tk.NORMAL
            entrybT1lo['state'] = tk.NORMAL
            entrybT1hi['state'] = tk.NORMAL
            entrybT1num['state'] = tk.NORMAL
            entrybZ1lo['state'] = tk.NORMAL
            entrybZ1hi['state'] = tk.NORMAL
            entrybZ1num['state'] = tk.NORMAL
            entrybebv1lo['state'] = tk.NORMAL
            entrybebv1hi['state'] = tk.NORMAL
            entrybebv1num['state'] = tk.NORMAL
            if howmany == "all":
                entrybT2lo['state'] = tk.NORMAL
                entrybT2hi['state'] = tk.NORMAL
                entrybT2num['state'] = tk.NORMAL
                entrybebv2lo['state'] = tk.NORMAL
                entrybebv2hi['state'] = tk.NORMAL
                entrybebv2num['state'] = tk.NORMAL

        def disable2(howmany):
            entrybg1lo['state'] = tk.DISABLED
            entrybg1hi['state'] = tk.DISABLED
            entrybg1num['state'] = tk.DISABLED
            entrybT1lo['state'] = tk.DISABLED
            entrybT1hi['state'] = tk.DISABLED
            entrybT1num['state'] = tk.DISABLED
            entrybZ1lo['state'] = tk.DISABLED
            entrybZ1hi['state'] = tk.DISABLED
            entrybZ1num['state'] = tk.DISABLED
            entrybebv1lo['state'] = tk.DISABLED
            entrybebv1hi['state'] = tk.DISABLED
            entrybebv1num['state'] = tk.DISABLED
            if howmany == "all":
                entrybT2lo['state'] = tk.DISABLED
                entrybT2hi['state'] = tk.DISABLED
                entrybT2num['state'] = tk.DISABLED
                entrybebv2lo['state'] = tk.DISABLED
                entrybebv2hi['state'] = tk.DISABLED
                entrybebv2num['state'] = tk.DISABLED


        def stuff_vals2():
            entrybdict = [[entrybg1lo,entrybg1hi,entrybg1num],[entrybT1lo,entrybT1hi,entrybT1num],[entrybZ1lo,entrybZ1hi,entrybZ1num],[entrybebv1lo,entrybebv1hi,entrybebv1num],[entrybT2lo,entrybT2hi,entrybT2num],[entrybebv2lo,entrybebv2hi,entrybebv2num]]
            labelblistlist = [[labelbg1,"log(g)","log(g_hot)"],[labelbT1,"T/10000","T_hot/10000"],[labelbZ1,"Z","Z_hot"],[labelbebv1,"E(B-V)","E(B-V)_hot"],[labelbT2,"","T_cool/10000"],[labelbebv2,"","E(B-V)_cool"]]
            if user_model_cho.get() == "UVIT_HST":
                if starno_chosen.get() == "     1-star fit     ":
                    enable2("all")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[1]))
                    for i in range(6):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict1[i][j]))
                    disable2("all")
                    if checked2.get() == 1:
                        enable2("some")
                elif starno_chosen.get() == "     2-star fit     ":
                    enable2("all")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[2]))
                    for i in range(6):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict2[i][j]))
                    disable2("all")
                    if checked2.get() == 1:
                        enable2("all")

        def stuffy(useless):
            stuff_vals()
            stuff_vals2()
        
        def stuffyonly2(useless):
            stuff_vals2()

        def gray():
            if starno_chosen.get() == "     1-star fit     ":
                if entrylowerbound1['state'] == tk.NORMAL:
                    disable("some")
                elif entrylowerbound1['state'] == tk.DISABLED:
                    enable("some")
            elif starno_chosen.get() == "     2-star fit     ":
                if entrylowerbound1['state'] == tk.NORMAL:
                    disable("all")
                elif entrylowerbound1['state'] == tk.DISABLED:
                    enable("all")
        
        def gray2():
            if starno_chosen.get() == "     1-star fit     ":
                if entrybg1lo['state'] == tk.NORMAL:
                    disable2("some")
                elif entrybg1lo['state'] == tk.DISABLED:
                    enable2("some")
            elif starno_chosen.get() == "     2-star fit     ":
                if entrybg1lo['state'] == tk.NORMAL:
                    disable2("all")
                elif entrybg1lo['state'] == tk.DISABLED:
                    enable2("all")

        user_model_cho = tk.StringVar()
        user_model_cho.set(self.model_chosen_set)
        modelchooptions = ["UVIT_HST"]
        modelcholabel = tk.Label(mwin,text="Model data filters",bg="alice blue")
        modelcholabel.place(x=38,y=360)
        modelchomenu = tk.OptionMenu(mwin,user_model_cho,*modelchooptions,command=stuffyonly2)
        modelchomenu.place(x=32,y=390)
        starlabel = tk.Label(mwin,text="Fitting method",bg="alice blue")
        starlabel.place(x=38,y=270)
        starno_chosen.set(self.chosenstar)
        staroptions = ["     1-star fit     ","     2-star fit     "]
        starmenu = tk.OptionMenu(mwin,starno_chosen,*staroptions,command=stuffy)
        starmenu.place(x=32,y=300)

        checkbutton = tk.Checkbutton(mwin,text="Edit bounds for theta_r",variable=checked,command=gray,bg="mint cream")
        checkbutton.place(x=10,y=ycheckbutton)
        checkbutton2 = tk.Checkbutton(mwin,text="Edit parameters grid",variable=checked2,command=gray2,bg="lavender")
        checkbutton2.place(x=680,y=130)

        user_filename = tk.StringVar()
        user_filename.set(self.filenamevar)
        enterfileneame = tk.Entry(mwin,textvariable = user_filename,width=45)
        enterfileneame.place(x=113,y=30)
        labeltop = tk.Label(mwin,text="Input file: ", bg='white',border=2,relief=tk.RIDGE,padx=3,pady=1)
        labeltop.place(x=35,y=29)

        gobutton = tk.Button(mwin,text="Fit data",font=("Arial",10),command = collectfilename,pady=10,padx=25,bd=2)
        gobutton.place(x=860,y=30)
        grent2()
        grent2()
        grent3()
        grent3()
        grent4()
        grent4()
        disable("all")
        disable2("all")
        stuffy(3)
        mwin.mainloop()

    ##

    def extract_measured_flux(self):
        assert self.switch == True, "Program terminated"

        if self.model_chosen == "UVIT_HST":
                
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
                import tkinter as tk
                miniwin = tk.Tk()
                miniwin.geometry("10x10+800+500")
                response = tk.messagebox.askquestion('Warning',"No entries found for {}. Do you wish to proceed?\n\n(These filters will not be fitted. If a single column is missing without its error or vice versa, you should double check the file for naming typos)".format(badstr))
                if response == "yes":
                    miniwin.destroy()
                if response == "no":
                    assert response == "yes", "Program terminated"

            for rowind,row in self.raw_magnitudes_frame.iterrows():
                for colind,colelement in enumerate(row):
                    if colelement == -999:
                        self.raw_magnitudes_frame.iat[rowind,colind] = np.nan


    def convert_to_AB(self):
        if self.model_chosen == "UVIT_HST":
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

        if self.model_chosen == "UVIT_HST":
            self.filternames = ["F148W","F169M","F172M","N219M","N279N","f275w","f336w","f475w","f814w","f110w","f160w"]
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
            
    def buildGrid(self):
        import numpy as np

        if self.single_star == True:
            g1vals = np.linspace(self.g1lowest,self.g1highest,self.g1num)
            T1vals = np.linspace(self.T1lowest,self.T1highest,self.T1num)
            Z1vals = np.linspace(self.Z1lowest,self.Z1highest,self.Z1num)
            ebv1vals = np.linspace(self.ebv1lowest,self.ebv1highest,self.ebv1num)

            self.g1grid,self.T1grid,self.Z1grid,self.ebv1grid = np.meshgrid(g1vals,T1vals,Z1vals,ebv1vals,indexing='ij')

        elif self.double_star == True:
            g1vals = np.linspace(self.g1lowest,self.g1highest,self.g1num)
            T1vals = np.linspace(self.T1lowest,self.T1highest,self.T1num)
            Z1vals = np.linspace(self.Z1lowest,self.Z1highest,self.Z1num)
            ebv1vals = np.linspace(self.ebv1lowest,self.ebv1highest,self.ebv1num)
            T2vals = np.linspace(self.Tbound2lo,self.Tbound2hi,self.T2num)
            ebv2vals = np.linspace(self.ebvbound2lo,self.ebvbound2hi,self.ebv2num)

            self.g1grid,self.T1grid,self.Z1grid,self.ebv1grid,self.T2grid,self.ebv2grid = np.meshgrid(g1vals,T1vals,Z1vals,ebv1vals,T2vals,ebv2vals,indexing='ij')

    def prepare_for_interpolation(self):
        import pandas as pd
        import xarray as xr
        import numpy as np

        ds_disk = xr.open_dataset("saved_on_disk.nc")
        self.da = ds_disk.to_array()

    ##blue

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

    def minichisqfunc_single(self,theta_r1_sq,g1,T1,Z1,ebv1,valid_filters_this_row,curr_row):

        mean_models = []
        interpolist = self.interpolate(g1,10000*T1,Z1,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models.append(interpolist[i]*(theta_r1_sq*1e-24)*10**(-0.4*(ebv1*(extinctolist[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        mean_chi2 = sum(summands)
        return mean_models, mean_chi2

    def minichisqfunc2_single(self,theta_r1_sq,g1,T1,Z1,ebv1,valid_filters_this_row,curr_row):
        if self.silent is False:
            print("Fitting theta_r1 to mean parameters: Testing row {} with mean log(g1), mean T1/10000, mean Z1, theta_r1_sq/1e-24, mean ebv1: ".format(self.rows[curr_row]+2), g1,T1,Z1,theta_r1_sq,ebv1)

        mean_models = []
        interpolist = self.interpolate(g1,10000*T1,Z1,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models.append(interpolist[i]*(theta_r1_sq*1e-24)*10**(-0.4*(ebv1*(extinctolist[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        new_chi2 = sum(summands)
        if self.silent is False:
            print("chi2 ", new_chi2)

        return new_chi2

    def minichisqfunc_double(self,theta_r1_sq,theta_r2_sq,g1,T1,Z1,ebv1,T2,ebv2,valid_filters_this_row,curr_row):
      
        mean_models1 = []
        interpolist1 = self.interpolate(g1,10000*T1,Z1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models1.append(interpolist1[i]*(theta_r1_sq*1e-24)*10**(-0.4*(ebv1*(extinctolist1[i]+3.001))))
        mean_models2 = []
        interpolist2 = self.interpolate(2.5,10000*T2,-1.5,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models2.append(interpolist2[i]*(theta_r2_sq*1e-24)*10**(-0.4*(ebv2*(extinctolist2[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i] - mean_models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        mean_chisq = sum(summands)
        return mean_models1, mean_models2, mean_chisq

    def minichisqfunc2_double(self,tup,g1,T1,Z1,ebv1,T2,ebv2,valid_filters_this_row,curr_row):
        theta_r1_sq,theta_r2_sq = tup

        if self.silent is False:
            print("Fitting thetas to mean parameters: Testing row {} with mean log(g1), mean T1/10000, mean Z1, theta_r1_sq/1e-24, mean E_bv1, mean T2/10000, theta_r2_sq, mean E_bv2: ".format(self.rows[curr_row]+2), g1, T1, Z1, theta_r1_sq, ebv1, T2, theta_r2_sq, ebv2)

        mean_models1 = []
        interpolist1 = self.interpolate(g1,10000*T1,Z1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models1.append(interpolist1[i]*(theta_r1_sq*1e-24)*10**(-0.4*(ebv1*(extinctolist1[i]+3.001))))
        mean_models2 = []
        interpolist2 = self.interpolate(2.5,10000*T2,-1.5,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models2.append(interpolist2[i]*(theta_r2_sq*1e-24)*10**(-0.4*(ebv2*(extinctolist2[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i] - mean_models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        new_chi2 = sum(summands)
        if self.silent is False:
            print("chisq: ",new_chi2,"\n")
        
        return new_chi2

    def chisqfunc(self,theta_r1_sq,g1,T1,Z1,ebv1,valid_filters_this_row,curr_row):
        if self.silent is False:
            print("Testing row {} with grid log(g1), grid T1/10000, grid Z1, theta_r1_sq/1e-24, grid ebv1: ".format(self.rows[curr_row]+2), g1,T1,Z1,theta_r1_sq,ebv1)

        models = []
        interpolist = self.interpolate(g1,10000*T1,Z1,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models.append(interpolist[i]*(theta_r1_sq*1e-24)*10**(-0.4*(ebv1*(extinctolist[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)
        if self.silent is False:
            print("chisq: ",chisq,"\n")

        return chisq

    def analyticfunc(self,g1,T1,Z1,ebv1,valid_filters_this_row,curr_row):

        if self.silent is False:
            print("Finding theta_r_sq/1e-24 analytically for row {} with grid log(g1), grid T1/10000, grid Z1, grid ebv1: ".format(self.rows[curr_row]+2), g1,T1,Z1,ebv1)

        modelsnoThetarsq = []
        interpolist = self.interpolate(g1,10000*T1,Z1,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            modelsnoThetarsq.append(interpolist[i]*10**(-0.4*(ebv1*(extinctolist[i]+3.001))))

        Tf1summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            Tf1summands.append((self.bandfluxes.iat[curr_row,valid_ind]*modelsnoThetarsq[i])/(self.bandfluxerrors.iat[curr_row,valid_ind])**2)
        Tf1 = sum(Tf1summands)

        Tm11summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            Tm11summands.append((modelsnoThetarsq[i]/(self.bandfluxerrors.iat[curr_row,valid_ind]))**2)
        Tm11 = sum(Tm11summands)

        thetarsq = Tf1/Tm11*1e24

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - thetarsq*modelsnoThetarsq[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)
        if self.silent is False:
            print("theta_r_sq/1e-24, chisq: ",thetarsq,chisq,"\n")

        return thetarsq,chisq

    def chisqfunc2(self,tup,g1,T1,Z1,ebv1,T2,ebv2,valid_filters_this_row,curr_row):
        theta_r1_sq,theta_r2_sq = tup
        if self.silent is False:
            print("Testing row {} with grid log(g1), grid T1/10000, grid Z1, theta_r1_sq/1e-24, grid E_bv1, grid T2/10000, theta_r2_sq/1e-24, grid E_bv2: ".format(self.rows[curr_row]+2), g1, T1, Z1, theta_r1_sq, ebv1, T2, theta_r2_sq, ebv2)

        models1 = []
        interpolist1 = self.interpolate(g1,T1*10000,Z1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(interpolist1[i]*(theta_r1_sq*1e-24)*10**(-0.4*(ebv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(2.5,T2*10000,-1.5,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(interpolist2[i]*(theta_r2_sq*1e-24)*10**(-0.4*(ebv2*(extinctolist2[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i] - models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)
        if self.silent is False:
            print("chisq: ",chisq,"\n")
        return chisq

    def analyticfunc2(self,g1,T1,Z1,ebv1,T2,ebv2,valid_filters_this_row,curr_row):
        from scipy.linalg import solve
        import numpy as np

        if self.silent is False:
            print("Finding theta_r1_sq/1e-24 and theta_r2_sq/1e-24 analytically for row {} with grid log(g1), grid T1/10000, grid Z1, grid E_bv1, grid T2/10000, grid E_bv2: ".format(self.rows[curr_row]+2), g1, T1, Z1, ebv1, T2, ebv2)

        models1noThetarsq = []
        interpolist1 = self.interpolate(g1,T1*10000,Z1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1noThetarsq.append(interpolist1[i]*10**(-0.4*(ebv1*(extinctolist1[i]+3.001))))
        models2noThetarsq = []
        interpolist2 = self.interpolate(2.5,T2*10000,-1.5,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2noThetarsq.append(interpolist2[i]*10**(-0.4*(ebv2*(extinctolist2[i]+3.001))))

        Tf1summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            Tf1summands.append((self.bandfluxes.iat[curr_row,valid_ind]*models1noThetarsq[i])/(self.bandfluxerrors.iat[curr_row,valid_ind])**2)
        Tf1 = sum(Tf1summands)

        Tf2summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            Tf2summands.append((self.bandfluxes.iat[curr_row,valid_ind]*models2noThetarsq[i])/(self.bandfluxerrors.iat[curr_row,valid_ind])**2)
        Tf2 = sum(Tf2summands)

        Tm11summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            Tm11summands.append((models1noThetarsq[i]/(self.bandfluxerrors.iat[curr_row,valid_ind]))**2)
        Tm11 = sum(Tm11summands)

        Tm12summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            Tm12summands.append((models1noThetarsq[i]*models2noThetarsq[i])/(self.bandfluxerrors.iat[curr_row,valid_ind])**2)
        Tm12 = sum(Tm12summands)

        Tm22summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            Tm22summands.append((models2noThetarsq[i]/(self.bandfluxerrors.iat[curr_row,valid_ind]))**2)
        Tm22 = sum(Tm11summands)

        Tm = np.array([[Tm11,Tm12],[Tm12,Tm22]])
        Tf = np.array([Tf1,Tf2])

        Thetarsq = solve(Tm,Tf)

        if Thetarsq[0] <= 0:
            theta_r1_sq = 0
            theta_r2_sq = Tf2/Tm22*1e24
        elif Thetarsq[1] <= 0:
            theta_r1_sq = Tf1/Tm11*1e24
            theta_r2_sq = 0
        else:
            theta_r1_sq = Thetarsq[0]*1e24
            theta_r2_sq = Thetarsq[1]*1e24

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - theta_r1_sq*models1noThetarsq[i] - theta_r2_sq*models2noThetarsq[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)
        if self.silent is False:
            print("theta_r1_sq/1e-24, theta_r2_sq/1e-24, chisq: ",theta_r1_sq,theta_r2_sq,chisq,"\n")
        return theta_r1_sq,theta_r2_sq,chisq

    def chisqfuncerror(self,theta_r_sq,mean_chi2,g,T,Z,E_bv,valid_filters_this_row,curr_row):

        models = []
        interpolist = self.interpolate(g,10000*T,Z,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models.append(interpolist[i]*(theta_r_sq*1e-24)*10**(-0.4*(E_bv*(extinctolist[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)-mean_chi2-4.72
        return chisq

    def chisqfunc2error_1(self,theta_r1_sq,mean_chi2,g1,T1,Z1,E_bv1,T2,theta_r2_sq,E_bv2,valid_filters_this_row,curr_row):

        models1 = []
        interpolist1 = self.interpolate(g1,T1*10000,Z1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(interpolist1[i]*(theta_r1_sq*1e-24)*10**(-0.4*(E_bv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(2.5,T2*10000,-1.5,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(interpolist2[i]*(theta_r2_sq*1e-24)*10**(-0.4*(E_bv2*(extinctolist2[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i] - models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)-mean_chi2-9.28
        return chisq

    def chisqfunc2error_2(self,theta_r2_sq,mean_chi2,g1,T1,Z1,theta_r1_sq,E_bv1,T2,E_bv2,valid_filters_this_row,curr_row):

        models1 = []
        interpolist1 = self.interpolate(g1,T1*10000,Z1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(interpolist1[i]*(theta_r1_sq*1e-24)*10**(-0.4*(E_bv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(2.5,T2*10000,-1.5,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(interpolist2[i]*(theta_r2_sq*1e-24)*10**(-0.4*(E_bv2*(extinctolist2[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i] - models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)-mean_chi2-9.28
        return chisq

    def minimize_chisq(self):
        import numpy as np
        from math import exp, sqrt
        from scipy.optimize import Bounds

        if self.single_star == True:
            bnds = Bounds([self.thetabound1lo],[self.thetabound1hi])
            x0 = np.array([(self.thetabound1lo+self.thetabound1hi)/2*(self.thetabound1lo+self.thetabound1hi)/2])

            self.mean_g1s = []
            self.mean_T1s = []
            self.mean_Z1s = []
            self.mean_theta_r1s = []
            self.mean_ebv1s = []
            
            self.var_g1s = []
            self.var_T1s = []
            self.var_Z1s = []
            self.var_theta_r1s = []
            self.var_ebv1s = []

            self.sigma_g1s = []
            self.sigma_T1s = []
            self.sigma_Z1s = []
            self.sigma_theta_r1s = []
            self.sigma_ebv1s = []

            self.gridThetars = []
            self.gridChisqs = []

            self.smallest_chi2s = []
            self.smallest_chi2_params = []

            self.newtheta_r1s = []
            self.newchi2s = []
            
            for curr_row in range(self.bandfluxes.shape[0]): 
                valid_filters_this_row = []
                for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
                    if np.isnan(bandflux) == False:
                        valid_filters_this_row.append(valid_ind)

                gridChisq = np.zeros((self.g1num,self.T1num,self.Z1num,self.ebv1num))
                gridThetar = np.zeros((self.g1num,self.T1num,self.Z1num,self.ebv1num))
                Wtot = 0
                smallest_chi2 = 1e14
                smallest_chi2_params = np.zeros(5)
                for i in range(self.g1num):
                    for j in range(self.T1num):
                        for k in range(self.Z1num):
                            for l in range(self.ebv1num):
                                g1 = self.g1grid[i,j,k,l]
                                T1 = self.T1grid[i,j,k,l]
                                Z1 = self.Z1grid[i,j,k,l]
                                ebv1 = self.ebv1grid[i,j,k,l]
                                if self.solvemethod == 0:
                                    res = opt.minimize(self.chisqfunc, x0, args=(g1,T1,Z1,ebv1,valid_filters_this_row,curr_row,), bounds=bnds)
                                    chi2 = res.fun
                                    theta_r1 = sqrt(res.x[0])
                                elif self.solvemethod == 1:
                                    theta_r1, chi2 = self.analyticfunc(g1,T1,Z1,ebv1,valid_filters_this_row,curr_row)
                                gridChisq[i,j,k,l] = chi2
                                gridThetar[i,j,k,l] = theta_r1
                                if chi2 < smallest_chi2:
                                    smallest_chi2 = chi2
                                    smallest_chi2_params[0] = g1
                                    smallest_chi2_params[1] = T1
                                    smallest_chi2_params[2] = Z1
                                    smallest_chi2_params[3] = theta_r1
                                    smallest_chi2_params[4] = ebv1

                self.smallest_chi2s.append(0)
                self.smallest_chi2s[curr_row] = smallest_chi2
                print("Smallest chi2 for row {}: {}".format(self.rows[curr_row]+2,smallest_chi2))
                self.smallest_chi2_params.append(0)
                self.smallest_chi2_params[curr_row] = smallest_chi2_params
                print("Associated parameter values: log(g1) {}, T1/10000 {}, Z1 {}, theta_r1/1e-12 {}, ebv1 {}".format(smallest_chi2_params[0],smallest_chi2_params[1],smallest_chi2_params[2],smallest_chi2_params[3],smallest_chi2_params[4]))
                gridChisq -= smallest_chi2
                self.mean_g1s.append(0)
                self.mean_T1s.append(0)
                self.mean_Z1s.append(0)
                self.mean_theta_r1s.append(0)
                self.mean_ebv1s.append(0)
                
                for i in range(self.g1num):
                    for j in range(self.T1num):
                        for k in range(self.Z1num):
                            for l in range(self.ebv1num): 
                                g1 = self.g1grid[i,j,k,l]
                                T1 = self.T1grid[i,j,k,l]
                                Z1 = self.Z1grid[i,j,k,l]
                                theta_r1 = gridThetar[i,j,k,l]
                                ebv1 = self.ebv1grid[i,j,k,l]
                                chi2 = gridChisq[i,j,k,l]

                                Wtot += exp(-chi2/2)
                                self.mean_g1s[curr_row] += exp(-chi2/2)*g1
                                self.mean_T1s[curr_row] += exp(-chi2/2)*T1
                                self.mean_Z1s[curr_row] += exp(-chi2/2)*Z1
                                self.mean_theta_r1s[curr_row] += exp(-chi2/2)*theta_r1
                                self.mean_ebv1s[curr_row] += exp(-chi2/2)*ebv1
                                
                self.mean_g1s[curr_row] /= Wtot
                self.mean_T1s[curr_row] /= Wtot
                self.mean_Z1s[curr_row] /= Wtot
                self.mean_theta_r1s[curr_row] /= Wtot
                self.mean_ebv1s[curr_row] /= Wtot

                print("weighted mean log(g1) ", self.mean_g1s[curr_row])
                print("weighted mean T1/10000 ", self.mean_T1s[curr_row])
                print("weighted mean Z1 ", self.mean_Z1s[curr_row])
                print("weighted mean theta_r1/1e-12 ", self.mean_theta_r1s[curr_row])
                print("weighted mean ebv1 ", self.mean_ebv1s[curr_row])

                self.var_g1s.append(0)
                self.var_T1s.append(0)
                self.var_Z1s.append(0)
                self.var_theta_r1s.append(0)
                self.var_ebv1s.append(0)

                self.sigma_g1s.append(0)
                self.sigma_T1s.append(0)
                self.sigma_Z1s.append(0)
                self.sigma_theta_r1s.append(0)
                self.sigma_ebv1s.append(0)

                for i in range(self.g1num):
                    for j in range(self.T1num):
                        for k in range(self.Z1num):
                            for l in range(self.ebv1num):
                                g1 = self.g1grid[i,j,k,l]
                                T1 = self.T1grid[i,j,k,l]
                                Z1 = self.Z1grid[i,j,k,l]
                                theta_r1 = gridThetar[i,j,k,l]
                                ebv1 = self.ebv1grid[i,j,k,l]
                                chi2 = gridChisq[i,j,k,l]

                                self.var_g1s[curr_row] += exp(-chi2/2)*(g1-self.mean_g1s[curr_row])*(g1-self.mean_g1s[curr_row])
                                self.var_T1s[curr_row] += exp(-chi2/2)*(T1-self.mean_T1s[curr_row])*(T1-self.mean_T1s[curr_row])
                                self.var_Z1s[curr_row] += exp(-chi2/2)*(Z1-self.mean_Z1s[curr_row])*(Z1-self.mean_Z1s[curr_row])
                                self.var_theta_r1s[curr_row] += exp(-chi2/2)*(theta_r1-self.mean_theta_r1s[curr_row])*(theta_r1-self.mean_theta_r1s[curr_row])
                                self.var_ebv1s[curr_row] += exp(-chi2/2)*(ebv1-self.mean_ebv1s[curr_row])*(ebv1-self.mean_ebv1s[curr_row])
                                
                gridChisq += smallest_chi2
                self.gridThetars.append(gridThetar.flatten())
                self.gridChisqs.append(gridChisq.flatten())
                                
                self.var_g1s[curr_row] /= Wtot
                self.var_T1s[curr_row] /= Wtot
                self.var_Z1s[curr_row] /= Wtot
                self.var_theta_r1s[curr_row] /= Wtot
                self.var_ebv1s[curr_row] /= Wtot

                self.sigma_g1s[curr_row] = sqrt(self.var_g1s[curr_row])
                self.sigma_T1s[curr_row] = sqrt(self.var_T1s[curr_row])
                self.sigma_Z1s[curr_row] = sqrt(self.var_Z1s[curr_row])
                self.sigma_theta_r1s[curr_row] = sqrt(self.var_theta_r1s[curr_row])
                self.sigma_ebv1s[curr_row] = sqrt(self.var_ebv1s[curr_row])

                print("weighted var log(g1) ", self.var_g1s[curr_row])
                print("sigma log(g1) (sqrt weighted var log(g1)) ", self.sigma_g1s[curr_row])
                print("weighted var T1/10000 ", self.var_T1s[curr_row])
                print("sigma T1/10000 (sqrt weighted var T1/10000) ", self.sigma_T1s[curr_row])
                print("weighted var Z1 ", self.var_Z1s[curr_row])
                print("sigma Z1 (sqrt weighted var Z1) ", self.sigma_Z1s[curr_row])
                print("weighted var theta_r1/1e-12 ", self.var_theta_r1s[curr_row])
                print("sigma theta_r1/1e-12 (sqrt weighted var theta r1) ", self.sigma_theta_r1s[curr_row])
                print("weighted var ebv1 ", self.var_ebv1s[curr_row])
                print("sigma ebv1 (sqrt weighted var ebv1) ", self.sigma_ebv1s[curr_row])

                x02 = np.array([self.mean_theta_r1s[curr_row]*self.mean_theta_r1s[curr_row]])
                res2 = opt.minimize(self.minichisqfunc2_single, x02, args=(self.mean_g1s[curr_row],self.mean_T1s[curr_row],self.mean_Z1s[curr_row],self.mean_ebv1s[curr_row],valid_filters_this_row,curr_row,), bounds=bnds)

                newchi2 = res2.fun
                newtheta_r1 = sqrt(res2.x[0])

                print("chi2 of fitted theta_r1/1e-12 to mean parameters: ", newchi2)
                print("fitted theta_r1/1e-12: ", newtheta_r1)

                self.newchi2s.append(newchi2)
                self.newtheta_r1s.append(newtheta_r1)
        
        elif self.double_star == True:
            bnds = Bounds([self.thetabound1lo,self.thetabound2lo],[self.thetabound1hi,self.thetabound2hi])
            x0 = np.array([(self.thetabound1lo+self.thetabound1hi)/2*(self.thetabound1lo+self.thetabound1hi)/2,(self.thetabound2lo+self.thetabound2hi)/2*(self.thetabound2lo+self.thetabound2hi)/2])
            self.mean_g1s = []
            self.mean_T1s = []
            self.mean_Z1s = []
            self.mean_theta_r1s = []
            self.mean_ebv1s = []
            self.mean_T2s = []
            self.mean_theta_r2s = []
            self.mean_ebv2s = []
            
            self.var_g1s = []
            self.var_T1s = []
            self.var_Z1s = []
            self.var_theta_r1s = []
            self.var_ebv1s = []
            self.var_T2s = []
            self.var_theta_r2s = []
            self.var_ebv2s = []

            self.sigma_g1s = []
            self.sigma_T1s = []
            self.sigma_Z1s = []
            self.sigma_theta_r1s = []
            self.sigma_ebv1s = []
            self.sigma_T2s = []
            self.sigma_theta_r2s = []
            self.sigma_ebv2s = []

            self.gridThetar1s = []
            self.gridThetar2s = []
            self.gridChisqs = []

            self.smallest_chi2s = []
            self.smallest_chi2_params = []

            self.newtheta_r1s = []
            self.newtheta_r2s = []
            self.newchi2s = []
            
            for curr_row in range(self.bandfluxes.shape[0]): 
                valid_filters_this_row = []
                for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
                    if np.isnan(bandflux) == False:
                        valid_filters_this_row.append(valid_ind)

                gridChisq = np.zeros((self.g1num,self.T1num,self.Z1num,self.ebv1num,self.T2num,self.ebv2num))
                gridThetar1 = np.zeros((self.g1num,self.T1num,self.Z1num,self.ebv1num,self.T2num,self.ebv2num))
                gridThetar2 = np.zeros((self.g1num,self.T1num,self.Z1num,self.ebv1num,self.T2num,self.ebv2num))
                Wtot = 0
                smallest_chi2 = 1e14
                smallest_chi2_params = np.zeros(8)
                for i in range(self.g1num):
                    for j in range(self.T1num):
                        for k in range(self.Z1num):
                            for l in range(self.ebv1num):
                                for m in range(self.T2num):
                                    for n in range(self.ebv2num):
                                        g1 = self.g1grid[i,j,k,l,m,n]
                                        T1 = self.T1grid[i,j,k,l,m,n]
                                        Z1 = self.Z1grid[i,j,k,l,m,n]
                                        ebv1 = self.ebv1grid[i,j,k,l,m,n]
                                        T2 = self.T2grid[i,j,k,l,m,n]
                                        ebv2 = self.ebv2grid[i,j,k,l,m,n]
                                        if self.solvemethod == 0:
                                            res = opt.minimize(self.chisqfunc2, x0, args=(g1,T1,Z1,ebv1,T2,ebv2,valid_filters_this_row,curr_row,), bounds=bnds)
                                            chi2 = res.fun
                                            theta_r1 = sqrt(res.x[0])
                                            theta_r2 = sqrt(res.x[1])
                                        elif self.solvemethod == 1:
                                            theta_r1, theta_r2, chi2 = self.analyticfunc2(g1,T1,Z1,ebv1,T2,ebv2,valid_filters_this_row,curr_row)
                                        gridChisq[i,j,k,l,m,n] = chi2
                                        gridThetar1[i,j,k,l,m,n] = theta_r1
                                        gridThetar2[i,j,k,l,m,n] = theta_r2
                                        if chi2 < smallest_chi2:
                                            smallest_chi2 = chi2
                                            smallest_chi2_params[0] = g1
                                            smallest_chi2_params[1] = T1
                                            smallest_chi2_params[2] = Z1
                                            smallest_chi2_params[3] = theta_r1
                                            smallest_chi2_params[4] = ebv1
                                            smallest_chi2_params[5] = T2
                                            smallest_chi2_params[6] = theta_r2
                                            smallest_chi2_params[7] = ebv2

                self.smallest_chi2s.append(0)
                self.smallest_chi2s[curr_row] = smallest_chi2
                print("Smallest chi2 for row {}: {}".format(self.rows[curr_row]+2,smallest_chi2))
                self.smallest_chi2_params.append(0)
                self.smallest_chi2_params[curr_row] = smallest_chi2_params
                print("Associated parameter values: log(g1) {}, T1/10000 {}, Z1 {}, theta_r1/1e-12 {}, ebv1 {}, T2/10000 {}, theta_r2/1e-12 {}, ebv2 {}".format(smallest_chi2_params[0],smallest_chi2_params[1],smallest_chi2_params[2],smallest_chi2_params[3],smallest_chi2_params[4],smallest_chi2_params[5],smallest_chi2_params[6],smallest_chi2_params[7]))
                gridChisq -= smallest_chi2
                self.mean_g1s.append(0)
                self.mean_T1s.append(0)
                self.mean_Z1s.append(0)
                self.mean_theta_r1s.append(0)
                self.mean_ebv1s.append(0)
                self.mean_T2s.append(0)
                self.mean_theta_r2s.append(0)
                self.mean_ebv2s.append(0)
                
                for i in range(self.g1num):
                    for j in range(self.T1num):
                        for k in range(self.Z1num):
                            for l in range(self.ebv1num): 
                                for m in range(self.T2num):
                                    for n in range(self.ebv2num):
                                        g1 = self.g1grid[i,j,k,l,m,n]
                                        T1 = self.T1grid[i,j,k,l,m,n]
                                        Z1 = self.Z1grid[i,j,k,l,m,n]
                                        theta_r1 = gridThetar1[i,j,k,l,m,n]
                                        ebv1 = self.ebv1grid[i,j,k,l,m,n]
                                        T2 = self.T2grid[i,j,k,l,m,n]
                                        theta_r2 = gridThetar2[i,j,k,l,m,n]
                                        ebv2 = self.ebv2grid[i,j,k,l,m,n]
                                        chi2 = gridChisq[i,j,k,l,m,n]

                                        Wtot += exp(-chi2/2)
                                        self.mean_g1s[curr_row] += exp(-chi2/2)*g1
                                        self.mean_T1s[curr_row] += exp(-chi2/2)*T1
                                        self.mean_Z1s[curr_row] += exp(-chi2/2)*Z1
                                        self.mean_theta_r1s[curr_row] += exp(-chi2/2)*theta_r1
                                        self.mean_ebv1s[curr_row] += exp(-chi2/2)*ebv1
                                        self.mean_T2s[curr_row] += exp(-chi2/2)*T2
                                        self.mean_theta_r2s[curr_row] += exp(-chi2/2)*theta_r2
                                        self.mean_ebv2s[curr_row] += exp(-chi2/2)*ebv2
                                
                self.mean_g1s[curr_row] /= Wtot
                self.mean_T1s[curr_row] /= Wtot
                self.mean_Z1s[curr_row] /= Wtot
                self.mean_theta_r1s[curr_row] /= Wtot
                self.mean_ebv1s[curr_row] /= Wtot
                self.mean_T2s[curr_row] /= Wtot
                self.mean_theta_r2s[curr_row] /= Wtot
                self.mean_ebv2s[curr_row] /= Wtot

                print("weighted mean log(g1) ", self.mean_g1s[curr_row])
                print("weighted mean T1/10000 ", self.mean_T1s[curr_row])
                print("weighted mean Z1 ", self.mean_Z1s[curr_row])
                print("weighted mean theta r1/1e-12 ", self.mean_theta_r1s[curr_row])
                print("weighted mean ebv1 ", self.mean_ebv1s[curr_row])
                print("weighted mean T2/10000 ", self.mean_T2s[curr_row])
                print("weighted mean theta r2/1e-12 ", self.mean_theta_r2s[curr_row])
                print("weighted mean ebv2 ", self.mean_ebv2s[curr_row])

                self.var_g1s.append(0)
                self.var_T1s.append(0)
                self.var_Z1s.append(0)
                self.var_theta_r1s.append(0)
                self.var_ebv1s.append(0)
                self.var_T2s.append(0)
                self.var_theta_r2s.append(0)
                self.var_ebv2s.append(0)

                self.sigma_g1s.append(0)
                self.sigma_T1s.append(0)
                self.sigma_Z1s.append(0)
                self.sigma_theta_r1s.append(0)
                self.sigma_ebv1s.append(0)
                self.sigma_T2s.append(0)
                self.sigma_theta_r2s.append(0)
                self.sigma_ebv2s.append(0)

                for i in range(self.g1num):
                    for j in range(self.T1num):
                        for k in range(self.Z1num):
                            for l in range(self.ebv1num):
                                for m in range(self.T2num):
                                    for n in range(self.ebv2num):
                                        g1 = self.g1grid[i,j,k,l,m,n]
                                        T1 = self.T1grid[i,j,k,l,m,n]
                                        Z1 = self.Z1grid[i,j,k,l,m,n]
                                        theta_r1 = gridThetar1[i,j,k,l,m,n]
                                        ebv1 = self.ebv1grid[i,j,k,l,m,n]
                                        T2 = self.T1grid[i,j,k,l,m,n]
                                        theta_r2 = gridThetar2[i,j,k,l,m,n]
                                        ebv2 = self.ebv2grid[i,j,k,l,m,n]
                                        chi2 = gridChisq[i,j,k,l,m,n]

                                        self.var_g1s[curr_row] += exp(-chi2/2)*(g1-self.mean_g1s[curr_row])*(g1-self.mean_g1s[curr_row])
                                        self.var_T1s[curr_row] += exp(-chi2/2)*(T1-self.mean_T1s[curr_row])*(T1-self.mean_T1s[curr_row])
                                        self.var_Z1s[curr_row] += exp(-chi2/2)*(Z1-self.mean_Z1s[curr_row])*(Z1-self.mean_Z1s[curr_row])
                                        self.var_theta_r1s[curr_row] += exp(-chi2/2)*(theta_r1-self.mean_theta_r1s[curr_row])*(theta_r1-self.mean_theta_r1s[curr_row])
                                        self.var_ebv1s[curr_row] += exp(-chi2/2)*(ebv1-self.mean_ebv1s[curr_row])*(ebv1-self.mean_ebv1s[curr_row])
                                        self.var_T2s[curr_row] += exp(-chi2/2)*(T2-self.mean_T2s[curr_row])*(T2-self.mean_T2s[curr_row])
                                        self.var_theta_r2s[curr_row] += exp(-chi2/2)*(theta_r2-self.mean_theta_r2s[curr_row])*(theta_r2-self.mean_theta_r2s[curr_row])
                                        self.var_ebv2s[curr_row] += exp(-chi2/2)*(ebv2-self.mean_ebv2s[curr_row])*(ebv2-self.mean_ebv2s[curr_row])
                                
                gridChisq += smallest_chi2
                self.gridThetar1s.append(gridThetar1.flatten())
                self.gridThetar2s.append(gridThetar2.flatten())
                self.gridChisqs.append(gridChisq.flatten())
                                
                self.var_g1s[curr_row] /= Wtot
                self.var_Z1s[curr_row] /= Wtot
                self.var_T1s[curr_row] /= Wtot
                self.var_theta_r1s[curr_row] /= Wtot
                self.var_ebv1s[curr_row] /= Wtot
                self.var_T2s[curr_row] /= Wtot
                self.var_theta_r2s[curr_row] /= Wtot
                self.var_ebv2s[curr_row] /= Wtot

                self.sigma_g1s[curr_row] = sqrt(self.var_g1s[curr_row])
                self.sigma_Z1s[curr_row] = sqrt(self.var_Z1s[curr_row])
                self.sigma_T1s[curr_row] = sqrt(self.var_T1s[curr_row])
                self.sigma_theta_r1s[curr_row] = sqrt(self.var_theta_r1s[curr_row])
                self.sigma_ebv1s[curr_row] = sqrt(self.var_ebv1s[curr_row])
                self.sigma_T2s[curr_row] = sqrt(self.var_T2s[curr_row])
                self.sigma_theta_r2s[curr_row] = sqrt(self.var_theta_r2s[curr_row])
                self.sigma_ebv2s[curr_row] = sqrt(self.var_ebv2s[curr_row])

                print("weighted var log(g1) ", self.var_g1s[curr_row])
                print("sigma g1 (sqrt weighted var log(g1)) ", self.sigma_g1s[curr_row])
                print("weighted var T1/10000 ", self.var_T1s[curr_row])
                print("sigma T1/10000 (sqrt weighted var T1/10000) ", self.sigma_T1s[curr_row])
                print("weighted var Z1 ", self.var_Z1s[curr_row])
                print("sigma Z1 (sqrt weighted var Z1) ", self.sigma_Z1s[curr_row])
                print("weighted var theta_r1/1e-12 ", self.var_theta_r1s[curr_row])
                print("sigma theta_r1/1e-12 (sqrt weighted var theta_r1/1e-12) ", self.sigma_theta_r1s[curr_row])
                print("weighted var ebv1 ", self.var_ebv1s[curr_row])
                print("sigma ebv1 (sqrt weighted var ebv1) ", self.sigma_ebv1s[curr_row])
                print("weighted var T2/10000 ", self.var_T2s[curr_row])
                print("sigma T2/10000 (sqrt weighted var T2/10000) ", self.sigma_T2s[curr_row])
                print("weighted var theta_r2/1e-12 ", self.var_theta_r2s[curr_row])
                print("sigma theta_r2/1e-12 (sqrt weighted var theta_r2/1e-12) ", self.sigma_theta_r2s[curr_row])
                print("weighted var ebv2 ", self.var_ebv2s[curr_row])
                print("sigma ebv2 (sqrt weighted var ebv2) ", self.sigma_ebv2s[curr_row])

                x02 = np.array([self.mean_theta_r1s[curr_row]*self.mean_theta_r1s[curr_row],self.mean_theta_r2s[curr_row]*self.mean_theta_r2s[curr_row]])
                res2 = opt.minimize(self.minichisqfunc2_double, x02, args=(self.mean_g1s[curr_row],self.mean_T1s[curr_row],self.mean_Z1s[curr_row],self.mean_ebv1s[curr_row],self.mean_T2s[curr_row],self.mean_ebv2s[curr_row],valid_filters_this_row,curr_row,), bounds=bnds)

                newchi2 = res2.fun
                newtheta_r1 = sqrt(res2.x[0])
                newtheta_r2 = sqrt(res2.x[1])

                print("chi2 of fitted theta_rs/1e-12 to other mean parameters: ", newchi2)
                print("fitted theta_r1/1e-12 to other mean parameters: ", newtheta_r1)
                print("fitted theta_r2/1e-12 to other mean parameters: ", newtheta_r2)

                self.newchi2s.append(newchi2)
                self.newtheta_r1s.append(newtheta_r1)
                self.newtheta_r2s.append(newtheta_r2)
                
    ##

    def find_param_errors(self):
        import numpy as np
        from math import sqrt

        if self.single_star == True:

            self.errorsallrows = []
            for curr_row in range(self.bandfluxes.shape[0]):  
                valid_filters_this_row = []
                for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
                    if np.isnan(bandflux) == False:
                        valid_filters_this_row.append(valid_ind)
                errorsthisrow = []
                g = self.mean_g1s[curr_row]
                T = self.mean_T1s[curr_row]
                Z = self.mean_Z1s[curr_row]
                theta_r1 = self.mean_theta_r1s[curr_row]
                ebv = self.mean_ebv1s[curr_row]
                mean_models, mean_chi2 = self.minichisqfunc_single(theta_r1,g,T,Z,ebv,valid_filters_this_row,curr_row)
                #
                try:
                    theta_r1_lowererror = theta_r1 - sqrt(opt.root_scalar(self.chisqfuncerror, args=(mean_chi2,g,T,Z,ebv,valid_filters_this_row,curr_row),method="brentq",bracket=[self.thetabound1lo*self.thetabound1lo,theta_r1*theta_r1]).root)
                except:
                    theta_r1_lowererror = "N/A"
                try:
                    theta_r1_uppererror = sqrt(opt.root_scalar(self.chisqfuncerror, args=(mean_chi2,g,T,Z,ebv,valid_filters_this_row,curr_row),method="brentq",bracket=[theta_r1*theta_r1,self.thetabound1hi*self.thetabound1hi]).root)-theta_r1
                except:
                    theta_r1_squppererror = "N/A"
                errorsthisrow.append([theta_r1_lowererror,theta_r1_uppererror])
                #
                self.errorsallrows.append(errorsthisrow)


        elif self.double_star == True:
            self.errorsallrows = []
            for curr_row in range(self.bandfluxes.shape[0]):  
                valid_filters_this_row = []
                for valid_ind,bandflux in enumerate(self.bandfluxes.loc[curr_row,:]):
                    if np.isnan(bandflux) == False:
                        valid_filters_this_row.append(valid_ind)

                errorsthisrow = []
                g1 = self.mean_g1s[curr_row]
                T1 = self.mean_T1s[curr_row]
                Z1 = self.mean_Z1s[curr_row]
                theta_r1 = self.mean_theta_r1s[curr_row]
                ebv1 = self.mean_ebv1s[curr_row]
                T2 = self.mean_T2s[curr_row]
                theta_r2 = self.mean_theta_r2s[curr_row]
                ebv2 = self.mean_ebv2s[curr_row]
                mean_models1, mean_models2, mean_chi2 = self.minichisqfunc_double(theta_r1,theta_r2,g1,T1,Z1,ebv1,T2,ebv2,valid_filters_this_row,curr_row)
                #           
                try:
                    theta_r1_lowererror = theta_r1 - sqrt(opt.root_scalar(self.chisqfunc2error_1, args=(mean_chi2,g1,T1,Z1,ebv1,T2,theta_r2,ebv2,valid_filters_this_row,curr_row),method="brentq",bracket=[self.thetabound1lo*self.thetabound1lo,theta_r1*theta_r1]).root)
                except:
                    theta_r1_lowererror = "N/A"
                try:
                    theta_r1_uppererror = sqrt(opt.root_scalar(self.chisqfunc2error_1, args=(mean_chi2,g1,T1,Z1,ebv1,T2,theta_r2,ebv2,valid_filters_this_row,curr_row),method="brentq",bracket=[theta_r1*theta_r1,self.thetabound1hi*self.thetabound1hi]).root)-theta_r1
                except:
                    theta_r1_uppererror = "N/A"
                errorsthisrow.append([theta_r1_lowererror,theta_r1_uppererror])
                #           
                try:
                    theta_r2_lowererror = theta_r2 - sqrt(opt.root_scalar(self.chisqfunc2error_2, args=(mean_chi2,g1,T1,Z1,theta_r1,ebv1,T2,ebv2,valid_filters_this_row,curr_row),method="brentq",bracket=[self.thetabound2lo*self.thetabound2lo,theta_r2*theta_r2]).root)
                except:
                    theta_r2_lowererror = "N/A"
                try:
                    theta_r2_uppererror = sqrt(opt.root_scalar(self.chisqfunc2error_2, args=(mean_chi2,g1,T1,Z1,theta_r1,ebv1,T2,ebv2,valid_filters_this_row,curr_row),method="brentq",bracket=[theta_r2*theta_r2,self.thetabound2hi*self.thetabound2hi]).root) - theta_r2
                except:
                    theta_r2_uppererror = "N/A"
                errorsthisrow.append([theta_r2_lowererror,theta_r2_uppererror])
                #
                self.errorsallrows.append(errorsthisrow)

    def display_all_results(self):
        if self.dispresults == 1:
            if self.single_star == True:
                self.mean_fluxes = []
                self.mean_chi2s = []
                for curr_row in range(self.bandfluxes.shape[0]): 
                    self.display_results_single(curr_row)
            elif self.double_star == True:
                self.mean_hotfluxes = []
                self.mean_coolfluxes = []
                self.mean_chi2s = []
                for curr_row in range(self.bandfluxes.shape[0]): 
                    self.display_results_double(curr_row)

    ##purple

    def save_output(self):

        import numpy as np
        import pandas as pd

        if self.weightedmeanvarresults == 1:
            
            if self.single_star == True:

                df1 = pd.DataFrame({
                    'row' : [i+2 for i in self.rows],
                    'weighted_mean_log(g1)' : self.mean_g1s,
                    'sigma_log(g1)' : self.sigma_g1s,
                    'weighted_mean_T1/10000' : self.mean_T1s,
                    'sigma_T1/10000 ' : self.sigma_T1s,
                    'weighted_mean_Z1' : self.mean_Z1s,
                    'sigma_Z1 ' : self.sigma_Z1s,
                    'weighted_mean_theta_r1/1e-12' : self.mean_theta_r1s,
                    'sigma_theta_r1/1e-12 ' : self.sigma_theta_r1s,
                    'weighted_mean_ebv1' : self.mean_ebv1s,
                    'sigma_ebv1 ' : self.sigma_ebv1s,
                    'chi2_using_mean_parameters' : self.mean_chi2s,
                    'fitted_theta_r1/1e-12_to_mean_parameters' : self.newtheta_r1s,
                    'chi2_of_fitted_theta_r1/1e-12' : self.newchi2s})

                try:
                    df1.to_csv("{}".format(self.weightedmeanvarname),index=False)
                except:
                    import tkinter as tk
                    from tkinter import messagebox
                    tk.messagebox.showerror('Error','An error occurred. This can happen if a file is open while trying to overwrite it. Please close any relevant files and try again.')  
        
            elif self.double_star == True:

                df1 = pd.DataFrame({
                    'row' : [i+2 for i in self.rows],
                    'weighted_mean_log(g1)' : self.mean_g1s,
                    'sigma_log(g1)' : self.sigma_g1s,
                    'weighted_mean_T1/10000' : self.mean_T1s,
                    'sigma_T1/10000' : self.sigma_T1s,
                    'weighted_mean_Z1' : self.mean_Z1s,
                    'sigma_Z1' : self.sigma_Z1s,
                    'weighted_mean_theta_r1' : self.mean_theta_r1s,
                    'sigma_theta_r1' : self.sigma_theta_r1s,
                    'weighted_mean_ebv1' : self.mean_ebv1s,
                    'sigma_ebv1' : self.sigma_ebv1s,
                    'weighted_mean_T2/10000' : self.mean_T2s,
                    'sigma_T2/10000' : self.sigma_T2s,
                    'weighted_mean_theta_r2' : self.mean_theta_r2s,
                    'sigma_theta_r2' : self.sigma_theta_r2s,
                    'weighted_mean_ebv2' : self.mean_ebv2s,
                    'sigma_ebv2' : self.sigma_ebv2s,
                    'chi2_using_mean_parameters' : self.mean_chi2s,
                    'fitted_theta_r1_to_mean_parameters' : self.newtheta_r1s,
                    'fitted_theta_r2_to_mean_parameters' : self.newtheta_r2s,
                    'chi2_of_fitted_thetas' : self.newchi2s})

                try:
                    df1.to_csv("{}".format(self.weightedmeanvarname),index=False)
                except:
                    import tkinter as tk
                    from tkinter import messagebox
                    tk.messagebox.showerror('Error','An error occurred. This can happen if a file is open while trying to overwrite it. Please close any relevant files and try again.')  

        if self.gridresults == 1:

            if self.single_star == True:

                for curr_row in range(self.bandfluxes.shape[0]):

                    a = pd.DataFrame({
                        'log(g)' : self.g1grid.flatten(),
                        'temperature/10000' : self.T1grid.flatten(),
                        'abundance' : self.Z1grid.flatten(),
                        'theta_r/1e-12' : self.gridThetars[curr_row],
                        'E(B-V)' : self.ebv1grid.flatten(),
                        'Chi squared' : self.gridChisqs[curr_row]})
                    
                    parts = self.gridname.split(".")
                    numbered_gridname = parts[0] + str(self.rows[curr_row]+2) + "." + parts[1]

                    try:
                        a.to_csv("{}".format(numbered_gridname),index=False)
                    except:
                        import tkinter as tk
                        from tkinter import messagebox
                        tk.messagebox.showerror('Error','An error occurred. This can happen if a file is open while trying to overwrite it. Please close any relevant files and try again.')             
            
            elif self.double_star == True:

                for curr_row in range(self.bandfluxes.shape[0]):

                    a = pd.DataFrame({
                        'log(g_hot)' : self.g1grid.flatten(),
                        'temperature_hot/10000' : self.T1grid.flatten(),
                        'abundance_hot' : self.Z1grid.flatten(),
                        'theta_r_hot/1e-12' : self.gridThetar1s[curr_row],
                        'E(B-V)_hot' : self.ebv1grid.flatten(),
                        'temperature_cool/10000' : self.T2grid.flatten(),
                        'theta_r_cool/1e-12' : self.gridThetar2s[curr_row],
                        'E(B-V)_cool' : self.ebv2grid.flatten(),
                        'Chi squared' : self.gridChisqs[curr_row]})
                    
                    parts = self.gridname.split(".")
                    numbered_gridname = parts[0] + str(self.rows[curr_row]+2) + "." + parts[1]

                    try:
                        a.to_csv("{}".format(numbered_gridname),index=False)
                    except:
                        import tkinter as tk
                        from tkinter import messagebox
                        tk.messagebox.showerror('Error','An error occurred. This can happen if a file is open while trying to overwrite it. Please close any relevant files and try again.')             
    ##

    ##red
 
    def display_results_single(self,curr_row):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        topw = tk.Tk()
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

        valid_actualfilters_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_actualfilters_this_row.append(self.filternames[valid_ind])
    
        fig = Figure(figsize=(8.75,5))
        abc = fig.add_subplot(111)
        abc.scatter(valid_avgwv_this_row,valid_fluxes_this_row,color="orange")
        abc.set_xlabel("Wavelength [nm]")
        abc.set_ylabel("Flux [mJy]")
        abc.set_title("Source at row {}".format(self.rows[curr_row]+2))
        #abc.errorbar(valid_avgwv_this_row,valid_fluxes_this_row,yerr=valid_errors_this_row,fmt="o",color="orange")
        mean_models, mean_chi2 = self.minichisqfunc_single(self.mean_theta_r1s[curr_row]*self.mean_theta_r1s[curr_row],self.mean_g1s[curr_row],self.mean_T1s[curr_row],self.mean_Z1s[curr_row],self.mean_ebv1s[curr_row],valid_filters_this_row,curr_row)
        print("\nchi2 of mean parameters: ", mean_chi2,"\n")
        abc.plot(valid_avgwv_this_row,mean_models,color="blue")

        if self.plotscale == 1:
            pass
        elif self.plotscale == 0:
            abc.set_xscale('log')
            abc.set_yscale('log')
            abc.set_xticks([150,171,199,276,337,476,833,1097,1522])
            abc.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

        if self.saveplots == 1:
            saveimgname = self.imgfilename.replace("X","{}".format(self.rows[curr_row]+2))
            fig.savefig('{}'.format(saveimgname), bbox_inches='tight', dpi=150)

        canvas = FigureCanvasTkAgg(fig, master=topw)
        canvas.get_tk_widget().pack(anchor=tk.E)
        canvas.draw()

        label1 = tk.Label(topw,text="Average wavelength of each filter (x):")
        label1.place(x=50,y=20)
        textbox1 = tk.Text(topw,height=6,width=30)
        for filtername,avgwv in zip(valid_actualfilters_this_row,valid_avgwv_this_row):
            textbox1.insert(tk.END,"{}      {}\n".format(filtername,avgwv))
        textbox1.place(x=50,y=50)
        label2 = tk.Label(topw,text="Bandfluxes (y, orange):")
        label2.place(x=50,y=220)
        textbox2 = tk.Text(topw,height=6,width=30)
        for filtername,bf in zip(valid_actualfilters_this_row,valid_fluxes_this_row):
            textbox2.insert(tk.END,"{}      {}\n".format(filtername,format(bf,'.8e')))
        textbox2.place(x=50,y=250)
        label3 = tk.Label(topw,text="Bandflux errors:")
        label3.place(x=50,y=420)
        textbox3 = tk.Text(topw,height=6,width=30)
        for filtername,bfe in zip(valid_actualfilters_this_row,valid_errors_this_row):
            textbox3.insert(tk.END,"{}      {}\n".format(filtername,format(bfe,'.8e')))
        textbox3.place(x=50,y=450)
        label4 = tk.Label(topw,text="Model fluxes (y, blue):")
        label4.place(x=50,y=620)
        textbox4 = tk.Text(topw,height=6,width=30)
        self.mean_fluxes.append(0)
        for filtername,mod in zip(valid_actualfilters_this_row,mean_models):
            self.mean_fluxes[curr_row] += mod
            textbox4.insert(tk.END,"{}      {}\n".format(filtername,format(mod,'.8e')))
        print("total model flux using weighted mean parameters: {}".format(self.mean_fluxes[curr_row]))
        textbox4.place(x=50,y=650)
        groove = tk.Canvas(topw,width=215,height=120,bd=4,relief=tk.RIDGE)
        groove.place(x=405,y=655)
        label5 = tk.Label(topw,text="chi^2 value using \nweighted mean parameters")
        label5.place(x=425,y=665)
        label5a = tk.Label(topw,text="{}".format(format(mean_chi2,'.6e')),font=("Arial",12))
        label5a.place(x=445,y=725)
        ridge = tk.Canvas(topw,width=600,height=300,bd=4,relief=tk.GROOVE)
        ridge.place(x=875,y=630)
        self.mean_chi2s.append(0)
        self.mean_chi2s[curr_row] = mean_chi2
        #label6 = tk.Label(topw,text="Best fit parameters",pady=15)
        #label6.place(x=865,y=725)
        labelheader = tk.Label(topw,text="Parameter                        Weighted mean             Error_lower             Error_upper",bd=4,relief=tk.GROOVE,padx=40,bg="azure")
        labelheader.place(x=878,y=603) 
        import math
        log_g_sticker1 = format(self.mean_g1s[curr_row],'.6e')

        label7 = tk.Label(topw,text="log_g                  =             {}".format(log_g_sticker1))
        label7.place(x=910,y=648)

        temp_sticker1 = format(self.mean_T1s[curr_row]*10000,'.6e') 
        label8= tk.Label(topw,text = "temperature       =             {}".format(temp_sticker1))
        label8.place(x=910,y=683)

        abundance_sticker1 = format(self.mean_Z1s[curr_row],'.6e')
        label9 = tk.Label(topw, text = "abundance         =              {}".format(abundance_sticker1))
        label9.place(x=910,y=718)

        theta_r_sticker1 = format(self.mean_theta_r1s[curr_row]*1e-12,'.6e')
        try:
            theta_r_sticker2 = format(self.errorsallrows[curr_row][0][0],'.6e')
        except:
            theta_r_sticker2 = "       N/A       "
        try:
            theta_r_sticker3 = format(self.errorsallrows[curr_row][0][1],'.6e')
        except:
            theta_r_sticker3 = "       N/A       "
        label10 = tk.Label(topw,text="theta_r                =              {}        ({})        ({})".format(theta_r_sticker1,theta_r_sticker2,theta_r_sticker3))
        label10.place(x=910,y=753)

        ebv_sticker1 = format(self.mean_ebv1s[curr_row],'.6e')
        label11 = tk.Label(topw,text="E(b-v)                 =              {}".format(ebv_sticker1))
        label11.place(x=910,y=788)

        def closethesource():
            topw.destroy()
        byebyebutt = tk.Button(topw, bd=3, font="Arial 10", text="Next source",command=closethesource,padx=30,pady=5)
        byebyebutt.place(x=423,y=830)
        topw.mainloop()

    def display_results_double(self,curr_row):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        topw = tk.Tk()
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

        valid_actualfilters_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_actualfilters_this_row.append(self.filternames[valid_ind])
    

        fig = Figure(figsize=(8.75,5))
        abc = fig.add_subplot(111)
        abc.scatter(valid_avgwv_this_row,valid_fluxes_this_row,color="orange")
        abc.set_xlabel("Wavelength [nm]")
        abc.set_ylabel("Flux [mJy]")
        abc.set_title("Source at row {}".format(self.rows[curr_row]+2))
        #abc.errorbar(valid_avgwv_this_row,valid_fluxes_this_row,yerr=valid_errors_this_row,fmt="o",color="orange")
        hotmodels, coolmodels, mean_chi2 = self.minichisqfunc_double(self.mean_theta_r1s[curr_row]*self.mean_theta_r1s[curr_row], self.mean_theta_r2s[curr_row]*self.mean_theta_r2s[curr_row], self.mean_g1s[curr_row],self.mean_T1s[curr_row],self.mean_Z1s[curr_row],self.mean_ebv1s[curr_row],self.mean_T2s[curr_row],self.mean_ebv2s[curr_row],valid_filters_this_row,curr_row)
        print("\nchi2 of mean parameters: ", mean_chi2,"\n")
        abc.plot(valid_avgwv_this_row,hotmodels,color="red")
        abc.plot(valid_avgwv_this_row,coolmodels,color="blue")
        sumofmodels = [hotmodels[i] + coolmodels[i] for i in range(len(hotmodels))]
        abc.plot(valid_avgwv_this_row,sumofmodels,color="limegreen")

        if self.plotscale == 1:
            pass
        elif self.plotscale == 0:
            abc.set_xscale('log')
            abc.set_yscale('log')
            abc.set_xticks([150,171,199,276,337,476,833,1097,1522])
            abc.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

        if self.saveplots == 1:
            saveimgname = self.imgfilename.replace("X","{}".format(self.rows[curr_row]+2))
            fig.savefig('{}'.format(saveimgname), bbox_inches='tight', dpi=150)

        canvas = FigureCanvasTkAgg(fig, master=topw)
        canvas.get_tk_widget().pack(anchor=tk.E)
        canvas.draw()

        label1 = tk.Label(topw,text="Average wavelength of each filter (x):")
        label1.place(x=50,y=20)
        textbox1 = tk.Text(topw,height=6,width=30)
        for filtername,avgwv in zip(valid_actualfilters_this_row,valid_avgwv_this_row):
            textbox1.insert(tk.END,"{}      {}\n".format(filtername,avgwv))
        textbox1.place(x=50,y=50)
        label2 = tk.Label(topw,text="Bandfluxes (y, orange):")
        label2.place(x=50,y=195)
        textbox2 = tk.Text(topw,height=6,width=30)
        for filtername,bf in zip(valid_actualfilters_this_row,valid_fluxes_this_row):
            textbox2.insert(tk.END,"{}      {}\n".format(filtername,format(bf,'.8e')))
        textbox2.place(x=50,y=225)
        label3 = tk.Label(topw,text="Bandflux errors:")
        label3.place(x=50,y=370)
        textbox3 = tk.Text(topw,height=6,width=30)
        for filtername,bfe in zip(valid_actualfilters_this_row,valid_errors_this_row):
            textbox3.insert(tk.END,"{}      {}\n".format(filtername,format(bfe,'.8e')))
        textbox3.place(x=50,y=400)
        label4 = tk.Label(topw,text="Hot star model fluxes (y, red):")
        label4.place(x=50,y=545)
        textbox4 = tk.Text(topw,height=6,width=30)
        self.mean_hotfluxes.append(0)
        for filtername,hotmod in zip(valid_actualfilters_this_row,hotmodels):
            self.mean_hotfluxes[curr_row] += hotmod
            textbox4.insert(tk.END,"{}      {}\n".format(filtername,format(hotmod,'.8e')))
        print("total hot model flux using weighted mean parameters: {}".format(self.mean_hotfluxes[curr_row]))
        textbox4.place(x=50,y=575)
        label5 = tk.Label(topw,text="Cool star model fluxes (y, blue):")
        label5.place(x=50,y=720)
        textbox5 = tk.Text(topw,height=6,width=30)
        self.mean_coolfluxes.append(0)
        for filtername,coolmod in zip(valid_actualfilters_this_row,coolmodels):
            self.mean_coolfluxes[curr_row] += coolmod
            textbox5.insert(tk.END,"{}      {}\n".format(filtername,format(coolmod,'.8e')))
        print("total cool model flux using weighted mean parameters: {}".format(self.mean_coolfluxes[curr_row]))
        textbox5.place(x=50,y=750)
        groove = tk.Canvas(topw,width=215,height=120,bd=4,relief=tk.RIDGE)
        groove.place(x=405,y=655)
        label5 = tk.Label(topw,text="chi^2 value using \nweighted mean parameters")
        label5.place(x=425,y=665)
        label5a = tk.Label(topw,text="{}".format(format(mean_chi2,'.6e')),font=("Arial",12))
        label5a.place(x=445,y=725)
        ridge = tk.Canvas(topw,width=600,height=300,bd=4,relief=tk.GROOVE)
        ridge.place(x=875,y=630)
        self.mean_chi2s.append(0)
        self.mean_chi2s[curr_row] = mean_chi2
        #label6 = tk.Label(topw,text="Best fit parameters",pady=15)
        #label6.place(x=865,y=725)
        labelheader = tk.Label(topw,text="Parameter                        Weighted mean             Error_lower             Error_upper",bd=4,relief=tk.GROOVE,padx=40,bg="azure")
        labelheader.place(x=878,y=603) 
        import math
        log_g_hot_sticker1 = format(self.mean_g1s[curr_row],'.6e')
        label7 = tk.Label(topw,text="log_g_hot                  =     {}".format(log_g_hot_sticker1))
        label7.place(x=910,y=648)

        temp_hot_sticker1 = format(self.mean_T1s[curr_row]*10000,'.6e')   
        label8= tk.Label(topw,text = "temperature_hot       =     {}".format(temp_hot_sticker1))
        label8.place(x=910,y=678)

        abundance_hot_sticker1 = format(self.mean_Z1s[curr_row],'.6e')
        label9 = tk.Label(topw, text = "abundance_hot         =      {}".format(abundance_hot_sticker1))
        label9.place(x=910,y=708)

        theta_r_hot_sticker1 = format(self.mean_theta_r1s[curr_row]*1e-12,'.6e')
        try:
            theta_r_hot_sticker2 = format(self.errorsallrows[curr_row][0][0],'.6e')
        except:
            theta_r_hot_sticker2 = "       N/A       "
        try:
            theta_r_hot_sticker3 = format(self.errorsallrows[curr_row][0][1],'.6e')
        except:
            theta_r_hot_sticker3 = "       N/A       "
        label10 = tk.Label(topw,text="theta_r_hot                =      {}        ({})        ({})".format(theta_r_hot_sticker1,theta_r_hot_sticker2,theta_r_hot_sticker3))
        label10.place(x=910,y=738)

        ebv_hot_sticker1 = format(self.mean_ebv1s[curr_row],'.6e')
        label11 = tk.Label(topw,text="E(b-v)_hot                 =      {}".format(ebv_hot_sticker1))
        label11.place(x=910,y=768)

        temp_cool_sticker1 = format(self.mean_T2s[curr_row]*10000,'.6e')
        label12 = tk.Label(topw,text="temperature_cool     =      {}".format(temp_cool_sticker1))
        label12.place(x=910,y=798)

        theta_r_cool_sticker1 = format(self.mean_theta_r2s[curr_row]*1e-12,'.6e')
        try:
            theta_r_cool_sticker2 = format(self.errorsallrows[curr_row][1][0],'.6e')
        except:
            theta_r_cool_sticker2 = "       N/A       "
        try:
            theta_r_cool_sticker3 = format(self.errorsallrows[curr_row][1][1],'.6e')
        except:
            theta_r_cool_sticker3 = "       N/A       "
        label13 = tk.Label(topw,text="theta_r_cool              =      {}        ({})        ({})".format(theta_r_cool_sticker1,theta_r_cool_sticker2,theta_r_cool_sticker3))
        label13.place(x=910,y=828)

        ebv_cool_sticker1 = format(self.mean_ebv2s[curr_row],'.6e')
        label14 = tk.Label(topw,text="E(b-v)_cool               =      {}".format(ebv_cool_sticker1))
        label14.place(x=910,y=858)

        def closethesource():
            topw.destroy()
        byebyebutt = tk.Button(topw, bd=3, font="Arial 10", text="Next source",command=closethesource,padx=30,pady=5)
        byebyebutt.place(x=423,y=830)
        topw.mainloop()

    ##


go = ChiSquared()