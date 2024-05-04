from WITecSDK.Parameters import COMParameters, ParameterNotAvailableException

class ScanTable:

    _sparampath = "UserParameters|ScanTable|"

    def __init__(self, aCOMParameters: COMParameters):
        self._positionXCOM = aCOMParameters.GetFloatParameter(self._sparampath + "PositionX")
        self._positionYCOM = aCOMParameters.GetFloatParameter(self._sparampath + "PositionY")
        self._positionZCOM = aCOMParameters.GetFloatParameter(self._sparampath + "PositionZ")

    @property
    def PositionX(self) -> float:
        return self._positionXCOM.GetValue()
    
    @PositionX.setter
    def PositionX(self, posX: float):
        self._positionXCOM.SetValue(posX)

    @property
    def PositionY(self) -> float:
        return self._positionYCOM.GetValue()
    
    @PositionY.setter
    def PositionY(self, posY: float):
        self._positionYCOM.SetValue(posY)

    @property
    def PositionZ(self) -> float:
        return self._positionZCOM.GetValue()
    
    @PositionZ.setter
    def PositionZ(self, posZ: float):
        self._positionZCOM.SetValue(posZ)
