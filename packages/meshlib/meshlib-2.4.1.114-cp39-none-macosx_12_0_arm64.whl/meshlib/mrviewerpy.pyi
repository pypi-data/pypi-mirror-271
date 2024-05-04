from __future__ import annotations
import meshlib.mrmeshpy
import typing
__all__ = ['UiEntry', 'UiEntryType', 'Viewer', 'ViewerLaunchParams', 'ViewerLaunchParamsMode', 'ViewerSetup', 'Viewport', 'ViewportFitDataParams', 'ViewportFitMode', 'addMeshToScene', 'addPointCloudToScene', 'clearScene', 'getSelectedMeshes', 'launch', 'modifySelectedMesh', 'selectByName', 'selectByType', 'uiListEntries', 'uiPressButton', 'unselectAll']
class UiEntry:
    def __repr__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def type(self) -> UiEntryType:
        ...
class UiEntryType:
    """
    UI entry type enum.
    
    Members:
    
      button
    
      group
    
      other
    """
    __members__: typing.ClassVar[dict[str, UiEntryType]]  # value = {'button': <UiEntryType.button: 0>, 'group': <UiEntryType.group: 1>, 'other': <UiEntryType.other: 2>}
    button: typing.ClassVar[UiEntryType]  # value = <UiEntryType.button: 0>
    group: typing.ClassVar[UiEntryType]  # value = <UiEntryType.group: 1>
    other: typing.ClassVar[UiEntryType]  # value = <UiEntryType.other: 2>
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Viewer:
    """
    GLFW-based mesh viewer
    """
    def __init__(self) -> None:
        ...
    def captureScreenShot(self, path: str) -> None:
        """
        Captures part of window (redraw 3d scene over UI (without redrawing UI))
        """
    def incrementForceRedrawFrames(self, num: int = 1, swapOnLastOnly: bool = False) -> None:
        """
        Increment number of forced frames to redraw in event loop
        if `swapOnLastOnly` only last forced frame will be present on screen and all previous will not
        """
    def preciseFitDataViewport(self, vpList: meshlib.mrmeshpy.ViewportMask = ..., params: ViewportFitDataParams = ...) -> None:
        """
        Calls fitData and change FOV to match the screen size then
        params - params fit data
        """
    def shutdown(self) -> None:
        """
        sets stop event loop flag (this flag is glfwShouldWindowClose equivalent)
        """
    def skipFrames(self, frames: int) -> None:
        ...
    def viewport(self, viewportId: meshlib.mrmeshpy.ViewportId = ...) -> Viewport:
        """
        Return the current viewport, or the viewport corresponding to a given unique identifier
        	viewportId - unique identifier corresponding to the desired viewport (current viewport if 0)
        """
class ViewerLaunchParams:
    """
    This struct contains rules for viewer launch
    """
    height: int
    width: int
    windowMode: ViewerLaunchParamsMode
    def __init__(self) -> None:
        ...
    @property
    def animationMaxFps(self) -> int:
        """
        max fps if animating
        """
    @animationMaxFps.setter
    def animationMaxFps(self, arg0: int) -> None:
        ...
    @property
    def fullscreen(self) -> bool:
        """
        if true starts fullscreen
        """
    @fullscreen.setter
    def fullscreen(self, arg0: bool) -> None:
        ...
    @property
    def isAnimating(self) -> bool:
        """
        if true - calls render without system events
        """
    @isAnimating.setter
    def isAnimating(self, arg0: bool) -> None:
        ...
    @property
    def name(self) -> str:
        """
        Window name
        """
    @name.setter
    def name(self, arg0: str) -> None:
        ...
class ViewerLaunchParamsMode:
    """
    Members:
    
      Hide : Don't show window
    
      HideInit : Show window after init
    
      Show : Show window immediately
    
      TryHidden : Launches in "Hide" mode if OpenGL is present and "NoWindow" if it is not
    
      NoWindow : Don't initialize GL window (don't call GL functions)(force `isAnimating`)
    """
    Hide: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.Hide: 2>
    HideInit: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.HideInit: 1>
    NoWindow: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.NoWindow: 4>
    Show: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.Show: 0>
    TryHidden: typing.ClassVar[ViewerLaunchParamsMode]  # value = <ViewerLaunchParamsMode.TryHidden: 3>
    __members__: typing.ClassVar[dict[str, ViewerLaunchParamsMode]]  # value = {'Hide': <ViewerLaunchParamsMode.Hide: 2>, 'HideInit': <ViewerLaunchParamsMode.HideInit: 1>, 'Show': <ViewerLaunchParamsMode.Show: 0>, 'TryHidden': <ViewerLaunchParamsMode.TryHidden: 3>, 'NoWindow': <ViewerLaunchParamsMode.NoWindow: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ViewerSetup:
    def __init__(self) -> None:
        ...
class Viewport:
    """
    Viewport is a rectangular area, in which the objects of interest are going to be rendered.
    An application can have a number of viewports each with its own ID.
    """
    def cameraLookAlong(self, dir: meshlib.mrmeshpy.Vector3f, up: meshlib.mrmeshpy.Vector3f) -> None:
        """
        Set camera look direction and up direction (they should be perpendicular)
        this function changes camera position and do not change camera spot (0,0,0) by default
        to change camera position use setCameraTranslation after this function
        """
    def cameraRotateAround(self, axis: meshlib.mrmeshpy.Line3f, angle: float) -> None:
        """
        Rotates camera around axis +direction applied to axis point
        note: this can make camera clip objects (as far as distance to scene center is not fixed)
        """
class ViewportFitDataParams:
    def __init__(self) -> None:
        ...
    @property
    def factor(self) -> float:
        """
        part of the screen for scene location
        """
    @factor.setter
    def factor(self, arg0: float) -> None:
        ...
    @property
    def mode(self) -> ViewportFitMode:
        """
        fit mode
        """
    @mode.setter
    def mode(self, arg0: ViewportFitMode) -> None:
        ...
    @property
    def snapView(self) -> bool:
        """
        snapView - to snap camera angle to closest canonical quaternion
        """
    @snapView.setter
    def snapView(self, arg0: bool) -> None:
        ...
class ViewportFitMode:
    """
    Fit mode ( types of objects for which the fit is applied )
    
    Members:
    
      Visible : fit all visible objects
    
      SelectedObjects : fit only selected objects
    
      SelectedPrimitives : fit only selected primitives
    """
    SelectedObjects: typing.ClassVar[ViewportFitMode]  # value = <ViewportFitMode.SelectedObjects: 2>
    SelectedPrimitives: typing.ClassVar[ViewportFitMode]  # value = <ViewportFitMode.SelectedPrimitives: 1>
    Visible: typing.ClassVar[ViewportFitMode]  # value = <ViewportFitMode.Visible: 0>
    __members__: typing.ClassVar[dict[str, ViewportFitMode]]  # value = {'Visible': <ViewportFitMode.Visible: 0>, 'SelectedObjects': <ViewportFitMode.SelectedObjects: 2>, 'SelectedPrimitives': <ViewportFitMode.SelectedPrimitives: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
def addMeshToScene(mesh: meshlib.mrmeshpy.Mesh, name: str) -> None:
    """
    add given mesh to scene tree
    """
def addPointCloudToScene(points: meshlib.mrmeshpy.PointCloud, name: str) -> None:
    """
    add given point cloud to scene tree
    """
def clearScene() -> None:
    """
    remove all objects from scene tree
    """
def getSelectedMeshes() -> meshlib.mrmeshpy.vectorMesh:
    """
    Get copies of all selected meshes in the scene.
    """
def launch(params: ViewerLaunchParams = ..., setup: ViewerSetup = ...) -> None:
    """
    starts default viewer with given params and setup
    """
def modifySelectedMesh(mesh: meshlib.mrmeshpy.Mesh) -> None:
    """
    Assign a new mesh to the selected mesh object. Exactly one object must be selected.
    """
def selectByName(objectName: str) -> None:
    """
    select objects in scene tree with given name, unselect others
    """
def selectByType(typeName: str) -> None:
    """
    string typeName: {"Meshes", "Points", "Voxels"}
    objects in scene tree with given type, unselect others
    """
def uiListEntries(arg0: list[str]) -> list[UiEntry]:
    """
    List existing UI entries at the specified path.
    Pass an empty list to see top-level groups.
    Add group name to the end of the vector to see its contents.
    When you find the button you need, pass it to `uiPressButton()`.
    """
def uiPressButton(arg0: list[str]) -> None:
    """
    Simulate a button click. Use `uiListEntries()` to find button names.
    """
def unselectAll() -> None:
    """
    unselect all objects in scene tree
    """
