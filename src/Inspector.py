import numpy
import random

    

    
NUMBER_OF_SAMPLES = 300

class Inspector1(object):
    """
        This Class is used to simulate the Inspector1 behaviour
    """
    
    def __init__(self):
        """
            intilazation of the Inspector1 class 
        """

        self.mean= self.generate_mean_from_data()

    
    def generate_mean_from_data(self):
        """
            Returns the Mean for component 1 from the data set
        """
       
        file_path = "data_files\servinsp1.dat"

        content = []
        
        for i in open(file_path).readlines():
            i.strip().split()
            
            converted = -1

            try:
                converted = float(i)
            except:
                print ("Empty Space Found!")

            if converted != -1:
                content.append(float(i))

        return sum(content) / NUMBER_OF_SAMPLES
    
    def generate_inspect_time(self):
        """
            Creates a inspection time delay from the distribution returns delay time and component 
        """
        #Generate the random time delay from the mean and change to seconds
        time = numpy.random.exponential(self.mean, 1)[0] * 60
        return (time, "C1")




class Inspector2(object):
    """
        This Class is used to simulate the Inspector2 behaviour
    """
    
    def __init__(self):
        """
            intilazation of the Inspector2 class 
        """
        #stubing mean implementation due to file accessing errors
        self.C2_mean = self.generate_mean_from_data("C2")
        self.C3_mean = self.generate_mean_from_data("C3")
    

    def generate_mean_from_data(self, component):
        """
            returns the Mean for the given component from the distribution
        """
        

        if component == "C2":
            file_path = "data_files\servinsp22.dat"
        else:
            file_path = "data_files\servinsp23.dat"
        
        
        content = []
        
        for i in open(file_path).readlines():
            i.strip().split()
            
            converted = -1

            try:
                converted = float(i)
            except:
                print ("Empty Space Found!")

            if converted != -1:
                content.append(float(i))

        return sum(content) / NUMBER_OF_SAMPLES


    def generate_inspect_time(self):
        """
            Creates a inspection time delay from the distribution 
            returns the delay time and the component 
        """

        # Randomly select the component to generate inpect time for 
        if random.getrandbits(1) == 1:
            component = "C2"
        else:
            component = "C3"


        if component == "C2":
            # convert randomly generated delay in minutes to seconds
            time = numpy.random.exponential(self.C2_mean, 1)[0] * 60
        else: 
            time = numpy.random.exponential(self.C3_mean, 1)[0] * 60
        
        return (time, component)