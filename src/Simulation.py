import numpy as np
import queue
from Inspector import Inspector1, Inspector2
from Buffer import Component_Buffer_Manager
from Workstation import Workstation
import logging
from datetime import datetime

# Remove/Add "#" from "# or True" to feature flags for easier enable/disable
USER_CHOOSES_SEED = False  # or True
CREATE_LOG_FILES = False  # or True

TOTAL_PRODUCT_CREATION_LIMIT = 100



class Simulation(object):
    def __init__(self, logger):
        self._clock = 0
        self.simulation_logger = logger

        #Using a list instead of a queue because the order that events occur may not be chronological
        self.future_event_list = []

        # [Total, P1, P2, P3] - index matches product
        self.product_counts = [0, 0, 0, 0]

        # [None, I1, I2] so inspector number matches index
        self.inspectors = [None, Inspector1(), Inspector2()]

        # [None, W1, W2, W3] so workstation number match index
        self.workstations = [None, 
                              Workstation("P1"),
                              Workstation("P2"),
                              Workstation("P3")] 

        self._buffer_manager = Component_Buffer_Manager()


    def get_next_event(self):
        """
            Removes and returns the next nearest chronological event from the future event list 
        """
        if len(self.future_event_list) == 0:
            raise ValueError("Error trying to get next chronological event before any have been scheduled")
        
        # Identify the index of the earliest chronological event from the future event list
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
        #self.simulation_logger.info(str(self._clock) + " - Inspector " + str(inspector_number) + " has started inspection component: " + component + "\n")
        print (str(self._clock) + " - Inspector " + str(inspector_number) + " has started inspection component: " + component + "\n")

        #Schedule event for inspection completion
        completion_time = self._clock + inspect_time
        self.future_event_list.append((completion_time, "Inspection_Complete", component))



    def add_to_buffer(self, component):
        """
            Processes attempting to add an inspected component to a buffer
        """
        # If successful, the buffers will be updated accordingly by calling this
        success, work_station = self._buffer_manager.attempt_to_add_to_buffer(component)

        # Inspector is blocked and can't add to buffer right now
        if not success:
            return

        # Schedule event for adding to buffer
        #self.simulation_logger.info
        print (str(self._clock) + " - " + "The inspector has placed " + component + " in " + work_station + "'s buffer")
        self.future_event_list.append((self._clock, "Add_to_Buffer", work_station))



    def unbuffer_workstation(self, product):
        """
            Processes attempting to start assembling a product
        """
        success = self._buffer_manager.attempt_to_assemble_product(product)

        if not success:
            # Could not build the product. 1 or more missing items on workstation buffer
            # Will eventually be successful once buffers get occupied
            return
        
        workstation_assembly_time = self.workstations[int(product[1])].get_delay_time()
        # self.simulation_logger.info
        print(str(self._clock) + " - Workstation " + product + " has started building " + product)
        
        # Schedule event for completing assembly
        build_completion_time = self._clock + workstation_assembly_time
        self.future_event_list.append((build_completion_time, "Assembly_Complete", product))



    def process_product_made(self, product):
        """
            Processes the completeing the a specified product's assembly
        """
        self.product_counts[0] += 1  # Total product counter
        self.product_counts[int(product[1])] += 1  # Product specific counter
        #self.simulation_logger.info
        print (str(self._clock) + " - " + product + " has been completed")

        # Try to create another product
        self.future_event_list.append((self._clock, "Unbuffer_Start_Assembly", product))


# Main script
if __name__ == "__main__":

    # set seed for random number generator
    seed = 0
    if USER_CHOOSES_SEED:
        seed = input('Enter simulation seed:')
    np.random.seed((int(seed)))

    #   Logging Setup
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger()

#    fileHandler = logging.FileHandler("logs/{1}.log".format("logs", datetime.now().strftime("%d-%m-%Y")))
#    fileHandler.setFormatter(logFormatter)
#    fileHandler.setLevel("WARNING")
#    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)


    # Create simulation object
    sim = Simulation(logger)

    # Schedule first inspection completion for both inspectors I1 & I2
    sim.schedule_add_to_buffer(1)
    sim.schedule_add_to_buffer(2)

    while sim.product_counts[0] <= TOTAL_PRODUCT_CREATION_LIMIT:
        # Get next event
        # Event Tuple Structure ( time, event_type, Product||Component )
        evt = sim.get_next_event()

        # update clock
        sim._clock = evt[0]

        #Update event type discernation
        if evt[1] == "Inspection_Complete":
            sim.add_to_buffer(evt[2])
        elif evt[1] == "Add_to_Buffer" or evt[1] == "Unbuffer_Start_Assembly":
            sim.unbuffer_workstation(evt[2])
        elif evt[1] == "Assembly_Complete":
            sim.process_product_made(evt[2])