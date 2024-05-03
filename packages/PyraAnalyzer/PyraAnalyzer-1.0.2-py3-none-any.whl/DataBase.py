import sys
import os
import csv
import numpy as np
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
import Model

class CreateDataBase (object):
    def __init__(self, name:str):
        self.dataBase = []
        self.name = name

    def ReadDataBaseFromCSV(self, databasePath:str, delimiter:str):
        try:
            readedCsv = csv.reader(open(databasePath),delimiter=delimiter)
            groupExpertHeader = []
            groupExpertHeader.append(next(readedCsv))
            groupExpertHeader.append(next(readedCsv))
            groupExpertHeader = list(np.unique(np.array(list(zip(*groupExpertHeader))), axis=0))

            header = list(next(readedCsv))

            allEvidenceDegrees = [] 
            for line in readedCsv:
                allEvidenceDegrees.append(line)

            for line in groupExpertHeader:
                if not ('' == line[0]):
                    index = next((i for i, item in enumerate(self.dataBase) if item.name == line[0]), -1)
                    if index >= 0:
                        expert = Model.Expert()
                        expert.SetName(line[1])
                        for line2 in allEvidenceDegrees:
                            evidenceDegreesIdx = [header.index(i) for i in header if expert.name[len(expert.name)-1] in i]
                            evidenceDegree = Model.EvidenceDegrees()
                            evidenceDegree.SetMi(float(line2[evidenceDegreesIdx[0]]))
                            evidenceDegree.SetLambda(float(line2[evidenceDegreesIdx[1]]))
                            section = Model.Section()
                            section.SetName(line2[1])
                            section.SetEvidenceDegrees(evidenceDegree)
                
                            factorIdx = next((i for i, item in enumerate(expert.factors) if item.name == line2[0]), -1)

                            if factorIdx >= 0:
                                expert.factors[factorIdx].SetSection(section)
                            else:
                                factor = Model.Factor()
                                factor.SetName(line2[0])
                                factor.SetWeight(line2[2])
                                factor.SetSection(section)
                                expert.SetFactor(factor)

                        self.dataBase[index].SetExpert(expert)
                    else:
                        group = Model.Group()
                        group.SetName(line[0])
                        expert = Model.Expert()
                        expert.SetName(line[1])
                        for line2 in allEvidenceDegrees:
                            evidenceDegreesIdx = [header.index(i) for i in header if expert.name[len(expert.name)-1] in i]
                            evidenceDegree = Model.EvidenceDegrees()
                            evidenceDegree.SetMi(float(line2[evidenceDegreesIdx[0]]))
                            evidenceDegree.SetLambda(float(line2[evidenceDegreesIdx[1]]))
                            section = Model.Section()
                            section.SetName(line2[1])
                            section.SetEvidenceDegrees(evidenceDegree)
                
                            factorIdx = next((i for i, item in enumerate(expert.factors) if item.name == line2[0]), -1)

                            if factorIdx >= 0:
                                expert.factors[factorIdx].SetSection(section)
                            else:
                                factor = Model.Factor()
                                factor.SetName(line2[0])
                                factor.SetWeight(line2[2])
                                factor.SetSection(section)
                                expert.SetFactor(factor)

                        group.SetExpert(expert)
                        self.dataBase.append(group)
        except:
            print("LPAlib its unable to open this data base.")



        
