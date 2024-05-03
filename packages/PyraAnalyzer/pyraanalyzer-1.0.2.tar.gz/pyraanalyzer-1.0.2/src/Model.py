class Name (object):
    def __init__(self):
        self.name = None

    def SetName(self, name:str):
        self.name = name  

class ResultDegrees (object):
    def __init__(self, m:float, l:float):
        self.gCer = float(m) - float(l)
        self.gUnc = float(m) + float(l) - 1
        self.lowDefinitionState = None
    
    def SetLowDefinitionState(self, lowDefinitionState:str):
        self.lowDefinitionState = lowDefinitionState

class Decision(object):
    def __init__(self, gCer:float, gUnc:float, lowDefinitionState:str):
        self.gCer = float(gCer)
        self.gUnc = float(gUnc)
        self.lowDefinitionState = lowDefinitionState


class EvidenceDegrees(object):
    def __init__(self):
        self.m = 0
        self.l = 0
    
    def SetMi(self, m:float):
        self.m = float(m)

    def SetLambda(self, l:float):
        self.l = float(l)

class Section (Name):
    def __init__(self):
        super().__init__()
        self.evidenceDegrees = None
        self.resultDegrees = None

    def SetEvidenceDegrees(self, evidenceDegrees:EvidenceDegrees):
        self.evidenceDegrees = evidenceDegrees

    def SetResultDegrees(self, resultDegrees:EvidenceDegrees):
        self.resultDegrees = resultDegrees

class Factor (Name):
    def __init__(self):
        super().__init__()
        self.weight = 1
        self.sections = []
    
    def SetWeight(self, weight:int):
        self.weight = int(weight)

    def SetSection(self, section:Section):
        self.sections.append(section)

    def UpdateSection(self, section:Section, idx):
        self.sections[idx] = section
    
    def DeleteSection(self, idx):
        self.sections.pop(idx)
    
    def GetIndexByPattern(self, pattern):
        return next((i for i, item in enumerate(self.sections) if pattern in item.name), -1)

class Expert (Name):
    def __init__(self):
        super().__init__()
        self.factors = []

    def SetFactor(self, factor:Factor):
        self.factors.append(factor)

    def UpdateFactor(self, factor:Factor, idx):
        self.factors[idx] = factor
    
    def DeleteFactor(self, idx):
        self.factors.pop(idx)

    def GetIndexByPattern(self, pattern):
        return next((i for i, item in enumerate(self.factors) if pattern in item.name), -1)
    
class Group (Name):
    def __init__(self):
        super().__init__()
        self.experts = []

    def SetExpert(self, expert:Expert):
        self.experts.append(expert)

    def UpdateExpert(self, expert:Expert, idx):
        self.experts[idx] = expert
    
    def DeleteExpert(self, idx):
        self.experts.pop(idx)

    def GetIndexByPattern(self, pattern):
        return next((i for i, item in enumerate(self.experts) if pattern in item.name), -1)