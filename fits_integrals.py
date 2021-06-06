class FitsIntegrals():
    def __init__(self):
        pass
    
    def grav_out_str(self,grav_in):
        return "g" + str(grav_in).replace(".", "")
    
    def temp_out_str(self,temp_in):
        return str(int(temp_in))

    def metal_out_str(self,metal_in):
        if metal_in == 0:
            return "p00"
        elif str(metal_in).find("-") != -1:
            return str(metal_in).replace(".", "").replace("-", "m")
        else:
            return "p"+str(metal_in).replace(".", "")

    def cycle_through_fits(self):
        from astropy.io import fits
        import numpy as np
        from calculations.normalized_filters import NormalizedFilters
        nf = NormalizedFilters()
        self.allmetallist =[-2.5,-2.0,-1.5,-1.0,-0.5,0,0.2,0.5]
        self.alltemplist=[3500,3750,4000,4250,4500,4750,5000,5250,5500,5750,6000,6250,6500,6750,7000,7250,7500,7750,8000,8250,8500,8750,9000,9250,9500,9750,10000,10250,10500,10750,11000,11250,11500,11750,12000,12250,12500,12750,13000,14000,15000,16000,17000,18000,19000,20000,21000,22000,23000,24000,25000,26000,27000,28000,29000,30000,31000,32000,33000,34000,35000,36000,37000,38000,39000,40000,41000,42000,43000,44000,45000,46000,47000,48000,49000,50000]
        self.allgravlist = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0]
        self.allfilterlist = ["F148W","F169M","F172M","N219M","N279N","f275w","f336w","f475w","f814w","f110w","f160w"]
        self.allfilterlistno = [0,1,2,3,4,5,6,7,8,9,10]
        self.integralarray = np.zeros((8,76,11,11))
        metal_ind = 0
        for metal in self.allmetallist:
            #print("start new metal: {}, {}".format(metal_ind,metal))
            temp_ind = 0
            for temp in self.alltemplist:
                #print("start new temp: {}, {}".format(temp_ind,temp))
                grav_ind = 0
                for grav in self.allgravlist:
                    #print("start new grav: {}, {}".format(grav_ind,grav))
                    filter_ind = 0
                    with fits.open("fits_library/ck{}/ck{}_{}.fits".format(self.metal_out_str(metal), self.metal_out_str(metal), self.temp_out_str(temp))) as hdul:
                        F_lambda_spectrum = hdul[1].data["{}".format(self.grav_out_str(grav))]
                        indata_ang = hdul[1].data["WAVELENGTH"]
                        fdict = {"F148Wnormal2":nf.F148Wlist,"F169Mnormal2":nf.F169Mlist,"F172Mnormal2":nf.F172Mlist,"N219Mnormal2":nf.N219Mlist,"N279Nnormal2":nf.N279Nlist,"f275wnormal2":nf.f275wlist,"f336wnormal2":nf.f336wlist,"f475wnormal2":nf.f475wlist,"f814wnormal2":nf.f814wlist,"f110wnormal2":nf.f110wlist,"f160wnormal2":nf.f160wlist}
                        for key in fdict:
                            #print("start new filter: {}, {}".format(filter_ind,key))
                            prodfunc = []
                            for i,lam in enumerate(fdict[key]):
                                #print("start new lambda: {}, {}".format(i,lam))
                                #print("Things going into prodfunc; Rsp: {}, F_lambda: {} (flux at index {})".format(nf.normalized2.at[i,key],F_lambda_spectrum[np.where(indata_ang == lam*10)],np.where(indata_ang == lam*10)))
                                prodfunc.append(nf.normalized2.at[i,key]*F_lambda_spectrum[np.where(indata_ang == lam*10)])
                            areaelements = []
                            for i,lam in enumerate(fdict[key]):
                                if fdict[key][i] != fdict[key][-1]:  
                                        areaelements.append((prodfunc[i]+prodfunc[i+1])/2*(fdict[key][i+1]-fdict[key][i]))
                            self.integralarray[metal_ind,temp_ind,grav_ind,filter_ind]=(sum(areaelements))
                            filter_ind+=1
                            print("metal,temp,grav,filter =",metal_ind,temp_ind,grav_ind,filter_ind)
                    grav_ind+=1
                temp_ind+=1
            metal_ind+=1
    
    def x_array(self):
        print("made it to x_array")
        import xarray as xr
        self.labelled_integral_array = xr.DataArray(self.integralarray, coords=[("Abundance", self.allmetallist), ("Temperature", self.alltemplist), ("Log_of_surface_gravity",self.allgravlist), ("Filter",self.allfilterlistno)])
        print(self.labelled_integral_array)
        self.labelled_integral_array.to_netcdf("saved_on_disk.nc")


fi = FitsIntegrals()

fi.cycle_through_fits()

fi.x_array()