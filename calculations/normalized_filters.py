class NormalizedFilters():
    def __init__(self):
        self.read_from_csv()
        self.area_under_filter()
        self.filter_overlaps_with_fits()
        self.get_nans()
        self.interpolated_values_for_fits()
        self.normalize_yinterp()
        self.normalize_yinterp2()

    def read_from_csv(self):
        import pandas as pd
        import numpy as np
        self.xdata = pd.DataFrame()
        self.ydata = pd.DataFrame()
        self.filternamelist = ["f110w","F169M","F172M","N219M","N279N","f275w","f336w","f475w","f814w","F148W","f160w"]
        dflist=[]
        for i in range(11):
            dflist.append(pd.read_csv("11filters/{}.csv".format(self.filternamelist[i]),skiprows=5,delimiter=","))
        self.xdata = self.xdata.assign(f110w_wavelength=dflist[0].iloc[:,0],F169M_wavelength=dflist[1].iloc[:,0],F172M_wavelength=dflist[2].iloc[:,0],N219M_wavelength=dflist[3].iloc[:,0],N279N_wavelength=dflist[4].iloc[:,0],f275w_wavelength=dflist[5].iloc[:,0],f336w_wavelength=dflist[6].iloc[:,0],f475w_wavelength=dflist[7].iloc[:,0],f814w_wavelength=dflist[8].iloc[:,0],F148W_wavelength=dflist[9].iloc[:,0],f160w_wavelength=dflist[10].iloc[:,0])
        self.ydata = self.ydata.assign(f110w_throughput=dflist[0].iloc[:,1],F169M_eff_area=dflist[1].iloc[:,1],F172M_eff_area=dflist[2].iloc[:,1],N219M_eff_area=dflist[3].iloc[:,1],N279N_eff_area=dflist[4].iloc[:,1],f275w_throughput=dflist[5].iloc[:,1],f336w_throughput=dflist[6].iloc[:,1],f475w_throughput=dflist[7].iloc[:,1],f814w_throughput=dflist[8].iloc[:,1],F148W_eff_area=dflist[9].iloc[:,1],f160w_throughput=dflist[10].iloc[:,1])
        self.xdata = self.xdata[["F148W_wavelength","F169M_wavelength","F172M_wavelength","N219M_wavelength","N279N_wavelength","f275w_wavelength","f336w_wavelength","f475w_wavelength","f814w_wavelength","f110w_wavelength","f160w_wavelength"]]
        self.ydata = self.ydata[["F148W_eff_area","F169M_eff_area","F172M_eff_area","N219M_eff_area","N279N_eff_area","f275w_throughput","f336w_throughput","f475w_throughput","f814w_throughput","f110w_throughput","f160w_throughput"]]
        pd.set_option('display.max_rows', None)
        #print(self.xdata) #correct
        #print(self.ydata) #correct

    def area_under_filter(self):
        import pandas as pd
        import numpy as np
        xcont = pd.DataFrame()
        xcont = xcont.assign(F148Wcontwave = np.linspace(self.xdata.iat[0,0],self.xdata.iat[self.xdata.iloc[:,0].last_valid_index(),0],1000))
        xcont = xcont.assign(F169Mcontwave = np.linspace(self.xdata.iat[0,1],self.xdata.iat[self.xdata.iloc[:,1].last_valid_index(),1],1000))
        xcont = xcont.assign(F172Mcontwave = np.linspace(self.xdata.iat[0,2],self.xdata.iat[self.xdata.iloc[:,2].last_valid_index(),2],1000))
        xcont = xcont.assign(N219Mcontwave = np.linspace(self.xdata.iat[0,3],self.xdata.iat[self.xdata.iloc[:,3].last_valid_index(),3],1000))
        xcont = xcont.assign(N279Ncontwave = np.linspace(self.xdata.iat[0,4],self.xdata.iat[self.xdata.iloc[:,4].last_valid_index(),4],1000))
        xcont = xcont.assign(f275wcontwave = np.linspace(self.xdata.iat[0,5],self.xdata.iat[self.xdata.iloc[:,5].last_valid_index(),5],1000))
        xcont = xcont.assign(f336wcontwave = np.linspace(self.xdata.iat[0,6],self.xdata.iat[self.xdata.iloc[:,6].last_valid_index(),6],1000))
        xcont = xcont.assign(f475wcontwave = np.linspace(self.xdata.iat[0,7],self.xdata.iat[self.xdata.iloc[:,7].last_valid_index(),7],1000))
        xcont = xcont.assign(f814wcontwave = np.linspace(self.xdata.iat[0,8],self.xdata.iat[self.xdata.iloc[:,8].last_valid_index(),8],1000))
        xcont = xcont.assign(f110wcontwave = np.linspace(self.xdata.iat[0,9],self.xdata.iat[self.xdata.iloc[:,9].last_valid_index(),9],1000))
        xcont = xcont.assign(f160wcontwave = np.linspace(self.xdata.iat[0,10],self.xdata.iat[self.xdata.iloc[:,10].last_valid_index(),10],1000)) 
        #print(xcont) #correct    

        self.yinterp = pd.DataFrame()
        self.yinterp = self.yinterp.assign(F148Winterp = np.interp(xcont.loc[:,"F148Wcontwave"],self.xdata.loc[:,"F148W_wavelength"],self.ydata.loc[:,"F148W_eff_area"]))
        self.yinterp = self.yinterp.assign(F169Minterp = np.interp(xcont.loc[:,"F169Mcontwave"],self.xdata.loc[:,"F169M_wavelength"],self.ydata.loc[:,"F169M_eff_area"]))
        self.yinterp = self.yinterp.assign(F172Minterp = np.interp(xcont.loc[:,"F172Mcontwave"],self.xdata.loc[:,"F172M_wavelength"],self.ydata.loc[:,"F172M_eff_area"]))
        self.yinterp = self.yinterp.assign(N219Minterp = np.interp(xcont.loc[:,"N219Mcontwave"],self.xdata.loc[:,"N219M_wavelength"],self.ydata.loc[:,"N219M_eff_area"]))
        self.yinterp = self.yinterp.assign(N279Ninterp = np.interp(xcont.loc[:,"N279Ncontwave"],self.xdata.loc[:,"N279N_wavelength"],self.ydata.loc[:,"N279N_eff_area"]))
        self.yinterp = self.yinterp.assign(f275winterp = np.interp(xcont.loc[:,"f275wcontwave"],self.xdata.loc[:,"f275w_wavelength"],self.ydata.loc[:,"f275w_throughput"]))
        self.yinterp = self.yinterp.assign(f336winterp = np.interp(xcont.loc[:,"f336wcontwave"],self.xdata.loc[:,"f336w_wavelength"],self.ydata.loc[:,"f336w_throughput"]))
        self.yinterp = self.yinterp.assign(f475winterp = np.interp(xcont.loc[:,"f475wcontwave"],self.xdata.loc[:,"f475w_wavelength"],self.ydata.loc[:,"f475w_throughput"]))
        self.yinterp = self.yinterp.assign(f814winterp = np.interp(xcont.loc[:,"f814wcontwave"],self.xdata.loc[:,"f814w_wavelength"],self.ydata.loc[:,"f814w_throughput"]))
        self.yinterp = self.yinterp.assign(f110winterp = np.interp(xcont.loc[:,"f110wcontwave"],self.xdata.loc[:,"f110w_wavelength"],self.ydata.loc[:,"f110w_throughput"]))
        self.yinterp = self.yinterp.assign(f160winterp = np.interp(xcont.loc[:,"f160wcontwave"],self.xdata.loc[:,"f160w_wavelength"],self.ydata.loc[:,"f160w_throughput"]))     
        #print(self.yinterp) #correct

        self.area = []
        from scipy import integrate
        for col in range(11):
            self.area.append(integrate.trapz(self.yinterp.iloc[:,col],xcont.iloc[:,col]))
        #print(self.area) #correct

    def filter_overlaps_with_fits(self):
        from astropy.io import fits
        import numpy as np
        with fits.open("fits_library/ckm05/ckm05_3500.fits") as hdul:
            indata_ang = hdul[1].data["WAVELENGTH"]
            indata_nm = np.array([round(i/10,4) for i in indata_ang])

        self.F148Wlist = []
        self.F169Mlist = []
        self.F172Mlist = []
        self.N219Mlist = []
        self.N279Nlist = []
        self.f275wlist = []
        self.f336wlist = []
        self.f475wlist = []
        self.f814wlist = []
        self.f110wlist = []
        self.f160wlist = []
        megalist = [self.F148Wlist,self.F169Mlist,self.F172Mlist,self.N219Mlist,self.N279Nlist,self.f275wlist,self.f336wlist,self.f475wlist,self.f814wlist,self.f110wlist,self.f160wlist]

        for col in range(11):
            for wv in indata_nm:
                if wv > self.xdata.iat[0,col] and wv < self.xdata.iat[self.xdata.iloc[:,col].last_valid_index(),col]:
                    megalist[col].append(wv)
        
        #for ent in megalist:
            #print(ent) #correct

    def get_nans(self):
        import numpy as np

        self.F148Wnans = []
        for n in range(len(self.f110wlist)-len(self.F148Wlist)):
            self.F148Wnans.append(np.nan) 
        self.F169Mnans = []
        for n in range(len(self.f110wlist)-len(self.F169Mlist)):
            self.F169Mnans.append(np.nan)
        self.F172Mnans = []
        for n in range(len(self.f110wlist)-len(self.F172Mlist)):
            self.F172Mnans.append(np.nan)
        self.N219Mnans = []
        for n in range(len(self.f110wlist)-len(self.N219Mlist)):
            self.N219Mnans.append(np.nan) 
        self.N279Nnans = []
        for n in range(len(self.f110wlist)-len(self.N279Nlist)):
            self.N279Nnans.append(np.nan) 
        self.f275wnans = []
        for n in range(len(self.f110wlist)-len(self.f275wlist)):
            self.f275wnans.append(np.nan) 
        self.f336wnans = []
        for n in range(len(self.f110wlist)-len(self.f336wlist)):
            self.f336wnans.append(np.nan) 
        self.f475wnans = []
        for n in range(len(self.f110wlist)-len(self.f475wlist)):
            self.f475wnans.append(np.nan) 
        self.f814wnans = []
        for n in range(len(self.f110wlist)-len(self.f814wlist)):
            self.f814wnans.append(np.nan) 
        self.f160wnans = []
        for n in range(len(self.f110wlist)-len(self.f160wlist)):
            self.f160wnans.append(np.nan) 

    def interpolated_values_for_fits(self):
        import pandas as pd
        import numpy as np
        self.yinterp2 = pd.DataFrame()
        self.yinterp2 = self.yinterp2.assign(F148Winterp2 = np.append(np.interp(self.F148Wlist,self.xdata.loc[:,"F148W_wavelength"],self.ydata.loc[:,"F148W_eff_area"]),self.F148Wnans))
        self.yinterp2 = self.yinterp2.assign(F169Minterp2 = np.append(np.interp(self.F169Mlist,self.xdata.loc[:,"F169M_wavelength"],self.ydata.loc[:,"F169M_eff_area"]),self.F169Mnans))
        self.yinterp2 = self.yinterp2.assign(F172Minterp2 = np.append(np.interp(self.F172Mlist,self.xdata.loc[:,"F172M_wavelength"],self.ydata.loc[:,"F172M_eff_area"]),self.F172Mnans))
        self.yinterp2 = self.yinterp2.assign(N219Minterp2 = np.append(np.interp(self.N219Mlist,self.xdata.loc[:,"N219M_wavelength"],self.ydata.loc[:,"N219M_eff_area"]),self.N219Mnans))
        self.yinterp2 = self.yinterp2.assign(N279Ninterp2 = np.append(np.interp(self.N279Nlist,self.xdata.loc[:,"N279N_wavelength"],self.ydata.loc[:,"N279N_eff_area"]),self.N279Nnans))
        self.yinterp2 = self.yinterp2.assign(f275winterp2 = np.append(np.interp(self.f275wlist,self.xdata.loc[:,"f275w_wavelength"],self.ydata.loc[:,"f275w_throughput"]),self.f275wnans))
        self.yinterp2 = self.yinterp2.assign(f336winterp2 = np.append(np.interp(self.f336wlist,self.xdata.loc[:,"f336w_wavelength"],self.ydata.loc[:,"f336w_throughput"]),self.f336wnans))
        self.yinterp2 = self.yinterp2.assign(f475winterp2 = np.append(np.interp(self.f475wlist,self.xdata.loc[:,"f475w_wavelength"],self.ydata.loc[:,"f475w_throughput"]),self.f475wnans))
        self.yinterp2 = self.yinterp2.assign(f814winterp2 = np.append(np.interp(self.f814wlist,self.xdata.loc[:,"f814w_wavelength"],self.ydata.loc[:,"f814w_throughput"]),self.f814wnans))
        self.yinterp2 = self.yinterp2.assign(f110winterp2 = np.interp(self.f110wlist,self.xdata.loc[:,"f110w_wavelength"],self.ydata.loc[:,"f110w_throughput"]))
        self.yinterp2 = self.yinterp2.assign(f160winterp2 = np.append(np.interp(self.f160wlist,self.xdata.loc[:,"f160w_wavelength"],self.ydata.loc[:,"f160w_throughput"]),self.f160wnans))
        #print(self.yinterp2) #correct

    def normalize_yinterp(self):
        ### GRAPHING PURPOSES ONLY ###
        import pandas as pd
        self.normalized = pd.DataFrame()
        self.normalized = self.normalized.assign(F148Wnormal = self.yinterp.loc[:,"F148Winterp"]/self.area[0])
        self.normalized = self.normalized.assign(F169Mnormal = self.yinterp.loc[:,"F169Minterp"]/self.area[1])
        self.normalized = self.normalized.assign(F172Mnormal = self.yinterp.loc[:,"F172Minterp"]/self.area[2])
        self.normalized = self.normalized.assign(N219Mnormal = self.yinterp.loc[:,"N219Minterp"]/self.area[3])
        self.normalized = self.normalized.assign(N279Nnormal = self.yinterp.loc[:,"N279Ninterp"]/self.area[4])
        self.normalized = self.normalized.assign(f275wnormal = self.yinterp.loc[:,"f275winterp"]/self.area[5])
        self.normalized = self.normalized.assign(f336wnormal = self.yinterp.loc[:,"f336winterp"]/self.area[6])
        self.normalized = self.normalized.assign(f475wnormal = self.yinterp.loc[:,"f475winterp"]/self.area[7])
        self.normalized = self.normalized.assign(f814wnormal = self.yinterp.loc[:,"f814winterp"]/self.area[8])
        self.normalized = self.normalized.assign(f110wnormal = self.yinterp.loc[:,"f110winterp"]/self.area[9])
        self.normalized = self.normalized.assign(f160wnormal = self.yinterp.loc[:,"f160winterp"]/self.area[10])
        #print(self.normalized)

    def normalize_yinterp2(self):
        import pandas as pd
        self.normalized2 = pd.DataFrame()
        self.normalized2 = self.normalized2.assign(F148Wnormal2 = self.yinterp2.loc[:,"F148Winterp2"]/self.area[0])
        self.normalized2 = self.normalized2.assign(F169Mnormal2 = self.yinterp2.loc[:,"F169Minterp2"]/self.area[1])
        self.normalized2 = self.normalized2.assign(F172Mnormal2 = self.yinterp2.loc[:,"F172Minterp2"]/self.area[2])
        self.normalized2 = self.normalized2.assign(N219Mnormal2 = self.yinterp2.loc[:,"N219Minterp2"]/self.area[3])
        self.normalized2 = self.normalized2.assign(N279Nnormal2 = self.yinterp2.loc[:,"N279Ninterp2"]/self.area[4])
        self.normalized2 = self.normalized2.assign(f275wnormal2 = self.yinterp2.loc[:,"f275winterp2"]/self.area[5])
        self.normalized2 = self.normalized2.assign(f336wnormal2 = self.yinterp2.loc[:,"f336winterp2"]/self.area[6])
        self.normalized2 = self.normalized2.assign(f475wnormal2 = self.yinterp2.loc[:,"f475winterp2"]/self.area[7])
        self.normalized2 = self.normalized2.assign(f814wnormal2 = self.yinterp2.loc[:,"f814winterp2"]/self.area[8])
        self.normalized2 = self.normalized2.assign(f110wnormal2 = self.yinterp2.loc[:,"f110winterp2"]/self.area[9])
        self.normalized2 = self.normalized2.assign(f160wnormal2 = self.yinterp2.loc[:,"f160winterp2"]/self.area[10])
        print(self.normalized2)