"""
Grow by Index - Python Field
Author : Sheng Wen Cheng
"""

import c4d
import math
import random
from c4d.modules import mograph as mo

#-------------------------------------------------------------------------------------------------------------

# VALUE (float)
def SampleValue(op, transform, index, lastIndex):

    speed = 1.5       # Grow Speed (Unit : 1 / Second)
    random_val = (math.sin(index * 12.9898) * 43758.5453) % 1.0
    delay = 0.15 + (random_val * 0.1)  # ( Unit : Second )
    startFrame = 0

    fps = doc.GetFps()
    value = ( (time - startFrame / fps) * speed ) - delay * float(index)

    return value

#-------------------------------------------------------------------------------------------------------------

# Below is the engine that uses the above script.
# You can access it for creating more complex Fieldlayers and Fields.

# Declaring null constants
global NULLVECTOR
global NULLFLOAT
NULLVECTOR = c4d.Vector()
NULLFLOAT = 0.0

def InitSampling(op, info):

    # Update ratio for current sampling pass.
    global time
    global currentTimeRatio

    time = doc.GetTime().Get()
    currentTimeRatio = (time - doc.GetMinTime().Get()) / (doc.GetMaxTime().Get() - doc.GetMinTime().Get())
    # Multiplying by 2 to play the time twice in the project range.
    currentTimeRatio = currentTimeRatio * 2.0

    # Success, return False to prevent sampling.
    # FreeSampling will be called even if sampling was cancelled.
    return True

def FreeSampling(op, info):
    return True

def Sample(op, inputs, outputs, info):
    valueList = outputs._value

    if inputs._fullArraySize != 1 : #debug

        # First pass on even points to calculate values
        if 'SampleValue' in globals():
            for i in range(0, inputs._blockCount):
                valueList[i] = SampleValue(op,
                inputs._transform,
                i + inputs._blockOffset, #index
                inputs._fullArraySize - 1, #lastIndex
                )

    # Write the values in the FieldOutput
    outputs._value = valueList

    # No shape clipping here.
    outputs.ClearDeactivated(False)

    # Return false to cancel further sampling.
    return True