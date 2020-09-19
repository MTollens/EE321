import numpy
# this import is the library used for file IO of .wav files
from scipy.io import wavfile
# this import is a graphing utility
try:
    import plotly.graph_objs as go
except:
    global_verbose = False
    print("graphing utility not present")
    print("please install 'plotly'")
    print("py -m pip install plotly")
    print("on windows")
    print("or ")
    print("python3 -m pip install plotly")
    print("on linux")

# allows me to delete the old output if needed
import os
# used for optional command line useage
import sys

# function arguments such as title="Title" are optional variables for the function
# they are given a default value if not supplied with a value
def graph(x, y, title="Title", xaxis=None, yaxis=None):
    # graphing function
    # function borrowed and modified from: https://stackoverflow.com/a/62314178
    try:
        trace = go.Scatter(x=x, y=y)
        if not xaxis:
            xaxis = {'title': 'X Axis'}
        else:
            xaxis = {'title': xaxis}
        if not yaxis:
            yaxis = {'title': 'Y Axis'}
        else:
            yaxis = {'title': yaxis}

        my_layout = {
            'title': str(title),
            'title_x': 0.5,
            'xaxis': xaxis,
            'yaxis': yaxis,
        }
        fig = go.Figure(data=trace, layout=my_layout)
        fig.show()
    except Exception as e:
        print("graph of '{}' failed".format(title))
        print("Unable to graph due to:")
        print(e)


def Update(data, min=0, max=None, samples=True, verbose=False, channels=2):

    # updates the values of x and y so they can be used to graph
    x = []
    y = []
    if not max:
        max = len(data)
    if samples == True:
        samples = max + 64
    for e in range(min, max):
        if verbose:
            # enables and disables terminal output
            if e % 500 == 0:
                print("up to " + str(e))
        if e < samples:
            # the channels argument is used because the original file has two channels, we focus on only one channel for
            # simplicity because it it gets the important parts across, and we dont need twice as many output graphs
            if channels == 2:
                x.append(e)
                y.append(data[e][0])
            else:
                x.append(e)
                y.append(data[e])
        else:
            break

    return x, y


def Delay(data, delay):
    print("delay of {} samples added".format(delay))
    # this is the function that does any of the actual work to the sound file
    zeros = [0]*(len(data) + delay)
    for x in range(0,len(data)):
        zeros[delay+x] = data[x]
    print("Delay Added")
    return zeros

# Echo repeats a signal with a delay and applies a gain to each repition of the sigal
# Echo is used for both echoing and reverb: echo delay>fs, reverb delay<fs
# Echo has three inputs: data, delay, and n
# data is the input signal
# delay is the number of samples between each copied signal
# n is the number of times the signal is copied (defaulted to 3)
def Echo(data, delay, n=3):
    # waveforms is a 2d array that holds teh data and teh copies of data
    waveforms = [[0]*(len(data)+(n*delay))]*n
    # output holds the final new waveform
    output = [0]*(len(data)+(n*delay))
    #gain is the coefficient multiplied to each succesive signal
    gain = .25

    #for loop copies data n times, and applies each respective delay
    for x in range(0,n):
        for y in range(0,len(data)):
            waveforms[x][(x*delay)+y] += data[y]

    # for loop combines the waveforms and applies gain
    for x in range(0,n):
        for y in range(0,len(data)):
            #summation is the sum of all teh copies at one point in time
            summation = 0
            #divisor is how many waveforms overlap
            divisor = 0

            #for loop checks each waveform at one point and time
            for z in range(0, n):
                # if a signal exists on a particular waveform at this poin and time
                # increment divisor (indicatin how many waves overlap at this point in time)
                if abs(waveforms[z][y]) > 10:
                    divisor += 1
                # sum all the wave forms at this point in time
                summation += waveforms[z][y]
            # if no signal is found set devisor to 1 to avoid div by 0
            if divisor == 0:
                divisor = 1
            # use the summation and divisor to average the signal at this point in time
            # apply gain to this signal
            output[(x*delay)+y] += round(((gain**x)*summation)/divisor)
    print("Echo, Echo")
    return output



def numpy_to_regular(ndarray):
    # takes in a numpy array and makes it a standard python list, for easier useage
    assert isinstance(ndarray, numpy.ndarray), "this is not the correct type of input for Np_to_regular"
    result = ndarray.tolist()
    return result


def right_channel_only(Sound_list):
    # removes the left channel
    result = [0] * len(Sound_list)
    for x in range(0, len(Sound_list)):
        result[x] = Sound_list[x][0]
    return result


def regular_to_numpy(array):
    assert isinstance(array, list), "not a list"
    # takes in a regular python list and returns a numpy ndarray to be saved as a file.wav
    result = numpy.asarray(array)
    #result = numpy.ndarray([len(array),2])
    #for x in range(0, len(result)):
    #     result[x] = [int(round(array[x])), int(round(array[x]))]
    return result




# global verbose is used for graphical output. plotly must be installed
global_verbose = True
mode = "echo"
# used later
value = 0
# load in the .wav file;
# Data is the array of values,
# fs is the sample rate
arguments = ['','','','','','']
for x in range(0, len(sys.argv)):
    print(sys.argv)
    arguments[x] = sys.argv[x]


if arguments[1]:
    if arguments[1] in ["man", "help", "h"]:
        print("Project 1 \n by Matthew Thompson and Andrew Sins")
        print("for EE321 Signals and Systems")
        print("Built in python version 3.7")
        print("to use:")
        print("py Project1.py [operation to perform] [time value for use in operation]")

    elif os.path.exists(str(arguments[1])):
        inputfile = arguments[1]
    else:
        print("the specified file could not be found")
else:
    inputfile = "Welcome.wav"

if arguments[2]:
    if arguments[2] in ["d", "delay"]:
        mode = "delay"
    elif sys.argv[2] in ["e", "echo"]:
        mode = 'echo'
    elif arguments[2] in ["r", "reverb"]:
        mode = 'reverb'
else:
    mode = 'reverb'

if arguments[3]:
    try:
        value = int(arguments[3])
    except:
        print("argument '{}' could not be understood as a value".format(arguments[3]))
        print("please use an integer value")



# fs is the sample rate of the audio
# data is a numpy ndarray of samples
fs, data = wavfile.read(inputfile)
# in order to edit the file, we need to make it a copy so that we can get edit privileges
data = data.copy()


# this line ensures that the main functionality of the program is only activated if this is the top level program
# otherwise the program does nothing, but it still provides the functions here for external use
if __name__ == "__main__":
    print("this program features command line arguments")
    print("use:")
    print("'py Project1.py help'")
    print("to get additional information about this program")

    # attempt to delete previous output(s)
    os.system("del Output.wav")

    xs = []  # < this is the time value
    ys = []  # < this is the left channel

    if global_verbose:
        xs, ys = Update(data)
        #displays sound file before anything is done to it so we can get a baseline
        graph(xs, ys, inputfile+"_Original")


    # pre operation waveform
    print("Content loaded")

    Clean_data = numpy_to_regular(data)
    clean = right_channel_only(Clean_data)

    mode = "reverb"
    if mode == "delay":
        # this is where the delay is added
        clean = Delay(clean, fs*6)
    elif mode == "echo":
        clean = Echo(clean, fs)
    elif mode == "reverb":
        clean = Echo(clean, int(.25*fs), 3)
    else:
        print("operation {} is not known".format(mode))

    result = regular_to_numpy(clean)
    result.dtype = numpy.int16


    print("Generating output")

    if global_verbose:
        xs, ys = Update(result, channels=1)
        # displays the waveform after we have done something to it so that we can see the change
        graph(xs, ys, inputfile+"_modified_{}".format(mode))

    # write it as output
    # the value of fs is doubled here because the result channel is half as long. so we need to sample twice as fast for it
    # to sound normal
    # this is because we removed the left channel for simplicity, it does not significantly change the audio but it saves
    # a lot of work for us and for the program
    wavfile.write("Output.wav", int(fs*2), result)
    print("Finished")

