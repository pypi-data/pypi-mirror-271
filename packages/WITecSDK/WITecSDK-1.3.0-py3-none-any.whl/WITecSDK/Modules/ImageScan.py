from WITecSDK.Modules.HelperStructs import XYZPosition, LargeAreaSettings
from WITecSDK.Parameters import COMParameters, ParameterNotAvailableException

class ImageScan:

    _parampath = "UserParameters|SequencerScanImage|"
    
    def __init__(self, aCOMParameters: COMParameters):
        
        channelpath = "UserParameters|DAQSources|SpectralChannels|"
        self._scanMethodCOM = aCOMParameters.GetEnumParameter(self._parampath + "ConsecutiveMode")
        self._pointsPerLineCOM = aCOMParameters.GetIntParameter(self._parampath + "PointsPerLine")
        self._linesPerImageCOM = aCOMParameters.GetIntParameter(self._parampath + "LinesPerImage")
        self._layersPerScanCOM = aCOMParameters.GetIntParameter(self._parampath + "LayersPerScan")
        self._widthCOM = aCOMParameters.GetFloatParameter(self._parampath + "Geometry|Width")
        self._heightCOM = aCOMParameters.GetFloatParameter(self._parampath + "Geometry|Height")
        self._depthCOM = aCOMParameters.GetFloatParameter(self._parampath + "Geometry|Depth")
        self._centerAtCurrentPosCOM = aCOMParameters.GetTriggerParameter(self._parampath + "Geometry|CenterAtCurrentPosition")
        self._centerXCOM = aCOMParameters.GetFloatParameter(self._parampath + "Geometry|CenterX")
        self._centerYCOM = aCOMParameters.GetFloatParameter(self._parampath + "Geometry|CenterY")
        self._centerZCOM = aCOMParameters.GetFloatParameter(self._parampath + "Geometry|CenterZ")
        self._gammaCOM = aCOMParameters.GetFloatParameter(self._parampath + "Geometry|Gamma")
        self._alphaCOM = aCOMParameters.GetFloatParameter(self._parampath + "Geometry|Alpha")
        self._betaCOM = aCOMParameters.GetFloatParameter(self._parampath + "Geometry|Beta")
        self._startCOM = aCOMParameters.GetTriggerParameter(self._parampath + "Start")
        self._integrationTimeCOM = aCOMParameters.GetFloatParameter(self._parampath + "TraceIntegrationTime")
        self._FilterManager1 = None
        self._FilterManager1R = None
        self._FilterManager2 = None
        self._FilterManager2R = None
        self._FilterManager3 = None
        self._FilterManager3R = None
        try:
            self._FilterManager1 = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera1Data|ScanImage|CreateFilterManagerTrace")
            self._FilterManager1R = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera1Data|ScanImage|CreateFilterManagerRetrace")
            self._FilterManager2 = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera2Data|ScanImage|CreateFilterManagerTrace")
            self._FilterManager2R = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera2Data|ScanImage|CreateFilterManagerRetrace")
            self._FilterManager3 = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera3Data|ScanImage|CreateFilterManagerTrace")
            self._FilterManager3R = aCOMParameters.GetBoolParameter(channelpath + "SpectralCamera3Data|ScanImage|CreateFilterManagerRetrace")
        except ParameterNotAvailableException:
            pass
        except Exception as e:
            raise e
        
    def _initialize(self, points: int, lines: int, width: float, integrationTime: float, center: XYZPosition, gamma: float):
        if center is not None:
            self.Center = center
        else:
            self.centerAtCurrenPos()
        self.Gamma = gamma
        self.IntegrationTime = integrationTime
        self._pointsPerLineCOM.SetValue(points)
        self._linesPerImageCOM.SetValue(lines)
        self._widthCOM.SetValue(width)

    def InitializeArea(self, points: int, lines: int, width: float, height: float, integrationTime: float, center: XYZPosition = None, gamma: float = 0):
        self._initialize(points, lines, width, integrationTime, center, gamma)
        self.setScanMethodToArea()
        self._heightCOM.SetValue(height)     

    def InitializeDepth(self, points: int, lines: int, width: float, depth: float, integrationTime: float, center: XYZPosition = None, gamma: float = 0):
        self._initialize(points, lines, width, integrationTime, center, gamma)
        self.setScanMethodToDepth()
        self._depthCOM.SetValue(depth)

    def InitializeStack(self, points: int, lines: int, layers: int, width: float, height: float, depth: float, integrationTime: float, center: XYZPosition = None, gamma: float = 0):
        self._initialize(points, lines, width, integrationTime, center, gamma)
        self.setScanMethodToStack()
        self._layersPerScanCOM.SetValue(layers)
        self._heightCOM.SetValue(height)
        self._depthCOM.SetValue(depth)

    def GetAllParameters(self) -> LargeAreaSettings:
        return LargeAreaSettings(self._scanMethodCOM.GetValue(), self._pointsPerLineCOM.GetValue(), self._linesPerImageCOM.GetValue(),
                                 self._layersPerScanCOM.GetValue(), self._widthCOM.GetValue(), self._heightCOM.GetValue(),
                                 self._depthCOM.GetValue(), self.IntegrationTime, self.Center, self.Gamma)

    def SetAllParameters(self, LAStruct: LargeAreaSettings):
        if LAStruct.Mode == 0 or LAStruct.Mode == 1:
            self.InitializeArea(LAStruct.Points, LAStruct.Lines, LAStruct.Width, LAStruct.Height,
                                LAStruct.IntegrationTime, LAStruct.Center, LAStruct.Gamma)
        elif LAStruct.Mode == 2 or LAStruct.Mode == 3:
            self.InitializeDepth(LAStruct.Points, LAStruct.Lines, LAStruct.Width, LAStruct.Depth,
                                 LAStruct.IntegrationTime, LAStruct.Center, LAStruct.Gamma)
        elif LAStruct.Mode == 4:
            self.InitializeStack(LAStruct.Points, LAStruct.Lines, LAStruct.Layers ,LAStruct.Width,
                                 LAStruct.Height, LAStruct.Depth, LAStruct.IntegrationTime, LAStruct.Center, LAStruct.Gamma)
        else:
            raise Exception('Mode is not supported')

    def setScanMethodToArea(self):
        self._scanMethodCOM.SetValue(0)

    def setScanMethodToAreaLoop(self):
        self._scanMethodCOM.SetValue(1)

    def setScanMethodToDepth(self):
        self._scanMethodCOM.SetValue(2)

    def setScanMethodToDepthLoop(self):
        self._scanMethodCOM.SetValue(3)
        
    def setScanMethodToStack(self):
        self._scanMethodCOM.SetValue(4)

    def centerAtCurrenPos(self):
        self._centerAtCurrentPosCOM.ExecuteTrigger()

    def DeactivateFilterViewer(self):
        if self._FilterManager1 is not None:
            self._FilterManager1.SetValue(False)
            self._FilterManager1R.SetValue(False)
        if self._FilterManager2 is not None:
            self._FilterManager2.SetValue(False)
            self._FilterManager2R.SetValue(False)
        if self._FilterManager3 is not None:
            self._FilterManager3.SetValue(False)
            self._FilterManager3R.SetValue(False)

    @property
    def Center(self) -> XYZPosition:
        return XYZPosition(self._centerXCOM.GetValue(), self._centerYCOM.GetValue(), self._centerZCOM.GetValue())
    
    @Center.setter
    def Center(self, centerPoint: XYZPosition):
        self._centerXCOM.SetValue(centerPoint.X)
        self._centerYCOM.SetValue(centerPoint.Y)
        self._centerZCOM.SetValue(centerPoint.Z)

    @property
    def Gamma(self) -> float:
        return self._gammaCOM.GetValue()

    @Gamma.setter
    def Gamma(self, gamma: float):
        self._gammaCOM.SetValue(gamma)

    @property
    def Alpha(self) -> float:
        return self._alphaCOM.GetValue()

    @Alpha.setter
    def Alpha(self, alpha: float):
        self._alphaCOM.SetValue(alpha)

    @property
    def Beta(self) -> float:
        return self._betaCOM.GetValue()

    @Gamma.setter
    def Beta(self, beta: float):
        self._betaCOM.SetValue(beta)

    @property
    def IntegrationTime(self) -> float:
        return self._integrationTimeCOM.GetValue()

    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.SetValue(integrationTime)

    def Start(self):
        self._startCOM.ExecuteTrigger()

