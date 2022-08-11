"""
Grow by Index - Python Field
Author : Sheng Wen Cheng
"""
import c4d
import math
from c4d.modules import mograph as mo

#Variables:
    #pos = sample's position, index = sample's index, lastIndex = sample's the last index of, transform = a matrix to bring the samples to global space
    #uvw = sample's uvw coordinates, direction = sample's the directions
    #op = the field object
    #time = current time, #timeratio = current time progression in the document

#-------------------------------------------------------------------------------------------------------------

# VALUE (float)
def SampleValue(op, transform, pos, index, lastIndex, uvw, direction):

    speed = 1 # Grow Speed (Unit : 1 / Second)
    gap = 1 # The time to iteration all index ( Unit : Second )
    
    # lastIndex = 12 # Bug
    value = ( time * speed ) - ( float(index) / lastIndex ) * gap 

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
    # Or use outputs.GetValue(index) outputs.SetValue(index) to
    # access a single value.

    # Checking Available Inputs of Sample
    inputPosition = True if inputs._position else False
    inputUvw = True if inputs._uvw else False
    inputDirection = True if inputs._direction else False

    # First pass on even points to calculate values
    if 'SampleValue' in globals():
        for i in range(0, inputs._blockCount):
            valueList[i] = SampleValue(op,
            inputs._transform,
            inputs._position[i] if inputPosition else NULLVECTOR,
            i + inputs._blockOffset,
            inputs._fullArraySize - 1,
            inputs._uvw[i] if inputUvw else NULLVECTOR,
            inputs._direction[i] if inputDirection else NULLVECTOR
            )

    # Write the values in the FieldOutput
    outputs._value = valueList

    # No shape clipping here.
    outputs.ClearDeactivated(False)

    # Return false to cancel further sampling.
    return True