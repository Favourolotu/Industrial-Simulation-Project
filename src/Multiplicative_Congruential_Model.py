import time
import math

class Multiplicative_Congruential_Model(object):
    """       
        Based on linear multiplicative congruential model with a zero incrementor

    """
    def __init__(self, seed:int):
        """
            Constructor for Multiplicative_Congruential_Model class
        """
        self.current = seed if seed!=0 else 1
        self.a = 41040
        self.m = 23636842147
    
    def get_next_x(self):
        """
            Returns the next pseudorandom integer
        """
        next = (self.a * self.current) % self.m
        self.current = next
        return next
    
    def get_next_r(self) -> float:
        """
            Returns the next pseudorandom number from a uniform distribution between 0 and 1
        """
        generated_x = self.get_next_x()
        if generated_x==0:
            return 23636842146 / 23636842147
        else:
            return generated_x / 23636842147
    

def autocorrelation_test():
    """
        Conducts an autocorrelation test on MCM genrator
    """
    
    print("Starting Autocorrelation test...")

    #Setup constants and variables
    clean_n = 900
    clean_i = 1
    lag_m = 1 # from brightspace
    z_table_value = 1.96 # corresponds to alpha=0.05 divided by 2
    big_M = (clean_n-clean_i)//lag_m - 1

    generator = Multiplicative_Congruential_Model(round(time.time()))

    print("Big M: "+ str(big_M))

    #Create an n sized list of randomly generated numbers
    random_variable_list = []
    for j in range(clean_n):
        random_variable_list.append(generator.get_next_r())
    
    #Autocorrelation procedure
    sum_of_subsequent_products = 0
    previous_r = random_variable_list[clean_i]
    for j in range(clean_i+lag_m, big_M+1):
        sum_of_subsequent_products += random_variable_list[j] * previous_r
        previous_r = random_variable_list[j]

    p_im = (1/(big_M+1))*sum_of_subsequent_products - 0.25
    sigma_im = math.sqrt(13*big_M+7) / (12*(big_M+1))
    generated_z = (p_im/sigma_im)
    if generated_z < z_table_value :
        print("Null Hypothesis is NOT rejected")
        print("Autocorrelation test passed with M="+str(big_M)+" and Z="+str(generated_z)+"\n")
    else:
        print("Null Hypothesis is REJECTED")
        print("Autocorrelation test failed with M="+str(big_M)+" and Z="+str(generated_z)+"\n")

def kolmogorov_smirnov_test():
    """
        Conducts a Kolmogorov-Smirnov test on MCM genrator
    """
    print("Starting Kolmogorov-Smirnov test...")
    D_table = 1.36/math.sqrt(150)

    # Generate a list of 150 random numbers and the list of expected uniform cdf's
    generator = Multiplicative_Congruential_Model(round(time.time()))
    list_of_randoms = []
    expected_cdf = []
    for i in range(150):
        expected_cdf.append((i+1)/150)
        list_of_randoms.append(generator.get_next_r()) 

    # Sort the list
    list_of_randoms.sort()

    #Instantiate the D lists with first elements (D_minus first element unique procedure)
    D_plus = [expected_cdf[0]-list_of_randoms[0]]
    D_minus = [list_of_randoms[0]]

    for i in range(1,150):
        D_plus.append(expected_cdf[i]-list_of_randoms[i])
        D_minus.append(list_of_randoms[i]-expected_cdf[i-1])
    print("Max D_plus value: " + str(max(D_plus)))
    print("Max D_minus value: " + str(max(D_minus)))
    print("D_table value to beat: " + str(D_table))
    
    if max(max(D_plus),max(D_plus)) < D_table:
        print("Null Hypothesis is NOT rejected")
        print("Kolmogorov-Smirnov test passed\n\n")
    else:
        print("Null Hypothesis is REJECTED")
        print("Kolmogorov-Smirnov test FAILED\n\n")

    # for elem in list_of_randoms:
    #    print(elem)

if __name__ == '__main__':
    autocorrelation_test()
    kolmogorov_smirnov_test()
