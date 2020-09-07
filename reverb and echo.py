import numpy
# this import is the library used for file IO of .wav files
from scipy.io import wavfile
# this import is a graphing utility
import plotly.graph_objs as go
# this import will allow faster processing of larger files
from multiprocessing import process
# allows me to delete the old output if needed
import os

# function arguments such as title="Title" are optional variables for the function
# they are given a default value if not supplied with a value
def graph(x, y, title="Title", xaxis=None, yaxis=None):
    # graphing function
    # function borrowed and modified from: https://stackoverflow.com/a/62314178
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

# delete previous output
try:
    os.system("del Output.wav")
except:
    print("could not delete output.wav for some reason")
    print("(it may not have existed)")

# load in the .wav file;
# Data is the array of values,
# fs is the sample rate
inputfile = "173.wav"
fs, data = wavfile.read(inputfile)

xs = []
ys = []
samples = 10240
for e in range(0, len(data)):
    if e%500 == 0:
        print("up to " + str(e))
    if e < samples:
        xs.append(e) #data[e][0])
        ys.append(data[e][1])
    else:
        break

try:
    graph(xs, ys, inputfile)
except:
    print("failed to graph 1")

#perform operations on the data
print("phase 1 complete")


#for x in range(0,len(data)):


# write it as output
wavfile.write("Output.wav", fs, data)