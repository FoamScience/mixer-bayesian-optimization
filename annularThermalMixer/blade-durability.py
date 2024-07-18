## Computes area of blades+shaft where (wallShearStress**2) is greater than 70% of
## its value range at time = float(sys.argv[2]) secs

## arg1: Case path
## arg2: Time

import paraview
paraview.compatibility.major = 5
paraview.compatibility.minor = 10

#### import the simple module from the paraview
import sys
from paraview.simple import *
import paraview.servermanager as servermanager
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

casefoam = OpenFOAMReader(registrationName='case.foam', FileName=f'{sys.argv[1]}/case.foam')
casefoam.MeshRegions = ['group/movingWalls']
casefoam.Decomposepolyhedra = 0
UpdatePipeline(time=0.0, proxy=casefoam)
casefoam.CaseType = 'Decomposed Case'
casefoam.CellArrays = ['wallShearStress']
UpdatePipeline(time=float(sys.argv[2]), proxy=casefoam)

# create a new 'Python Calculator'
pythonCalculator1 = PythonCalculator(registrationName='PythonCalculator1', Input=casefoam)
UpdatePipeline(time=float(sys.argv[2]), proxy=pythonCalculator1)
pythonCalculator1.ArrayAssociation = 'Cell Data'
pythonCalculator1.ArrayName = 'w'
pythonCalculator1.Expression = 'pow(wallShearStress, 2)'

pythonCalculator2 = PythonCalculator(registrationName='PythonCalculator2', Input=pythonCalculator1)
UpdatePipeline(time=float(sys.argv[2]), proxy=pythonCalculator2)
pythonCalculator2.ArrayAssociation = 'Cell Data'
pythonCalculator2.ArrayName = 'wRange'
pythonCalculator2.Expression = 'min(w)+0.7*(max(w)-min(w))'

arr = servermanager.Fetch(pythonCalculator2)
wRangeThreshold = arr.GetBlock(0).GetBlock(0).GetCellData().GetArray("wRange").GetValue(0)

SetActiveSource(pythonCalculator1)

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=pythonCalculator1)
UpdatePipeline(time=float(sys.argv[2]), proxy=clip1)
clip1.ClipType = 'Scalar'
clip1.Scalars = ['CELLS', 'w']
clip1.Value = wRangeThreshold
arr = servermanager.Fetch(clip1)

# create a new 'Cell Size'
cellSize1 = CellSize(registrationName='CellSize1', Input=clip1)
UpdatePipeline(time=float(sys.argv[2]), proxy=cellSize1)
cellSize1.ComputeVertexCount = 0
cellSize1.ComputeLength = 0
cellSize1.ComputeVolume = 0
cellSize1.ComputeSum = 0
cellSize1.ComputeArea = 1

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=cellSize1)
UpdatePipeline(time=float(sys.argv[2]), proxy=integrateVariables1)
arr = servermanager.Fetch(integrateVariables1)
print(arr.GetCellData().GetArray("Area").GetValue(0))
