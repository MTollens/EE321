import numpy
# this import is the library used for file IO of .wav files
from scipy.io import wavfile
# this import is a graphing utility
import plotly.graph_objs as go
# allows me to delete the old output if needed
import os

import time

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


def Update(data, min=0, max=None, samples=True, verbose=False):
    # updates the values of x and y so they can be used to graph
    x = []
    y = []
    z = []
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
            x.append(e)
            y.append(data[e][0])
            z.append(data[e][1])
        else:
            break

    return x, y, z


def work(data, delay):
    # this is the function that does any of the actual work to the sound file
    zeros = numpy.zeros((len(data) + delay, 2))
    for x in range(0,len(data)):
        zeros[delay+x] = data[x]
    print("stop")
    return zeros


# attempt to delete previous output(s)
try:
    os.system("del Output.wav")
    os.system("del mid.wav")
except:
    print("could not delete output.wav for some reason")
    print("(it may not have existed)")


# load in the .wav file;
# Data is the array of values,
# fs is the sample rate
global_verbose = True
inputfile = "Welcome.wav"
fs, data = wavfile.read(inputfile)
# in order to edit the file, we need to make it a copy so that we can get edit privileges
data = data.copy()
delay = int(fs)

xs = [] # < this is the time value
ys = [] # < this is the left channel
zs = [] # < this is the right channel

xs, ys, zs = Update(data)
if global_verbose:
    graph(xs, ys, inputfile+"_Left")
    graph(xs, zs, inputfile+"_Right")


# pre operation waveform
print("phase 1 complete")


data = work(data, delay)

print("work complete")

xs, ys, zs = Update(data)
if global_verbose:
    graph(xs, ys, inputfile+"_modified_Right")
    graph(xs, zs, inputfile+"_modified_Left")

# write it as output
wavfile.write("Output.wav", fs, data)
print("end")