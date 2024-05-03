import sys
import os
import matplotlib.pyplot as plt
import numpy as np
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from DataBase import CreateDataBase
import Model

class QUPC (object):
    def __init__(self, analysis, savePath:str, figName:str, cvTrue:float, cvFalse:float, cvInconsistence:float ,cvParacompletness:float):
        self.analysis = analysis
        self.savePath = savePath
        self.figName = figName
        self.cvTrue = cvTrue
        self.cvFalse = cvFalse
        self.cvInconsistence = cvInconsistence
        self.cvParacompletness = cvParacompletness

    def WriteQUPC(self):
        x = np.array([self.cvParacompletness*2,0,self.cvTrue*2,0,self.cvParacompletness*2])
        y = np.array([0,self.cvInconsistence*2,0,self.cvFalse*2,0])
        plt.plot(x, y, color="black")

        x = np.array([0,0])
        y = np.array([self.cvParacompletness*2,self.cvInconsistence*2])
        plt.plot(x, y, color="red")

        x = np.array([self.cvFalse*2,self.cvTrue*2])
        y = np.array([0,0])
        plt.plot(x, y, color="red")

        x = np.array([0,self.cvTrue])
        y = np.array([0,self.cvFalse])
        plt.plot(x, y, color="blue")

        x = np.array([0,self.cvFalse])
        y = np.array([0,self.cvInconsistence])
        plt.plot(x, y, color="blue")

        x = np.array([0,self.cvTrue])
        y = np.array([0,self.cvInconsistence])
        plt.plot(x, y, color="blue")

        x = np.array([0,self.cvFalse])
        y = np.array([0,self.cvParacompletness])
        plt.plot(x, y, color="blue")

        if self.analysis.decision.gCer < 0:
            alignment = 'left'
        else:
            alignment = 'right'

        plt.plot(self.analysis.decision.gCer, self.analysis.decision.gUnc, 'd', color='green')
        plt.text(self.analysis.decision.gCer, self.analysis.decision.gUnc, self.analysis.decision.lowDefinitionState, horizontalalignment=alignment, weight='bold')

        for factor in self.analysis.results:
            plt.plot(factor.sections[0].resultDegrees.gCer, factor.sections[0].resultDegrees.gUnc, 'o', color='blue')

        plt.xlabel('Unfavorable Evidence Degree')
        plt.ylabel('Favorable Evidence Degree')

        plt.title('QUPC '+self.figName+' Plot')
        plt.grid(True)

        plt.xlim(-1,1)
        plt.ylim(-1,1)

        plt.savefig(os.path.join(self.savePath,"QUPC_"+self.figName+".jpg"))
        plt.clf()

class QUPCLPA2v(QUPC):
    def __init__(self, analysis, savePath:str, figName:str):
        super().__init__(analysis, savePath, figName, analysis.cvTrue, analysis.cvFalse, analysis.cvInconsistence, analysis.cvParacompletness)

class QUPCMPD(QUPC):
    def __init__(self, analysis, savePath:str, figName:str):
        super().__init__(analysis, savePath, figName, analysis.cvTrue, analysis.cvFalse, analysis.cvTrue, analysis.cvFalse)


class ParaAnalyzer (object):
    def __init__(self, dataBase:CreateDataBase):
        self.dataBase = dataBase
        self.maxDataBase = []
        self.minDataBase = []
        self.choosedSections = []
        self.results = []
        self.decision = None

    def SetSections(self, choosedSections:list):
        self.choosedSections = choosedSections

    def Maximization(self):
        for group in self.dataBase.dataBase:
            if len(group.experts) > 1:
                tmpFactors = self.CreateDefaulFactors(group.experts[0].factors)
                
                for expert2 in group.experts:
                    j = 0
                    for factor in expert2.factors:
                        evidenceDegree = Model.EvidenceDegrees()
                        sectionIdx = next((i for i, item in enumerate(factor.sections) if item.name == self.choosedSections[j]), -1)
                        if tmpFactors[j].sections[0].evidenceDegrees.m == 0 or tmpFactors[j].sections[0].evidenceDegrees.m < factor.sections[sectionIdx].evidenceDegrees.m:
                            evidenceDegree.SetMi(factor.sections[sectionIdx].evidenceDegrees.m)
                        else:
                            evidenceDegree.SetMi(tmpFactors[j].sections[0].evidenceDegrees.m)

                        if tmpFactors[j].sections[0].evidenceDegrees.m == 0 or tmpFactors[j].sections[0].evidenceDegrees.l > factor.sections[sectionIdx].evidenceDegrees.l:
                            evidenceDegree.SetLambda(factor.sections[sectionIdx].evidenceDegrees.l)
                        else:
                            evidenceDegree.SetLambda(tmpFactors[j].sections[0].evidenceDegrees.l)

                        tmpFactors[j].sections[0].evidenceDegrees = evidenceDegree
                        j += 1
                expert = group.experts[0]
                expert.SetName(group.name)
                expert.factors = tmpFactors
                group.experts = [expert]
            else:
                expert = group.experts[0]
                expert.SetName(group.name)
                factors = []
                j = 0
                for factor in expert.factors:
                    sectionIdx = next((i for i, item in enumerate(factor.sections) if item.name == self.choosedSections[j]), -1)
                    tmpFactor = factor
                    tmpFactor.sections = [factor.sections[sectionIdx]]
                    factors.append(tmpFactor)
                    j += 1
                expert.factors = factors
                group.experts = [expert]
            self.maxDataBase.append(expert)



    def Minimization(self):
        minimization = self.CreateDefaulFactors(self.maxDataBase[0].factors)
        for expert in self.maxDataBase:
            j = 0
            for factor in expert.factors:
                evidenceDegree = Model.EvidenceDegrees()
                if minimization[j].sections[0].evidenceDegrees.m == 0 or minimization[j].sections[0].evidenceDegrees.m > factor.sections[0].evidenceDegrees.m:
                    evidenceDegree.SetMi(factor.sections[0].evidenceDegrees.m)
                else:
                    evidenceDegree.SetMi(minimization[j].sections[0].evidenceDegrees.m)
                if minimization[j].sections[0].evidenceDegrees.m == 0 or minimization[j].sections[0].evidenceDegrees.l < factor.sections[0].evidenceDegrees.l:
                    evidenceDegree.SetLambda(factor.sections[0].evidenceDegrees.l)
                else:
                    evidenceDegree.SetLambda(minimization[j].sections[0].evidenceDegrees.l)
                minimization[j].sections[0].evidenceDegrees = evidenceDegree
                j += 1
        self.minDataBase = minimization
            
    def CreateDefaulFactors(self, factors:list):
        tmpFactors = []
        j = 0
        for factor in factors:
            evidenceDegree = Model.EvidenceDegrees()
            evidenceDegree.SetMi(0)
            evidenceDegree.SetLambda(0)
            tmpSection = Model.Section()
            tmpSection.SetName(self.choosedSections[j])
            tmpSection.SetEvidenceDegrees(evidenceDegree)
            tmpFactor = Model.Factor()
            tmpFactor.SetName(factor.name)
            tmpFactor.SetWeight(factor.weight)
            tmpFactor.SetSection(tmpSection)
            tmpFactors.append(tmpFactor)
            j += 1
        return tmpFactors

class LPA2v(ParaAnalyzer):
    def __init__(self, dataBase, cvTrue=0.55, cvFalse=-0.55, cvInconsistence=0.55, cvParacompletness=-0.55):
        super().__init__(dataBase)
        self.cvTrue = float(cvTrue)
        self.cvFalse = float(cvFalse)
        self.cvInconsistence = float(cvInconsistence)
        self.cvParacompletness = float(cvParacompletness)

    def CalculateDecision(self, choosedSections:list):
        rGCer = 0
        rGUnc = 0
        weigthSum = 0
        super().SetSections(choosedSections)
        super().Maximization()
        super().Minimization()
        for i in range(len(self.minDataBase)):
            self.results.append(self.minDataBase[i])
            self.results[i].sections[0].resultDegrees = Model.ResultDegrees(self.minDataBase[i].sections[0].evidenceDegrees.m,
                                                                            self.minDataBase[i].sections[0].evidenceDegrees.l)
            self.results[i].sections[0].resultDegrees.SetLowDefinitionState(self.GetLowDefinitionState(self.results[i].sections[0].resultDegrees.gCer,
                                                                                                       self.results[i].sections[0].resultDegrees.gUnc))
            rGCer = rGCer + (self.results[i].sections[0].resultDegrees.gCer * self.results[i].weight)  
            rGUnc = rGUnc + (self.results[i].sections[0].resultDegrees.gUnc * self.results[i].weight)
            weigthSum = weigthSum + self.results[i].weight                                                     
            self.results[i].sections[0].evidenceDegrees = None
        
        self.decision = Model.Decision(rGCer/weigthSum, rGUnc/weigthSum, self.GetLowDefinitionState(rGCer/weigthSum, rGUnc/weigthSum))
    
    def GetLowDefinitionState(self, gCer:float, gUnc:float):
        if gCer >= self.cvTrue:
            return "True"
        elif gCer <= self.cvFalse:
            return "False"
        elif gUnc >= self.cvInconsistence:
            return "Inconsistent"
        elif gUnc <= self.cvParacompletness:
            return "Paracompletness"
        elif (gCer >= 0 and gCer < self.cvTrue) and (gUnc >= 0 and gUnc < self.cvInconsistence):
            if gCer >= gUnc:
                return "Qv -> T"
            else:
                return "QT -> V"
        elif (gCer >= 0 and gCer < self.cvTrue) and (gUnc > self.cvParacompletness and gUnc <= 0):
            if  gCer >= abs(gUnc):
                return "QV -> ^"
            else:
                return "Q^-> V"
        elif (gCer > self.cvFalse and gCer <= 0) and (gUnc > self.cvParacompletness and gUnc <= 0):
            if abs(gCer) >= abs(gUnc):
                return "QF -> ^"
            else:
                return "Q^ -> F"
        elif (gCer > self.cvFalse and gCer <= 0) and (gUnc >= 0 and gUnc < self.cvInconsistence):
            if abs(gCer) >= gUnc:
                return "QF -> T"
            else:
                return "QT -> F"

class MPD(ParaAnalyzer):
    def __init__(self, dataBase, controlValue=0.65):
        super().__init__(dataBase)
        self.cvTrue = float(controlValue)
        self.cvFalse = 0 - float(controlValue)

    def CalculateDecision(self, choosedSections:list):
        rGCer = 0
        rGUnc = 0
        weigthSum = 0
        super().SetSections(choosedSections)
        super().Maximization()
        super().Minimization()
        for i in range(len(self.minDataBase)):
            self.results.append(self.minDataBase[i])
            self.results[i].sections[0].resultDegrees = Model.ResultDegrees(self.minDataBase[i].sections[0].evidenceDegrees.m,
                                                                            self.minDataBase[i].sections[0].evidenceDegrees.l)
            self.results[i].sections[0].resultDegrees.SetLowDefinitionState(self.GetLowDefinitionState(self.results[i].sections[0].resultDegrees.gCer,
                                                                                                       self.results[i].sections[0].resultDegrees.gUnc))
            rGCer = rGCer + (self.results[i].sections[0].resultDegrees.gCer * self.results[i].weight)  
            rGUnc = rGUnc + (self.results[i].sections[0].resultDegrees.gUnc * self.results[i].weight)
            weigthSum = weigthSum + self.results[i].weight                                                     
            self.results[i].sections[0].evidenceDegrees = None
        
        self.decision = Model.Decision(rGCer/weigthSum, rGUnc/weigthSum, self.GetLowDefinitionState(rGCer/weigthSum, rGUnc/weigthSum))
    
    def GetLowDefinitionState(self, gCer:float, gUnc:float):
        if gCer >= self.cvTrue:
            return "True"
        elif gCer <= self.cvFalse:
            return "False"
        elif gCer < self.cvTrue and gCer > self.cvFalse:
            return "Non Conclusive"