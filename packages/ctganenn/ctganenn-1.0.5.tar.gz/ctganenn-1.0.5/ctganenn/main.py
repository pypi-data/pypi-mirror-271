from imblearn.under_sampling import EditedNearestNeighbours
from ctgan import CTGAN
import pandas as pd

def CTGANENN(minClass,majClass,genData,targetLabel):
    batch_size = 5000
    epochs = 100
    model = CTGAN(batch_size=batch_size, epochs=epochs, verbose=True)
    model.fit(minClass)
    n_generated_data = genData
    generated_df = model.sample(n_generated_data)

    #concat original data and gan data
    data_concat = pd.concat([minClass, generated_df])
    # combine data churn and not churn
    data=pd.concat([majClass, data_concat])
    enn = EditedNearestNeighbours(n_neighbors=3)
    X=data.drop([targetLabel],axis=1)
    y=data[targetLabel]
    X, y = enn.fit_resample(X, y)

    return X,y
