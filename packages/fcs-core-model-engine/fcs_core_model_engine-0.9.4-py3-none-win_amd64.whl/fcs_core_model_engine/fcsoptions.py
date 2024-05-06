from enum import Enum, auto

class StatusMessageType(Enum):
    """
    Simple flags for status messages.
    """
    InfoStatus = 3
    WarningStatus = 4
    FailureStatus = 5

class ProcessExitStatus(Enum):
    """
    Encompasses possible exit statuses for a process.
    """

    Successful = 0 
    Warning = 1
    Failure = 2

    @staticmethod
    def is_valid_status(allegedly_valid_status: 'ProcessExitStatus') -> bool:
        """
        Checks if the passed in `allegedly_valid_status` belongs to 
        any of the allowed options.

        Returns:
            bool: True, if the status passed is among the existing options.
        """
        return allegedly_valid_status in ProcessExitStatus
    
class ContainerTypes(Enum):
    NotSpecified = 0
    Geometry = auto()
    Mesh = auto()
    Collaboration = auto()

class DataTypes(Enum):
    # Sub-shapes
    Face = 0
    Vertex = auto()
    Edge = auto()
    Element = auto()
    Node = auto()

    # Shapes
    TopoFace = auto()
    TopoEdge = auto()
    TopoVertex = auto()
    TopoWire = auto()
    TopoShell = auto()
    TopoSolid = auto()
    TopoElement = auto()
    TopoNode = auto()
    TopoMesh = auto()

    # Files
    Part = auto()
    Vector = auto()
    CoordinateSystem = auto()
    Thread = auto()
    Mesh = auto()

    # Folders
    Assembly = auto()
    Set = auto()
    Group = auto()

    # Containers
    GeometryCnt = auto()
    MeshCnt = auto()
