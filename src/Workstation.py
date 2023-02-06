import numpy

NUMBER_OF_SAMPLES = 300

class Workstation(object):
    """
        This Class is used to simulate the work station behaviour
    """

    def __init__(self, product_type):
        """
            Ininital delclairation for the workstation class
        """
        self.mean = self.generate_mean_from_data(product_type)
        
        self.product_type = product_type

    def generate_mean_from_data(self, product_type):
        """
            returns the mean for the specified product time from the data set
        """
        if product_type == "P1":
            file_path = "data_files/ws1.dat"
        elif product_type == "P2":
            file_path = "data_files/ws2.dat"
        elif product_type == "P3":
            file_path = "data_files/ws3.dat"
        else:
            raise ValueError ("Illegel product provided")

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
    
    def get_delay_time(self):
        """
            Creates a inspection time delay from the distribution 
            returns the delay time
        """
        # convert randomly generated delay in minutes to seconds
        time = numpy.random.exponential(self.mean, 1)[0] * 60
        return time
    