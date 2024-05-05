import datetime as dt
import pandas as pd
from sklearn.decomposition import PCA

def RFM(dataframe):
    dataframe['TotalRevenue'] = dataframe['Quantity'] * dataframe['Price']
    dataframe['InvoiceDate'] = pd.to_datetime(dataframe['InvoiceDate'], format="%m/%d/%Y %H:%M")
    maximum = max(dataframe['InvoiceDate'])
    maximum = maximum + pd.DateOffset(days = 1)
    dataframe['Distance'] = maximum - dataframe['InvoiceDate']
    #groupby Customer ID
    mometary = dataframe.groupby("CustomerID").TotalRevenue.sum()
    mometary = mometary.reset_index()

    frequency = dataframe.groupby("CustomerID").InvoiceDate.count()
    frequency = frequency.reset_index()

    recency = dataframe.groupby("CustomerID").Distance.min()
    recency = recency.reset_index()

    RFM = mometary.merge(frequency, on = "CustomerID", how="inner")
    RFM = RFM.merge(recency, on="CustomerID", how="inner")
    RFM.columns = ['CustomerID', 'TotalRevenue', 'Frequency', 'Recency']
    return RFM

def rfm_outlier_proccessing(RFM):
        #Xử lý outlier cho TotalRevenue
    Q1 = RFM['TotalRevenue'].quantile(0.25)
    Q3 = RFM['TotalRevenue'].quantile(0.75)

    IQR = Q3 - Q1
    RFM = RFM[(RFM['TotalRevenue'] >= Q1 - 1.5*IQR) & (RFM['TotalRevenue'] <= Q3 + 1.5*IQR)]

        #Xử lý outlier cho Frequency
    Q1 = RFM['Frequency'].quantile(0.25)
    Q3 = RFM['Frequency'].quantile(0.75)

    IQR = Q3 - Q1
    RFM = RFM[(RFM['Frequency'] >= Q1 - 1.5*IQR) & (RFM['Frequency'] <= Q3 + 1.5*IQR)]    

    #Xử lý outlier cho Recency
    Q1 = RFM['Recency'].quantile(0.25)
    Q3 = RFM['Recency'].quantile(0.75)

    IQR = Q3 - Q1
    RFM = RFM[(RFM['Recency'] >= Q1 - 1.5*IQR) & (RFM['Recency'] <= Q3 + 1.5*IQR)]                                         
    return RFM

def pca_transform(dataframe):

  pca = PCA(n_components=3, random_state=42)  # Create PCA object with 3 components

  # Fit the PCA model to the data
  pca_fit = pca.fit(dataframe)

  # Extract the transformed data using the correct method
  pca_data = pca_fit.transform(dataframe)

  # Create the DataFrame with appropriate column names
  pca_ds = pd.DataFrame(pca_data, columns=['PC1', 'PC2', 'PC3'])

  return pca_ds

