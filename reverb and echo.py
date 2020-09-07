import numpy
from scipy.io import wavfile
import plotly.graph_objs.scatter as go
import plotly
import os
# Line comments are prefaced with a #

def graph(x, y, title):
    plotly.offline.plot({
        "data": [go.Line(x=x, y=y)],
        "layout": go.Layout(title=title)
    }, auto_open=True)


# delete previous output
os.system("del Output.wav")

# load in the .wav file;
# Data is the array of values,
# fs is the sample rate
fs, data = wavfile.read("173.wav")

xs = []
ys = []
samples = 2048
for e in range(0, len(data)):
    if e < 2048:
        xs.append(e)#data[e][0])
        ys.append(data[e][1])
    else:
        break

print(xs)
print(ys)
graph(xs, ys, "sound")


#perform operations on the data
print("horse")

# write it as output
#wavfile.write("Output.wav", fs, data)