class FluxGui():
    def __init__(self):
        self.buildgui()
    
    def buildgui(self):
        import tkinter as tk
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        mwin = tk.Tk()
        mwin.geometry("1150x900+500+20")
        mwin.configure(bg="gray95")
        mwin.title("5-D integral plotter")

        def findranges():
            from tkinter import messagebox
            generalexcept = True

            try:
                if gravchecked.get() == 1:
                    user_grav1 = float(gravselect1.get())
                    user_grav2 = float(gravselect2.get())
                    if user_grav1 > user_grav2:
                        tk.messagebox.showinfo('Error', 'Gravity values must be from smaller to larger')
                        generalexcept = False
                        steg
                if tempchecked.get() == 1:
                    user_temp1 = float(tempselect1.get())
                    user_temp2 = float(tempselect2.get())
                    if user_temp1 > user_temp2:
                        tk.messagebox.showinfo('Error', 'Temperature values must be from smaller to larger')
                        generalexcept = False
                        o
                if metalchecked.get() == 1:
                    user_metal1 = float(metalselect1.get())
                    user_metal2 = float(metalselect2.get())
                    if user_metal1 > user_metal2:
                        tk.messagebox.showinfo('Error', 'Abundance values must be from smaller to larger')
                        generalexcept = False
                        saur
                if filterchecked.get() == 1:
                    user_filter1 = filterselect1.get()
                    user_filter2 = filterselect2.get()
                    
                    if user_filter1 == "F148W":
                        user_filter1 = 0
                    elif user_filter1 == "F169M":
                        user_filter1 = 1
                    elif user_filter1 == "F172M":
                        user_filter1 = 2
                    elif user_filter1 == "N219M":
                        user_filter1 = 3
                    elif user_filter1 == "N279N":
                        user_filter1 = 4
                    elif user_filter1 == "f275w":
                        user_filter1 = 5
                    elif user_filter1 == "f336w":
                        user_filter1 = 6
                    elif user_filter1 == "f475w":
                        user_filter1 = 7
                    elif user_filter1 == "f814w":
                        user_filter1 = 8
                    elif user_filter1 == "f110w":
                        user_filter1 = 9
                    elif user_filter1 == "f160w":
                        user_filter1 = 10

                    if user_filter2 == "F148W":
                        user_filter2 = 0
                    elif user_filter2 == "F169M":
                        user_filter2 = 1
                    elif user_filter2 == "F172M":
                        user_filter2 = 2
                    elif user_filter2 == "N219M":
                        user_filter2 = 3
                    elif user_filter2 == "N279N":
                        user_filter2 = 4
                    elif user_filter2 == "f275w":
                        user_filter2 = 5
                    elif user_filter2 == "f336w":
                        user_filter2 = 6
                    elif user_filter2 == "f475w":
                        user_filter2 = 7
                    elif user_filter2 == "f814w":
                        user_filter2 = 8
                    elif user_filter2 == "f110w":
                        user_filter2 = 9
                    elif user_filter2 == "f160w":
                        user_filter2 = 10
                    
                    if user_filter1 > user_filter2:
                        tk.messagebox.showinfo('Error', 'Filters must be in order from smaller wavelength to larger')
                        generalexcept = False
                        us

            except:
                if generalexcept == True:
                    tk.messagebox.showinfo('Error', 'Please select values from the boxes')
                else:
                    pass

            else:
                if gravchecked.get() == 0 and tempchecked.get() == 0 and metalchecked.get() == 0 and filterchecked.get() == 0:
                    print("You have to enter something!")
                else:
                    if gravchecked.get() == 1:
                        self.grav1 = user_grav1
                        self.grav2 = user_grav2
                    if tempchecked.get() == 1:    
                        self.temp1 = user_temp1
                        self.temp2 = user_temp2
                    if metalchecked.get() == 1:
                        self.metal1 = user_metal1
                        self.metal2 = user_metal2
                    if filterchecked.get() == 1:
                        self.filter1 = user_filter1
                        self.filter2 = user_filter2
                    mwin.quit()
       
        def grayoutgrav():
            if gravtext1['state'] == tk.NORMAL:
                gravtext1['state'] = tk.DISABLED
                gravbutton1['state'] = tk.DISABLED
                gravtext2['state'] = tk.DISABLED
                gravbutton2['state'] = tk.DISABLED
            elif gravtext1['state'] == tk.DISABLED:
                gravtext1['state'] = tk.NORMAL
                gravbutton1['state'] = tk.NORMAL
                gravtext2['state'] = tk.NORMAL
                gravbutton2['state'] = tk.NORMAL          
        gravchecked = tk.IntVar()
        gravcheckbox = tk.Checkbutton(mwin,variable=gravchecked,command = grayoutgrav)
        gravcheckbox.place(x=100,y=120)
        gravcheckbox.select()
        def pasteonlabelgrav1():
            try:
                gravselect1.set(gravtext1.selection_get())
            except:
                pass
        gravlabel1 = tk.Label(mwin,text = "Plot log of surface gravity from").place(x=150,y=120)
        gravtextframe1 = tk.Frame()
        gravtextframe1.place(x=400,y=50)
        gravscrollbar1 = tk.Scrollbar(gravtextframe1)
        gravscrollbar1.pack(side=tk.RIGHT,fill=tk.Y)
        gravtext1 = tk.Listbox(gravtextframe1,state=tk.NORMAL,bd=5,height=8,width=10,yscrollcommand=gravscrollbar1.set)
        gravtext1.pack()
        gravscrollbar1.configure(command=gravtext1.yview)
        gravlist = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
        for grav in gravlist:
            gravtext1.insert(tk.END,"{}".format(grav))
        gravbutton1 = tk.Button(mwin,text="select",bg="white",state=tk.NORMAL,command=pasteonlabelgrav1,padx=15)
        gravbutton1.place(x=520,y=70)
        gravselect1 = tk.StringVar()
        gravselectlabel1 = tk.Label(mwin,textvariable=gravselect1,font=("Arial",14),padx=20)
        gravselectlabel1.place(x=520,y=120)

        def pasteonlabelgrav2():
            try:
                gravselect2.set(gravtext2.selection_get())
            except:
                pass
        gravlabel2 = tk.Label(mwin,text = "to").place(x=650,y=120)
        gravtextframe2 = tk.Frame()
        gravtextframe2.place(x=700,y=50)
        gravscrollbar2 = tk.Scrollbar(gravtextframe2)
        gravscrollbar2.pack(side=tk.RIGHT,fill=tk.Y)
        gravtext2 = tk.Listbox(gravtextframe2,state=tk.NORMAL,bd=5,height=8,width=10,yscrollcommand=gravscrollbar2.set)
        gravtext2.pack()
        gravscrollbar2.configure(command=gravtext2.yview)
        gravlist = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
        for grav in gravlist:
            gravtext2.insert(tk.END,"{}".format(grav))
        gravbutton2 = tk.Button(mwin,state=tk.NORMAL,text="select",bg="white",command=pasteonlabelgrav2,padx=15)
        gravbutton2.place(x=820,y=70)
        gravselect2 = tk.StringVar()
        gravselectlabel2 = tk.Label(mwin,textvariable=gravselect2,font=("Arial",14),padx=20)
        gravselectlabel2.place(x=820,y=120)


        def grayouttemp():
            if temptext1['state'] == tk.NORMAL:
                temptext1['state'] = tk.DISABLED
                tempbutton1['state'] = tk.DISABLED
                temptext2['state'] = tk.DISABLED
                tempbutton2['state'] = tk.DISABLED
            elif temptext1['state'] == tk.DISABLED:
                temptext1['state'] = tk.NORMAL
                tempbutton1['state'] = tk.NORMAL
                temptext2['state'] = tk.NORMAL
                tempbutton2['state'] = tk.NORMAL
        tempchecked = tk.IntVar()
        tempcheckbox = tk.Checkbutton(mwin,variable=tempchecked,command=grayouttemp)
        tempcheckbox.place(x=100,y=320)
        tempcheckbox.select()
        def pasteonlabeltemp1():
            try:
                tempselect1.set(temptext1.selection_get())
            except:
                pass
        templabel1 = tk.Label(mwin,text = "Plot temperature from").place(x=150,y=320)
        temptextframe1 = tk.Frame()
        temptextframe1.place(x=400,y=250)
        tempscrollbar1 = tk.Scrollbar(temptextframe1)
        tempscrollbar1.pack(side=tk.RIGHT,fill=tk.Y)
        temptext1 = tk.Listbox(temptextframe1,state=tk.NORMAL,bd=5,height=8,width=10,yscrollcommand=tempscrollbar1.set)
        temptext1.pack()
        tempscrollbar1.configure(command=temptext1.yview)
        templist = [3500,3750,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500,6750,7000,7250,7500,7750,8000,8250,8500,8750,9000,9250,9500,9750,10000,10250,10500,10750,11000,11250,11500,11750,12000,12250,12500,12750,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000,24000,25000,26000,27000,28000,29000,30000,31000,32000,33000,34000,35000,36000,37000,38000,39000,40000,41000,42000,43000,44000,45000,46000,47000,48000,49000,50000]
        for temp in templist:
            temptext1.insert(tk.END,"{}".format(temp))
        tempbutton1 = tk.Button(mwin,state=tk.NORMAL,text="select",bg="white",command=pasteonlabeltemp1,padx=15)
        tempbutton1.place(x=520,y=270)
        tempselect1 = tk.StringVar()
        tempselectlabel1 = tk.Label(mwin,textvariable=tempselect1,font=("Arial",14),padx=20)
        tempselectlabel1.place(x=520,y=320)

        def pasteonlabeltemp2():
            try:
                tempselect2.set(temptext2.selection_get())
            except:
                pass
        templabel2 = tk.Label(mwin,text = "to").place(x=650,y=320)
        temptextframe2 = tk.Frame()
        temptextframe2.place(x=700,y=250)
        tempscrollbar2 = tk.Scrollbar(temptextframe2)
        tempscrollbar2.pack(side=tk.RIGHT,fill=tk.Y)
        temptext2 = tk.Listbox(temptextframe2,state=tk.NORMAL,bd=5,height=8,width=10,yscrollcommand=tempscrollbar2.set)
        temptext2.pack()
        tempscrollbar2.configure(command=temptext2.yview)
        templist = [3500,3750,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500,6750,7000,7250,7500,7750,8000,8250,8500,8750,9000,9250,9500,9750,10000,10250,10500,10750,11000,11250,11500,11750,12000,12250,12500,12750,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000,24000,25000,26000,27000,28000,29000,30000,31000,32000,33000,34000,35000,36000,37000,38000,39000,40000,41000,42000,43000,44000,45000,46000,47000,48000,49000,50000]
        for temp in templist:
            temptext2.insert(tk.END,"{}".format(temp))
        tempbutton2 = tk.Button(mwin,state=tk.NORMAL,text="select",bg="white",command=pasteonlabeltemp2,padx=15)
        tempbutton2.place(x=820,y=270)
        tempselect2 = tk.StringVar()
        tempselectlabel2 = tk.Label(mwin,textvariable=tempselect2,font=("Arial",14),padx=20)
        tempselectlabel2.place(x=820,y=320)


        def grayoutmetal():
            if metaltext1['state'] == tk.NORMAL:
                metaltext1['state'] = tk.DISABLED
                metalbutton1['state'] = tk.DISABLED
                metaltext2['state'] = tk.DISABLED
                metalbutton2['state'] = tk.DISABLED
            elif metaltext1['state'] == tk.DISABLED:
                metaltext1['state'] = tk.NORMAL
                metalbutton1['state'] = tk.NORMAL
                metaltext2['state'] = tk.NORMAL
                metalbutton2['state'] = tk.NORMAL
        metalchecked = tk.IntVar()
        metalcheckbox = tk.Checkbutton(mwin,variable=metalchecked,command=grayoutmetal)
        metalcheckbox.place(x=100,y=520)
        metalcheckbox.select()
        def pasteonlabelmetal1():
            try:
                metalselect1.set(metaltext1.selection_get())
            except:
                pass
        metallabel1 = tk.Label(mwin,text = "Plot metality from").place(x=150,y=520)
        metaltextframe1 = tk.Frame()
        metaltextframe1.place(x=400,y=450)
        metalscrollbar1 = tk.Scrollbar(metaltextframe1)
        metalscrollbar1.pack(side=tk.RIGHT,fill=tk.Y)
        metaltext1 = tk.Listbox(metaltextframe1,state=tk.NORMAL,bd=5,height=8,width=10,yscrollcommand=metalscrollbar1.set)
        metaltext1.pack()
        metalscrollbar1.configure(command=metaltext1.yview)
        metallist = [-2.5,-2.0,-1.5,-1.0,-0.5,0,0.2,0.5]
        for metal in metallist:
            metaltext1.insert(tk.END,"{}".format(metal))
        metalbutton1 = tk.Button(mwin,state=tk.NORMAL,text="select",bg="white",command=pasteonlabelmetal1,padx=15)
        metalbutton1.place(x=520,y=470)
        metalselect1 = tk.StringVar()
        metalselectlabel1 = tk.Label(mwin,textvariable=metalselect1,font=("Arial",14),padx=20)
        metalselectlabel1.place(x=520,y=520)

        def pasteonlabelmetal2():
            try:
                metalselect2.set(metaltext2.selection_get())
            except:
                pass
        metallabel2 = tk.Label(mwin,text = "to").place(x=650,y=520)
        metaltextframe2 = tk.Frame()
        metaltextframe2.place(x=700,y=450)
        metalscrollbar2 = tk.Scrollbar(metaltextframe2)
        metalscrollbar2.pack(side=tk.RIGHT,fill=tk.Y)
        metaltext2 = tk.Listbox(metaltextframe2,state=tk.NORMAL,bd=5,height=8,width=10,yscrollcommand=metalscrollbar2.set)
        metaltext2.pack()
        metalscrollbar2.configure(command=metaltext2.yview)
        metallist = [-2.5,-2.0,-1.5,-1.0,-0.5,0,0.2,0.5]
        for metal in metallist:
            metaltext2.insert(tk.END,"{}".format(metal))
        metalbutton2 = tk.Button(mwin,state=tk.NORMAL,text="select",bg="white",command=pasteonlabelmetal2,padx=15)
        metalbutton2.place(x=820,y=470)
        metalselect2 = tk.StringVar()
        metalselectlabel2 = tk.Label(mwin,textvariable=metalselect2,font=("Arial",14),padx=20)
        metalselectlabel2.place(x=820,y=520)
        
        def grayoutfilter():
            if filtertext1['state'] == tk.NORMAL:
                filtertext1['state'] = tk.DISABLED
                filterbutton1['state'] = tk.DISABLED
                filtertext2['state'] = tk.DISABLED
                filterbutton2['state'] = tk.DISABLED
            elif filtertext1['state'] == tk.DISABLED:
                filtertext1['state'] = tk.NORMAL
                filterbutton1['state'] = tk.NORMAL
                filtertext2['state'] = tk.NORMAL
                filterbutton2['state'] = tk.NORMAL
        filterchecked = tk.IntVar()
        filtercheckbox = tk.Checkbutton(mwin,variable=filterchecked,command=grayoutfilter)
        filtercheckbox.place(x=100,y=720)
        filtercheckbox.select()        
        def pasteonlabelfilter1():
            try:
                filterselect1.set(filtertext1.selection_get())
            except:
                pass
        filterlabel1 = tk.Label(mwin,text = "Plot filters from").place(x=150,y=720)
        filtertextframe1 = tk.Frame()
        filtertextframe1.place(x=400,y=650)
        filterscrollbar1 = tk.Scrollbar(filtertextframe1)
        filterscrollbar1.pack(side=tk.RIGHT,fill=tk.Y)
        filtertext1 = tk.Listbox(filtertextframe1,state=tk.NORMAL,bd=5,height=8,width=10,yscrollcommand=filterscrollbar1.set)
        filtertext1.pack()
        filterscrollbar1.configure(command=filtertext1.yview)
        filterlist = ["F148W","F169M","F172M","N219M","N279N","f275w","f336w","f475w","f814w","f110w","f160w"]
        for filter in filterlist:
            filtertext1.insert(tk.END,"{}".format(filter))
        filterbutton1 = tk.Button(mwin,state=tk.NORMAL,text="select",bg="white",command=pasteonlabelfilter1,padx=15)
        filterbutton1.place(x=520,y=670)
        filterselect1 = tk.StringVar()
        filterselectlabel1 = tk.Label(mwin,textvariable=filterselect1,font=("Arial",14),padx=20)
        filterselectlabel1.place(x=520,y=720)

        def pasteonlabelfilter2():
            try:
                filterselect2.set(filtertext2.selection_get())
            except:
                pass
        filterlabel2 = tk.Label(mwin,text = "to").place(x=650,y=720)
        filtertextframe2 = tk.Frame()
        filtertextframe2.place(x=700,y=650)
        filterscrollbar2 = tk.Scrollbar(filtertextframe2)
        filterscrollbar2.pack(side=tk.RIGHT,fill=tk.Y)
        filtertext2 = tk.Listbox(filtertextframe2,state=tk.NORMAL,bd=5,height=8,width=10,yscrollcommand=filterscrollbar2.set)
        filtertext2.pack()
        filterscrollbar2.configure(command=filtertext2.yview)
        filterlist = ["F148W","F169M","F172M","N219M","N279N","f275w","f336w","f475w","f814w","f110w","f160w"]
        for filter in filterlist:
            filtertext2.insert(tk.END,"{}".format(filter))
        filterbutton2 = tk.Button(mwin,state=tk.NORMAL,text="select",bg="white",command=pasteonlabelfilter2,padx=15)
        filterbutton2.place(x=820,y=670)
        filterselect2 = tk.StringVar()
        filterselectlabel2 = tk.Label(mwin,textvariable=filterselect2,font=("Arial",14),padx=20)
        filterselectlabel2.place(x=820,y=720)

        gobutton = tk.Button(mwin,text="Plot",font=("Arial",14),command=findranges,padx=20,pady=10)
        gobutton.place(x=1000,y=400)

        mwin.mainloop()
