from Inspector import Inspector1, Inspector2
from Buffer import Buffer_Manager
from Workstation import Workstation
import time
from Multiplicative_Congruential_Model import Multiplicative_Congruential_Model as mcm
import random
import statistics


MAX_PRODUCTION_NUMBER = 50000
ALTERNATE_POLICY_IN_USE = True



class Simulation(object):
    """
    This class ecompasses the behavoiur of the simulation
    """
    def __init__(self, seed):
        self.timer = 0

        #Keep track of future events
        self.future_event_list = []

        self.product_counts = {'Total': 0,'P1': 0,'P2': 0,'P3': 0}
        rand_gen = mcm(seed)
        self.inspectors = {1: Inspector1(rand_gen), 2: Inspector2(rand_gen)}

        self.workstations = { "P1": Workstation("P1", rand_gen),
                              "P2": Workstation("P2", rand_gen),
                              "P3": Workstation("P3", rand_gen)} 

        self.buffer_manager = Buffer_Manager()

        self.component_most_recent_block_time = [None, -1, -1, -1]
        self.component_total_block_time = [None, 0,0,0]
        
        self.block_counter = {"C1": 0,
                              "C2":0,
                              "C3":0}

        self.last_inspected = None


    def get_next_event(self):
        """
            Removes and returns the next nearest event from the future event list 
        """
        if len(self.future_event_list) == 0:
            raise ValueError("Error trying to get next event")
        
        current_min = self.future_event_list[0][0]
        current_min_index = 0

        for i in range(len(self.future_event_list)):
            if self.future_event_list[i][0] < current_min:
                current_min = self.future_event_list[i][0]
                current_min_index = i

        return self.future_event_list.pop(current_min_index)



    def schedule_add_to_buffer(self, inspector_number: int):
        """
            Start the inspection process for inspector id 
        """
        inspect_time, component = self.inspectors[inspector_number].generate_inspect_time()
        self.last_inspected = component


        if ALTERNATE_POLICY_IN_USE and inspector_number == 2:
            inspect_time, component = self.inspectors[inspector_number].get_alternate_policy_inspect_time(self.last_inspected)
        
            
        print (str(self.timer) + " - Inspector " + str(inspector_number) + " has started inspection component: " + component + "\n")

        self.last_inspected = component
        completion_time = self.timer + inspect_time
        self.future_event_list.append((completion_time, "Inspection_Complete", component))



    def add_to_buffer(self, component):
        """
            add an inspected component to a buffer
        """
        success, work_station = self.buffer_manager.attempt_to_add_to_buffer(component)

        # Inspector is blocked and can't add to buffer
        if not success:
            self.component_most_recent_block_time[int(component[1])] = self.timer
            self.block_counter[component] += 1
            return

        # Schedule event for adding to buffer
        print (str(self.timer) + " - " + "The inspector has placed " + component + " in " + work_station + "'s buffer")
        
        self.future_event_list.append((self.timer, "Start_Next_Inspection", 1 if component== "C1" else 2))
        
        self.future_event_list.append((self.timer, "Add_to_Buffer", work_station))




    def unbuffer_workstation(self, product):
        """
            This function unbuffers a workstation and assembles product
        """
        if self.workstations[product].is_building():
            return


        success = self.buffer_manager.assemble_product(product)

        if not success:
            return
        

        # Check if inspector 2 is waiting for a buffer spot 
        if product!="P1" and self.component_most_recent_block_time[int(product[1])] != -1:
            
            # let inspector 2 try buffering again
            self.buffer_manager.attempt_to_add_to_buffer("C2" if product=="P2" else "C3")

            # Tracking the blocked times
            blocked_time = self.timer - self.component_most_recent_block_time[int(product[1])]
            self.component_total_block_time[int(product[1])] += blocked_time
            self.component_most_recent_block_time[int(product[1])] = 0

            # Start inspector 2 next inspection
            self.future_event_list.append((self.timer, "Start_Next_Inspection", 2))

        # Check if inspector 1 is waiting for to add to buffer 
        if self.component_most_recent_block_time[1] != -1:
            
            # let inspector 1 add to buffer
            self.buffer_manager.attempt_to_add_to_buffer("C1")
            
            # Tracking the blocked times for components
            blocked_time = self.timer - self.component_most_recent_block_time[1]
            self.component_total_block_time[1] += blocked_time
            self.component_most_recent_block_time[1] = -1

            # Start the next inspection
            self.future_event_list.append((self.timer, "Start_Next_Inspection", 1 ))


        workstation_assembly_time = self.workstations[product].get_delay_time()
        print(str(self.timer) + " - Workstation " + product + " has started building " + product)
        
        # Schedule event for completing assembly
        build_completion_time = self.timer + workstation_assembly_time
        
        self.future_event_list.append((build_completion_time, "Assembly_Complete", product))



    def product_assembled(self, product):
        """
            Processes the completeing the a specified product's assembly
        """
        self.product_counts['Total'] += 1  
        self.product_counts[product] += 1  
        print (str(self.timer) + " - " + product + " has been completed")

        self.workstations[product].complete_build()
        # Try to create another product
        self.future_event_list.append((self.timer, "Unbuffer_Start_Assembly", product))



# Main script
if __name__ == "__main__":
        
    start = time.time()
    print("Simulation in progress, started at "+ str(start))
    print("Number of products to make before stopping : " + str(MAX_PRODUCTION_NUMBER))
    sim_block_times_stats = {"C1":[],
                            "C2":[],
                            "C3":[]}
    for i in range(632):

        seed = random.randint(20, 23232323)

        
        
        sim = Simulation(seed)

        # Schedule first inspection completion for both inspectors 1 and 2
        sim.schedule_add_to_buffer(1)
        sim.schedule_add_to_buffer(2)

    
        while sim.product_counts['Total'] < MAX_PRODUCTION_NUMBER:
        
            # Event format ( time, event_type, Product||Component )
            event = sim.get_next_event()

            # update simulation timer
            sim.timer = event[0]

            # Handle events
            if event[1] == "Inspection_Complete":
                sim.add_to_buffer(event[2])
            elif event[1] == "Add_to_Buffer" or event[1] == "Unbuffer_Start_Assembly":
                sim.unbuffer_workstation(event[2])
            elif event[1] == "Assembly_Complete":
                sim.product_assembled(event[2])
            elif event[1] == "Start_Next_Inspection":
                sim.schedule_add_to_buffer(event[2])

        sim_block_times_stats["C1"].append(sim.component_total_block_time[1] / sim.block_counter["C1"])
        sim_block_times_stats["C2"].append(sim.component_total_block_time[2] / sim.block_counter["C2"])
        sim_block_times_stats["C3"].append(sim.component_total_block_time[3] / sim.block_counter["C3"])
    
   
    for key in sim_block_times_stats:
        print(key + " Average waiting time:")
        print("Mean: " + str(round(statistics.mean(sim_block_times_stats[key]), 2)))
        print("Standard deviation: " + str(round(statistics.stdev(sim_block_times_stats[key]), 2)))
        print("n: " + str(len(sim_block_times_stats[key])) +"\n")

    end = time.time()
    print ("Simulation took: " + str(end-start) + " seconds")

