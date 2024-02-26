from typing import List, Optional
from pydantic import BaseModel, UUID4
from datetime import datetime


class HeaderCalibr(BaseModel):
    version: str
    uuid: UUID4
    timestamp: int
    packet: str
    consume_queue: str


class CameraCalibr(BaseModel):
    calibration: bool


class Body_1(BaseModel):
    cameras: List[CameraCalibr]


class CameraPosition(BaseModel):
    position: bool


class Body_2(BaseModel):
    cameras: List[CameraPosition]


class Body_3(BaseModel):
    position: bool
    img: str


class Body_31(BaseModel):
    position: bool
    result: bool


class JSON1(BaseModel):
    header: HeaderCalibr
    body: Body_1


class JSON0(BaseModel):
    header: HeaderCalibr
    body: Body_2


class JSON3(BaseModel):
    header: HeaderCalibr
    body: Body_3


class JSON31(BaseModel):
    header: HeaderCalibr
    body: Body_31


class JSON32(BaseModel):
    header: HeaderCalibr
    body: Body_3


class HeaderJSON4(BaseModel):
    version: str
    uuid: UUID4
    timestamp: datetime
    packet: str


class BodyCamerasJSON4(BaseModel):
    name: str
    position: int
    matrix: List[List]


class BodyCamerasJSON2(BaseModel):
    name: str
    position: int
    img: List[List]
    calibration: bool


class BodyJSON4(BaseModel):
    cameras: List[BodyCamerasJSON4]


class JSON4(BaseModel):
    header: HeaderJSON4
    body: BodyJSON4


class ConfirmMatrixApplicationBody(BaseModel):
    position: bool
    result: bool


class JSON5(BaseModel):
    header: HeaderCalibr
    body: ConfirmMatrixApplicationBody


class BodyJSON2(BaseModel):
    cameras: List[BodyCamerasJSON2]


class JSON2(BaseModel):
    header: HeaderJSON4
    body: BodyJSON2

class CalibrationFinalizationBody(BaseModel):
    result: bool
    errors: List[str]

class JSON6(BaseModel):
    header: HeaderCalibr
    body: CalibrationFinalizationBody

class Header(BaseModel):
    version: str
    uuid: UUID4
    timestamp: int
    packet: str
    groupUUID: UUID4
    packetNumber: int
    totalPackages: int
    consume_queue: str
    block_id: str

class Image(BaseModel):
    calculatorSheetID: str
    innerSheetID: str
    isFinal: bool
    type: str
    height: dict
    width: dict
    cameraNumber: int
    coordinates: dict
    imgMapArray: List[List]

class Body(BaseModel):
    images: List[Image]

class Data(BaseModel):
    header: Header
    body: Body

class Header2(BaseModel):
    version: str
    uuid: UUID4
    timestamp: int
    packet: str
    consume_queue: str
    block_id: str


class Reference(BaseModel):
    depth: float
    length: float
    width: float


class Sheet(BaseModel):
    innerSheetID: str
    cleaning: bool
    reference: Reference


class Body2(BaseModel):
    sheet: List[Sheet]

class Data2(BaseModel):
    header: Header2
    body: Body2


class Camera(BaseModel):
    name: str
    position: int
    status: int
    errors: Optional[List[str]] | None = None


class BodyCamera(BaseModel):
    cameras: List[Camera]


class DataCamera(BaseModel):
    header: Header2
    body: BodyCamera

class SheetSize(BaseModel):
    calculatorSheetID: str
    innerSheetID: str
    length: dict
    width: dict
    height: dict

class HeaderGeom(BaseModel):
    version: str
    uuid: UUID4
    timestamp: int
    packet: str
    groupUUID: UUID4
    packetNumber: int
    totalPackages: int
    consume_queue: str

class GeometryEvaluation(BaseModel):
    header: HeaderGeom
    body: SheetSize
