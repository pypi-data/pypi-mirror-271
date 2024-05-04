from WITecSDK.Parameters import COMParameters

class SpectralStitching:

    _parampath = "UserParameters|SpectralStitching|"

    def __init__(self, aCOMParameters: COMParameters):
        self._integrationTimeCOM = aCOMParameters.GetFloatParameter(self._parampath + "IntegrationTime")
        self._accumulationsCOM = aCOMParameters.GetIntParameter(self._parampath + "NumberOfAccumulations")
        self._startSpectralPosCOM = aCOMParameters.GetFloatParameter(self._parampath + "StartSpectralPosition")
        self._stopSpectralPosCOM = aCOMParameters.GetFloatParameter(self._parampath + "StopSpectralPosition")
        self._startSingleSpectrumCOM = aCOMParameters.GetTriggerParameter(self._parampath + "StartSpectralStitching")

    @property
    def NumberOfAccumulations(self) -> int:
        return self._accumulationsCOM.GetValue()

    @NumberOfAccumulations.setter
    def NumberOfAccumulations(self, numberOfAccumulations: int):
        self._accumulationsCOM.SetValue(numberOfAccumulations)

    @property
    def IntegrationTime(self) -> float:
        return self._integrationTimeCOM.GetValue()
    
    @IntegrationTime.setter
    def IntegrationTime(self, integrationTime: float):
        self._integrationTimeCOM.SetValue(integrationTime)

    @property
    def StartSpectralPosition(self) -> float:
        return self._startSpectralPosCOM.GetValue()
    
    @StartSpectralPosition.setter
    def StartSpectralPosition(self, startSpectralPos: float):
        self._startSpectralPosCOM.SetValue(startSpectralPos)

    @property
    def StopSpectralPosition(self) -> float:
        return self._stopSpectralPosCOM.GetValue()
    
    @StopSpectralPosition.setter
    def StopSpectralPosition(self, stopSpectralPos: float):
        self._stopSpectralPosCOM.SetValue(stopSpectralPos)

    def Start(self):
        self._startSingleSpectrumCOM.ExecuteTrigger()