import random
from utillities import expo_inverse_cdf


NUMBER_OF_SAMPLES = 300

class Inspector1(object):
    """
        This Class is used to simulate the Inspector1 behaviour
    """
    
    def __init__(self, rand_generator):
        """
            intilazation of the Inspector1 class 
        """

        self.rand_generator = rand_generator
        
    def generate_inspect_time(self):
        """
            Creates a inspection time delay from the distribution returns delay time and component 
        """
        # Lambda = 1 / sample_mean
        time = expo_inverse_cdf(self.rand_generator.get_next_r(), 0.096544573)       
        return (time, "C1")




class Inspector2(object):
    """
        This Class is used to simulate the Inspector2 behaviour
    """
    
    def __init__(self, rand_generator):
        """
            intilazation of the Inspector1 class 
        """

        self.rand_generator = rand_generator
    



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

        # Lambda = 1 / sample_mean
        if component == "C2":
            time = expo_inverse_cdf(self.rand_generator.get_next_r(), 0.06436289)
        else: 
            time = expo_inverse_cdf(self.rand_generator.get_next_r(), 0.048466621)
        
        return (time, component)