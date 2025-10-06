# trace generated using paraview version 5.10.0
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 10

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
casefoam = OpenFOAMReader(registrationName='case.foam', FileName=f'{sys.argv[1]}/case.foam')
casefoam.MeshRegions = ['internalMesh']
casefoam.Decomposepolyhedra = 0

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
casefoamDisplay = Show(casefoam, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
casefoamDisplay.Representation = 'Surface'
casefoamDisplay.ColorArrayName = [None, '']
casefoamDisplay.SelectTCoordArray = 'None'
casefoamDisplay.SelectNormalArray = 'None'
casefoamDisplay.SelectTangentArray = 'None'
casefoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
casefoamDisplay.SelectOrientationVectors = 'None'
casefoamDisplay.ScaleFactor = 0.02000000644089326
casefoamDisplay.SelectScaleArray = 'None'
casefoamDisplay.GlyphType = 'Arrow'
casefoamDisplay.GlyphTableIndexArray = 'None'
casefoamDisplay.GaussianRadius = 0.0010000003220446629
casefoamDisplay.SetScaleArray = [None, '']
casefoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
casefoamDisplay.OpacityArray = [None, '']
casefoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'
casefoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
casefoamDisplay.PolarAxes = 'PolarAxesRepresentation'
casefoamDisplay.ScalarOpacityUnitDistance = 0.007948100890761391
casefoamDisplay.OpacityArrayName = ['FIELD', 'CasePath']

# reset view to fit data
renderView1.ResetCamera(False)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# update the view to ensure updated data information
renderView1.Update()

# reset view to fit data
renderView1.ResetCamera(False)

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=casefoam)
clip1.ClipType = 'Plane'
clip1.HyperTreeGridClipper = 'Plane'
clip1.Scalars = [None, '']

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [0.0, 0.0, 0.09999997077576595]

# init the 'Plane' selected for 'HyperTreeGridClipper'
clip1.HyperTreeGridClipper.Origin = [0.0, 0.0, 0.09999997077576595]

# Properties modified on clip1
clip1.Scalars = ['POINTS', '']

# show data in view
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display.Representation = 'Surface'
clip1Display.ColorArrayName = [None, '']
clip1Display.SelectTCoordArray = 'None'
clip1Display.SelectNormalArray = 'None'
clip1Display.SelectTangentArray = 'None'
clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display.SelectOrientationVectors = 'None'
clip1Display.ScaleFactor = 0.02000000641773312
clip1Display.SelectScaleArray = 'None'
clip1Display.GlyphType = 'Arrow'
clip1Display.GlyphTableIndexArray = 'None'
clip1Display.GaussianRadius = 0.001000000320886656
clip1Display.SetScaleArray = [None, '']
clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display.OpacityArray = [None, '']
clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
clip1Display.DataAxesGrid = 'GridAxesRepresentation'
clip1Display.PolarAxes = 'PolarAxesRepresentation'
clip1Display.ScalarOpacityUnitDistance = 0.008392326916994984
clip1Display.OpacityArrayName = ['FIELD', 'CasePath']

# hide data in view
Hide(casefoam, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=clip1.ClipType)

# set active source
SetActiveSource(casefoam)

# Properties modified on casefoam
casefoam.CaseType = 'Decomposed Case'

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

animationScene1.GoToLast()

# set active source
SetActiveSource(clip1)

# Properties modified on casefoam
casefoam.CellArrays = ['T', 'U', 'alphat', 'dpdt', 'epsilon', 'k', 'nut', 'p', 'rho', 'wallShearStress']

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(clip1Display, ('CELLS', 'T'))

# rescale color and/or opacity maps used to include current data range
clip1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'T'
tLUT = GetColorTransferFunction('T')

# get opacity transfer function/opacity map for 'T'
tPWF = GetOpacityTransferFunction('T')

# set active source
SetActiveSource(casefoam)

# create a new 'OpenFOAMReader'
casefoam_1 = OpenFOAMReader(registrationName='case.foam', FileName=f'{sys.argv[1]}/case.foam')
casefoam_1.MeshRegions = ['internalMesh']
casefoam_1.Decomposepolyhedra = 0

# show data in view
casefoam_1Display = Show(casefoam_1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
casefoam_1Display.Representation = 'Surface'
casefoam_1Display.ColorArrayName = [None, '']
casefoam_1Display.SelectTCoordArray = 'None'
casefoam_1Display.SelectNormalArray = 'None'
casefoam_1Display.SelectTangentArray = 'None'
casefoam_1Display.OSPRayScaleFunction = 'PiecewiseFunction'
casefoam_1Display.SelectOrientationVectors = 'None'
casefoam_1Display.ScaleFactor = 0.02000000644089326
casefoam_1Display.SelectScaleArray = 'None'
casefoam_1Display.GlyphType = 'Arrow'
casefoam_1Display.GlyphTableIndexArray = 'None'
casefoam_1Display.GaussianRadius = 0.0010000003220446629
casefoam_1Display.SetScaleArray = [None, '']
casefoam_1Display.ScaleTransferFunction = 'PiecewiseFunction'
casefoam_1Display.OpacityArray = [None, '']
casefoam_1Display.OpacityTransferFunction = 'PiecewiseFunction'
casefoam_1Display.DataAxesGrid = 'GridAxesRepresentation'
casefoam_1Display.PolarAxes = 'PolarAxesRepresentation'
casefoam_1Display.ScalarOpacityUnitDistance = 0.007948100890761391
casefoam_1Display.OpacityArrayName = ['FIELD', 'CasePath']

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on casefoam_1
casefoam_1.CaseType = 'Decomposed Case'

# update the view to ensure updated data information
renderView1.Update()

animationScene1.GoToLast()

# Properties modified on casefoam_1
casefoam_1.MeshRegions = ['group/movingWalls', 'internalMesh']
casefoam_1.CellArrays = ['T', 'U', 'alphat', 'dpdt', 'epsilon', 'k', 'nut', 'p', 'rho', 'wallShearStress']

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on casefoam_1
casefoam_1.MeshRegions = ['group/movingWalls']

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(casefoam_1Display, ('CELLS', 'wallShearStress', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
casefoam_1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
casefoam_1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'wallShearStress'
wallShearStressLUT = GetColorTransferFunction('wallShearStress')

# get opacity transfer function/opacity map for 'wallShearStress'
wallShearStressPWF = GetOpacityTransferFunction('wallShearStress')

# get color legend/bar for wallShearStressLUT in view renderView1
wallShearStressLUTColorBar = GetScalarBar(wallShearStressLUT, renderView1)

# change scalar bar placement
wallShearStressLUTColorBar.WindowLocation = 'Any Location'
wallShearStressLUTColorBar.Position = [0.8074901445466492, 0.5670945157526255]
wallShearStressLUTColorBar.ScalarBarLength = 0.33000000000000007

# get color legend/bar for tLUT in view renderView1
tLUTColorBar = GetScalarBar(tLUT, renderView1)

# change scalar bar placement
tLUTColorBar.WindowLocation = 'Any Location'
tLUTColorBar.Position = [0.9244415243101183, 0.01283547257876317]

# change scalar bar placement
tLUTColorBar.Position = [0.8101182654402103, 0.12718786464410736]

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
wallShearStressLUT.ApplyPreset('Viridis (matplotlib)', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
wallShearStressLUT.ApplyPreset('Viridis (matplotlib)', True)

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(1522, 857)

# current camera placement for renderView1
renderView1.CameraPosition = [0.32853704626875113, 0.3086985667788851, 0.20802543324067163]
renderView1.CameraFocalPoint = [-0.030297167227738113, 0.04837149253678295, 0.09715387905344046]
renderView1.CameraViewUp = [-0.19896672090269937, -0.1389087880146568, 0.9701116392382511]
renderView1.CameraParallelScale = 0.17316410930356718

# save screenshot
SaveScreenshot(f'{sys.argv[1]}/{sys.argv[2]}.png', renderView1, ImageResolution=[1522, 857],
    TransparentBackground=1)

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1522, 857)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [0.32853704626875113, 0.3086985667788851, 0.20802543324067163]
renderView1.CameraFocalPoint = [-0.030297167227738113, 0.04837149253678295, 0.09715387905344046]
renderView1.CameraViewUp = [-0.19896672090269937, -0.1389087880146568, 0.9701116392382511]
renderView1.CameraParallelScale = 0.17316410930356718

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).ide3DWidgets(proxy=clip1.ClipType)
