import pandas as pd

baseDirectory = "D:\\Users\\Shane\\SkyDrive\\Documents\\Trading\\Research\\Data\\"
riskZInputFile = baseDirectory + "RiskZ\\" + "VIX.csv"


def getRiskZ():
    global RiskZDF
    RiskZDF = pd.read_csv(riskZInputFile)
