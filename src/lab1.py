import vtk

# initialize data
obj_reader = vtk.vtkOBJReader()
obj_reader.SetFileName("./data/Heart.obj")

plane = vtk.vtkPlane()
bounds = obj_reader.GetOutput().GetBounds()
plane.SetOrigin(
    (bounds[0] + bounds[1]) / 2,
    (bounds[2] + bounds[3]) / 2,
    (bounds[4] + bounds[5]) / 2,
)
plane.SetNormal(1, 0, 0)

clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(obj_reader.GetOutputPort())
clipper.SetClipFunction(plane)

clip_mapper = vtk.vtkPolyDataMapper()
clip_mapper.SetInputConnection(clipper.GetOutputPort())

clip_actor = vtk.vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetColor(0.9, 0.4, 0.4)

renderer = vtk.vtkRenderer()
renderer.AddActor(clip_actor)
renderer.SetBackground(0.1, 0.1, 0.2)

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1000, 800)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

plane_widget = vtk.vtkImplicitPlaneWidget()
plane_widget.SetInteractor(interactor)
plane_widget.SetPlaceFactor(1.0)
plane_widget.SetInputConnection(obj_reader.GetOutputPort())
plane_widget.PlaceWidget()
plane_widget.SetNormal(plane.GetNormal())
plane_widget.SetOrigin(plane.GetOrigin())
plane_widget.TubingOn()
plane_widget.On()


def update_clip(widget, event):
    widget.GetPlane(plane)
    render_window.Render()


plane_widget.AddObserver("InteractionEvent", update_clip)

renderer.ResetCamera()
interactor.Initialize()
interactor.Start()
