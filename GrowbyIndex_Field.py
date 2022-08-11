"""
Grow by Index 
Author : Sheng Wen Cheng
"""
import c4d
import math
from c4d.modules import mograph as mo

#
#These are simpler functions to allow quickly and easily make custom fields
#To use them, change the contents of the Value, Color, Alpha and Direction preset functions
#For more customization, the core functions can be found at the bottom

#Variables:
    #pos = sample's position, index = sample's index, lastIndex = sample's the last index of, transform = a matrix to bring the samples to global space
    #uvw = sample's uvw coordinates, direction = sample's the directions
    #op = the field object
    #time = current time, #timeratio = current time progression in the document


#-------------------------------------------------------------------------------------------------------------

# VALUE (float)
def SampleValue(op, transform, pos, index, lastIndex, uvw, direction):

    duration = 1 #Animation Duration Q: if clone objects has different duration?
    lastIndex = 12 # Bug
    value = (time/duration) - ( float(index) / lastIndex )

    return value

# COLOR (vector)
def SampleColor(op, transform, pos, index, lastIndex, uvw, direction):
    # Calculate the Color channel of the Python Field below
    globalpos = pos * transform
    radius = 1 - min(1,  (globalpos - op.GetMg().off).GetLength() / 200.0)
    color = c4d.Vector(radius, radius / 2.0, 0.3)
    #End of your code
    return color

# ALPHA (float)
def SampleAlpha(op, transform, pos, index, lastIndex, uvw, direction):
    # Calculate the Color Alpha channel of the Python Field below
    alpha = 1.0
    #End of your code
    return alpha

# DIRECTION (vector)
def SampleDir(op, transform, pos, index, lastIndex, uvw, direction):
    # Calculate the Direction channel of the Python Field below
    globalpos = pos * transform
    direction = (globalpos - op.GetMg().off).GetNormalized()
    #End of your code
    return direction

#-------------------------------------------------------------------------------------------------------------

# Below is the engine that uses the above script.
# You can access it for creating more complex Fieldlayers and Fields.

# Declaring null constants
global NULLVECTOR
global NULLFLOAT
NULLVECTOR = c4d.Vector()
NULLFLOAT = 0.0

def InitSampling(op, info):
    #Initializes sampling pass.
    #Perform allocation and initializations here to speed up sampling.
    #Return false on error to cancel sampling.
    #NOTE: InitSampling function is not required. If you don't need
    #it, you can remove it to increase performance.

    #Keyword arguments:
        #c4d.modules.mograph.FieldObject -- the python field.
        #c4d.modules.mograph.FieldInfo -- the sampling informations.
#

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
    #Cleanup sampling data.
    #Perform deallocation and reset here.
    #Next sampling pass will start with another call to InitSampling.
    #Return True on success. False return will print an error but it
    #won't cancel anything at this point.
    #NOTE: FreeSampling function is not required. If you don't need
    #it, you can remove it to increase performance.

    #Keyword arguments:
        #c4d.modules.mograph.FieldObject -- the python field.
        #c4d.modules.mograph.FieldInfo -- the sampling informations.
#

    # Nothing to cleanup, just return success.
    return True

def Sample(op, inputs, outputs, info):
    #Calculate the output values for the specified set
    #of input points. Allocations should be avoided in Sample
    #to maximize performance.
    #Return false on error to cancel sampling.
    #NOTE: Sample function is mandatory, PythonField cannot
    #function without it.

    #Keyword arguments:
        #c4d.modules.mograph.FieldObject -- the python field.
        #c4d.modules.mograph.FieldInput -- the points to sample.
        #c4d.modules.mograph.FieldOutput -- the sampling output arrays (pre-allocated).
        #c4d.modules.mograph.FieldInfo -- the sampling informations.


    # You can extract an output list and write to it directly.
    # Don't forget to write back the list at the end.
    valueList = outputs._value
    # Or use outputs.GetValue(index) outputs.SetValue(index) to
    # access a single value.

    # Checking Active Channels
    availableColor = True if outputs._color and outputs._alpha else False
    availableAlpha = True if outputs._alpha else False
    availableDirection = True if outputs._direction else False

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

    # Depending on the color parameters of the Effector and FieldLayer,
    # color arrays could be empty. You can check the FieldInfo flags also
    # to validate this.
    colorList = outputs._color
    alphaList = outputs._alpha
    if availableColor:
        if 'SampleColor' in globals():
            for i in range(0, inputs._blockCount):
                colorList[i] = SampleColor(op,
                inputs._transform,
                inputs._position[i] if inputPosition else NULLVECTOR,
            i + inputs._blockOffset,
            inputs._fullArraySize - 1,
            inputs._uvw[i] if inputUvw else NULLVECTOR,
            inputs._direction[i] if inputDirection else NULLVECTOR
            )
        else:
            for i in range(0, inputs._blockCount):
                colorList[i] = c4d.Vector(1.0)

        if 'SampleAlpha' in globals():
            for i in range(0, inputs._blockCount):
                alphaList[i] = SampleAlpha(op,
                inputs._transform,
                inputs._position[i] if inputPosition else NULLVECTOR,
            i + inputs._blockOffset,
            inputs._fullArraySize - 1,
            inputs._uvw[i] if inputUvw else NULLVECTOR,
            inputs._direction[i] if inputDirection else NULLVECTOR
            )
        else:
            for i in range(0, inputs._blockCount):
                alphaList[i] = 1.0

        # Write the colors in the FieldOutput
        outputs._color = colorList
        outputs._alpha = alphaList

    dirList = outputs._direction
    if availableDirection and ('SampleDir' in globals()):
        for i in range(0, inputs._blockCount):
            dirList[i] = SampleDir(op,
            inputs._transform,
            inputs._position[i] if inputPosition else NULLVECTOR,
            i + inputs._blockOffset,
            inputs._fullArraySize - 1,
            inputs._uvw[i] if inputUvw else NULLVECTOR,
            inputs._direction[i] if inputDirection else NULLVECTOR
            )

        outputs._direction = dirList

    # No shape clipping here.
    outputs.ClearDeactivated(False)

    # Return false to cancel further sampling.
    return True