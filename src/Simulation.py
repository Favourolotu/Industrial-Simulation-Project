from Inspector import Inspector1, Inspector2
from Buffer import Buffer_Manager
from Workstation import Workstation
import time
from Multiplicative_Congruential_Model import Multiplicative_Congruential_Model as mcm
import random


MAX_PRODUCTION_NUMBER = 50000



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
        print (str(self.timer) + " - Inspector " + str(inspector_number) + " has started inspection component: " + component + "\n")

        
        completion_time = self.timer + inspect_time
        self.future_event_list.append((completion_time, "Inspection_Complete", component))



    def add_to_buffer(self, component):
        """
            Processes attempting to add an inspected component to a buffer
        """
        success, work_station = self.buffer_manager.attempt_to_add_to_buffer(component)

        # Inspector is blocked and can't add to buffer
        if not success:
            # Inspector is blocked and can't add to buffer right now
            # Set the current time as the most recent block time
            self.component_most_recent_block_time[int(component[1])] = self.timer
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
            
            # Component 2 or 3 get's buffered, resume Inspector 2
            self.buffer_manager.attempt_to_add_to_buffer("C2" if product=="P2" else "C3")

            # Track the blocked time
            blocked_time = self.timer - self.component_most_recent_block_time[int(product[1])]
            self.component_total_block_time[int(product[1])] += blocked_time
            # Reset the most recent block time to unblocked
            self.component_most_recent_block_time[int(product[1])] = 0

            # Start inspector 2 next inspection
            self.future_event_list.append((self.timer, "Start_Next_Inspection", 2))

        # Check if inspector 1 is waiting for a buffer spot 
        if self.component_most_recent_block_time[1] != -1:
            
            # Resume inspector 1
            self.buffer_manager.attempt_to_add_to_buffer("C1")
            
            # Track the blocked time
            blocked_time = self.timer - self.component_most_recent_block_time[1]
            self.component_total_block_time[1] += blocked_time
            # Reset the most recent block time to unblocked
            self.component_most_recent_block_time[1] = -1

            # Start the next inspection
            self.future_event_list.append((self.timer, "Start_Next_Inspection", 1 ))

        #waiting_time = self.timer - self.workstation_most_recent_wait_for_component_time[product.value]
        #self.workstation_total_wait_for_component_time[int(product[1])] += waiting_time

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
        # self.workstation_most_recent_wait_for_component_time[int(product[1])] = self.timer



# Main script
if __name__ == "__main__":

    for i in range(632):

        seed = random.randint(20, 23232323)

        start = time.time()
        print("Simulation in progress, started at "+ str(start))
        print("Number of products to make before stopping : " + str(MAX_PRODUCTION_NUMBER))
        print()
        
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

        end = time.time()
        print ("Simulation took: " + str(end-start) + " seconds")
        print ("products produced => " + str(sim.product_counts))
        print("Blocked times: C1 => {0} C2 => {1} C3 => {2}".format(sim.component_total_block_time[1], sim.component_total_block_time[2], sim.component_total_block_time[3]))
        # print(str(sim.workstation_total_wait_for_component_time[1]))

