import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class FluxData():
    def __init__(self):
        self.prepare_dataarray()
        self.plot()

    def prepare_dataarray(self):
        ds_disk = xr.open_dataset("saved_on_disk.nc")
        da = ds_disk.to_array()
        self.da = da.rename("Flux_integral")

    def plot(self):
        from calculations.plot_uninterp_gui import FluxGui
        fluxgui = FluxGui()
        dimendict = {}
        try:
            dimendict['gravlo']=fluxgui.grav1
            dimendict['gravhi']=fluxgui.grav2
        except:
            pass
        try:
            dimendict['templo']=fluxgui.temp1
            dimendict['temphi']=fluxgui.temp2
        except:
            pass
        try:
            dimendict['metallo'] = fluxgui.metal1
            dimendict['metalhi']=fluxgui.metal2
        except:
            pass
        try:
            dimendict['filtlo'] = fluxgui.filter1
            dimendict['filthi'] = fluxgui.filter2
        except:
            pass
        
        if len(dimendict) == 8:
            da4dfilter = self.da.loc['__xarray_dataarray_variable__', dimendict['metallo']:dimendict['metalhi'], dimendict['templo']:dimendict['temphi'], dimendict['gravlo']:dimendict['gravhi'], dimendict['filtlo']:dimendict['filthi']]
            priority = []

            if dimendict['filtlo'] == dimendict['filthi']:
                priority.append(None)
            else:
                priority.append("Filter")

            if dimendict['metallo'] == dimendict['metalhi']:
                priority.append(None)
            else:
                priority.append("Abundance")

            if dimendict['templo'] == dimendict['temphi']:
                priority.append(None)
            else:
                priority.append("Temperature")

            if dimendict['gravlo'] == dimendict['gravhi']:
                priority.append(None)
            else:
                priority.append("Log_of_surface_gravity")
            
            da4dfilter.plot(x=priority[3],y=priority[2],col=priority[1],row=priority[0])
            plt.show()


fluxdata = FluxData()