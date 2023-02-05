import numpy as np
import queue
from Inspector import Inspector1, Inspector2
from Buffer import Buffer_Manager
from Workstation import Workstation
from datetime import datetime


MAX_PRODUCTION_NUMBER = 100



class Simulation(object):
    """
    This class ecompasses the behavoiur of the simulation
    """
    def __init__(self):
        self.timer = 0

        #Keep track of future events
        self.future_event_list = []

        self.product_counts = {'Total': 0,'P1': 0,'P2': 0,'P3': 0}

        self.inspectors = {1: Inspector1(), 2: Inspector2()}

        self.workstations = { "P1": Workstation("P1"),
                              "P2": Workstation("P2"),
                              "P3": Workstation("P3")} 

        self.buffer_manager = Buffer_Manager()


    def get_next_event(self):
        """
            Removes and returns the next nearest event from the future event list 
        """
        if len(self.future_event_list) == 0:
            raise ValueError("Error trying to get next chronological event before any have been scheduled")
        
        current_min = self.future_event_list[0][0]
        current_min_index = 0

        for i in range(len(self.future_event_list)):
            if self.future_event_list[i][0] < current_min:
                current_min = self.future_event_list[i][0]
                current_min_index = i

        # Remove and return the event at that index
        return self.future_event_list.pop(current_min_index)



    def schedule_add_to_buffer(self, inspector_number: int):
        """
            Initiates an inspector's inspection process and schedules 
            the attempt to add the component to the buffer
        """
        inspect_time, component = self.inspectors[inspector_number].generate_inspect_time()
        print (str(self.timer) + " - Inspector " + str(inspector_number) + " has started inspection component: " + component + "\n")

        completion_time = self.timer + inspect_time
        self.future_event_list.append((completion_time, "Inspection_Complete", component))



    def add_to_buffer(self, component):
        """
            Processes attempting to add an inspected component to a buffer
        """
        # If successful, the buffers will be updated accordingly by calling this
        success, work_station = self.buffer_manager.attempt_to_add_to_buffer(component)

        # Inspector is blocked and can't add to buffer right now
        if not success:
            return

        # Schedule event for adding to buffer
        print (str(self.timer) + " - " + "The inspector has placed " + component + " in " + work_station + "'s buffer")
        self.future_event_list.append((self.timer, "Start_Next_Inspection", 1 if component== "C1" else 2))
        self.future_event_list.append((self.timer, "Add_to_Buffer", work_station))



    def unbuffer_workstation(self, product):
        """
            Processes attempting to start assembling a product
        """
        success = self.buffer_manager.assemble_product(product)

        if not success:
            return
        
        workstation_assembly_time = self.workstations[product].get_delay_time()
        print(str(self.timer) + " - Workstation " + product + " has started building " + product)
        
        # Schedule event for completing assembly
        build_completion_time = self.timer + workstation_assembly_time
        self.future_event_list.append((build_completion_time, "Assembly_Complete", product))



    def process_product_made(self, product):
        """
            Processes the completeing the a specified product's assembly
        """
        self.product_counts['Total'] += 1  
        self.product_counts[product] += 1  
        print (str(self.timer) + " - " + product + " has been completed")

        # Try to create another product
        self.future_event_list.append((self.timer, "Unbuffer_Start_Assembly", product))


# Main script
if __name__ == "__main__":

    # set seed for random number generator
    seed = 0
    np.random.seed((int(seed)))


    sim = Simulation()

    # Schedule first inspection completion for both inspectors I1 & I2
    sim.schedule_add_to_buffer(1)
    sim.schedule_add_to_buffer(2)

    while sim.product_counts['Total'] <= MAX_PRODUCTION_NUMBER:
        # Get next event
        # Event Tuple Structure ( time, event_type, Product||Component )
        evt = sim.get_next_event()

        # update timer
        sim.timer = evt[0]

        # Handle events
        if evt[1] == "Inspection_Complete":
            sim.add_to_buffer(evt[2])
        elif evt[1] == "Add_to_Buffer" or evt[1] == "Unbuffer_Start_Assembly":
            sim.unbuffer_workstation(evt[2])
        elif evt[1] == "Assembly_Complete":
            sim.process_product_made(evt[2])
        elif evt[1] == "Start_Next_Inspection":
            sim.schedule_add_to_buffer(evt[2])