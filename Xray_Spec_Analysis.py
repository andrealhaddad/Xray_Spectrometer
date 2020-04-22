import numpy as np
import matplotlib.pyplot as plt

class Xray_Process:

    """
    Xray_Process
    Process the spectrometer image from Scienta soft xray spectrometer.
    The spectrometer could be in 2 different modes
    Mode 1: Using Scienta camera
    Mode 2: Using PCO.edge 5.5 camera (cropped)
    
    Values such as Pass Energy and Central Energy could be inserted/later on loaded from setup file...
    
    Correction Matrices from SPECS should accessible to load
    
    Choice between peak finding and fvb (after correction) is available
    
    """
    
    def __init__(self,Image, Grating = 300, Order = 0, Angle = 0, Slit_Angle = 0,  Process_Method = "FVB", Cam_boundaries = None):
        
        self.Image = Image
        self.Grating = Grating ##grating lines/mm
        self.Cam_boundaries = ([0,0],[0,0],[0,0],[0,0]) #list of tuples of x,y locations of boundaries
        self.Process_Method = Process_Method
        self.Order = Order
        self.Angle = Angle
        self.Slit_Angle = Slit_Angle

        self.Corr_Image = None
        self.Spectrum = None
        self.Energy_Axis = None ## In eV not lambda
        self.Peaks = None
        self.Energy_Axis == None

    def __calculate_Energy_Calibration(self):
        #use central energy and pass with operation mode to calculate Energy axis
        ## reference for slitless mode
        # https://aip.scitation.org/doi/pdf/10.1063/1.4772685
        # Scienta reference https://aip.scitation.org/doi/pdf/10.1063/1.1140929
        #calculations from https://onlinelibrary.wiley.com/doi/pdf/10.1002/cyto.a.20242
        #Estimate if orders will be overlapped! give a warning
        self.Energy_Axis = []
        
    def __Image_Correction(self):
        ## Check correction matrices of from SPECS
        ## CV2 warp image.
        #
        Corr_Image = []
        self.Corr_Image = Corr_Image

    def __peak_finding(self):
        ## refer to peak finding ...
        Peaks = []
        if self.Corr_Image == None:
            self.__Image_Correction()
        self.Peaks = Peaks

    def __calculate_Spectrum(self):

        if self.Corr_Image == None:
            self.__Image_Correction()
        if self.Energy_Axis == None:
            self.__calculate_Energy_Calibration()

        if self.Process_Method == "FVB":
            #threshold image Corrected image
            #
            self.spectrum = np.sum(self.Corr_Image, 1)

        elif self.Process_Method == "PF":
            ##Do peak finding and return (x,y, Int,wx,wy) of each peak.
            #set method for peak finding
            peak_location_list = self.__peak_finding()
            self.Hits = peak_location_list
            self.spectrum = [] ### bin hits

    ##Set variables
    def Set_Energies(self,Ene_Axis):
        self.Energy_Axis = Ene_Axis
    
    ##Get Variables
    def get_Caibrated_Spectrum(self):
        self.__calculate_Spectrum()
        return self.Spectrum
    
    def get_Energies_Axis(self):
        if self.Energy_Axis == None:
            self.__calculate_Energy_Calibration()
        return self.Energy_Axis
    
    def get_Corrected_Image(self):
        if self.Corr_Image == None:
            self.__Image_Correction()
        return self.Corr_Image

    def get_Peaks(self):
        if self.Peaks == None:
            self.__peak_finding()
        return self.Peaks

    def reset_values(self):
        self.Corr_Image = None
        self.Spectrum = None
        self.Energy_Axis = None
        self.Peaks = None
        self.Energy_Axis == None