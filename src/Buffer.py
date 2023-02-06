
BUFFER_CAPACITY = 2

class Buffer(object):
    """
    This class implements the buffer behaviour
    """
    def __init__(self):
        self.no_of_components = 0

    def add_to_buffer(self):
        """
            Adds component to current buffer, returns True if successful, False if buffer is full
        """
        if (self.no_of_components >= BUFFER_CAPACITY):
            return False
        else:
            self.no_of_components += 1
            return True

    def remove_from_buffer(self):
        """
            Removes component from buffer, throws error if buffer is empty
        """
        if (self.no_of_components <= 0):
            return

        self.no_of_components -= 1


class Buffer_Manager(object):
    """
    This class managers the buffer operations
    """
    def __init__(self):
        
        self.buffer_dictionary = {}
        self.buffer_dictionary[("C1", "P1")] = Buffer()
        self.buffer_dictionary[("C1", "P2")] = Buffer()
        self.buffer_dictionary[("C1", "P3")] = Buffer()
        self.buffer_dictionary[("C2", "P2")] = Buffer()
        self.buffer_dictionary[("C3", "P3")] = Buffer()

    def attempt_to_add_to_buffer(self, component):
        """
            Function trys to find a buffer to place the component in
            returns (True, Product) if successfully added
            returns (False, None) if all buffers are full. 
        """

        if component == "C1":
            
            buffer_capacities = []
            buffer_capacities.append(self.buffer_dictionary[("C1", "P1")].no_of_components)
            buffer_capacities.append(self.buffer_dictionary[("C1", "P2")].no_of_components)
            buffer_capacities.append(self.buffer_dictionary[("C1", "P3")].no_of_components)

            # retrun if all buffers are full
            if sum(buffer_capacities) == BUFFER_CAPACITY * 3:
                return False, None

            buffer_choice = buffer_capacities.index(min(buffer_capacities))

            if buffer_choice == 0:
                return self.buffer_dictionary[("C1", "P1")].add_to_buffer(), "P1"

            elif buffer_choice == 1:
                return self.buffer_dictionary[("C1", "P2")].add_to_buffer(), "P2"

            elif buffer_choice == 2:
                return self.buffer_dictionary[("C1", "P3")].add_to_buffer(), "P3"

            raise ValueError("Check buffer manager, error while attempting to add component C1 to a buffer")

        elif component == "C2":
            add_success = self.buffer_dictionary[("C2", "P2")].add_to_buffer()
            return add_success,  "P2" if add_success else None

        elif component == "C3":
            add_success = self.buffer_dictionary[("C3", "P3")].add_to_buffer()
            return add_success,  "P3" if add_success else None

    def assemble_product(self, product):
        """
            Trys to remove components from the workstation and assembles product
            Returns True if the needed buffers were non empty and this was done successfully
            Returns False if there are missing components on the buffers
        """
        if product == "P1":
            if (self.buffer_dictionary[("C1", "P1")].no_of_components == 0):
                return False

            self.buffer_dictionary[("C1", "P1")].remove_from_buffer()

        elif product == "P2":
            if (self.buffer_dictionary[("C1", "P2")].no_of_components == 0 and self.buffer_dictionary[("C2", "P2")].no_of_components == 0):
                return False

            self.buffer_dictionary[("C1", "P2")].remove_from_buffer()
            self.buffer_dictionary[("C2", "P2")].remove_from_buffer()

        elif product == "P3":
            if (self.buffer_dictionary[("C1", "P3")].no_of_components == 0 and self.buffer_dictionary[("C3", "P3")].no_of_components == 0):
                return False

            self.buffer_dictionary[("C1", "P3")].remove_from_buffer()
            self.buffer_dictionary[("C3", "P3")].remove_from_buffer()

        return True
