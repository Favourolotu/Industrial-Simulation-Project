from utillities import expo_inverse_cdf

NUMBER_OF_SAMPLES = 300

class Workstation(object):
    """
        This Class is used to simulate the work station behaviour
    """

    def __init__(self, product_type, rand_gen):
        """
            Ininital delclairation for the workstation class
        """
        self.product_type = product_type
        self.rand_generator = rand_gen
        self.currently_building = False

    
    def get_delay_time(self):
        """
            Creates a inspection time delay from the distribution 
            returns the delay time
        """
        # Lambda = 1 / sample_mean
        if self.product_type == "P1":
            return expo_inverse_cdf(self.rand_generator.get_next_r(), 0.217182777)
        elif self.product_type == "P2":
            return expo_inverse_cdf(self.rand_generator.get_next_r(), 0.090150136)
        else: 
            return expo_inverse_cdf(self.rand_generator.get_next_r(), 0.113693469)
        

    def complete_build(self):
        self.currently_building = False

    def is_building(self):
        """
            Returns the self.currently_building field
        """
        return self.currently_building
  
    