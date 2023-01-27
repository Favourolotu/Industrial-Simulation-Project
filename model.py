import numpy

FILE_NAMES = ["ws1.dat", "ws2.dat", "ws3.dat", "servinsp1.dat", "servinsp22.dat", "servinsp23.dat"]

full_content = {}

exponential_mean = {}

NUMBER_OF_SAMPLES = 300

debug = False

for filename in FILE_NAMES:

    content = []
    for i in open(filename).readlines():
        i.strip().split()
    
        converted = -1
        try:
            converted = float(i)
        except:
            if debug:
                print ("Empty Space Found!")

        if converted != -1:
            content.append(float(i))
        
    full_content[filename] = content

for elem in full_content:
    elem_mean = sum(full_content[elem]) / NUMBER_OF_SAMPLES

    # Generate random number and convert it to seconds
    exponential_mean[elem] = numpy.random.exponential(elem_mean, 1)[0]*60
    
print (exponential_mean)    