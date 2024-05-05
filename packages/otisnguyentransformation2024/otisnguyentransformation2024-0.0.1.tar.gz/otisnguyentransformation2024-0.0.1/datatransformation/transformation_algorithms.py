from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler
import pandas as pd

def scaler_transform(csv_trans):
    scaler = StandardScaler()
    csv_trans = scaler.fit_transform(csv_trans)
    return csv_trans
    