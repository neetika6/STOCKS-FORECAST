import quandl
import numpy as np
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
def model1(v,days):
    quandl.ApiConfig.api_key = "XzzQF2Kt35td1ptA5dFA"
    df=quandl.get("WIKI/"+v)
    df=df[["Adj. Close"]]
    forecast_out=60
    df["Prediction"]=df[["Adj. Close"]].shift(-forecast_out)
    X=np.array(df.drop(["Prediction"],1))
    X= X[:-forecast_out]
    y=np.array(df["Prediction"])
    y=y[:-forecast_out]
    #split the data into 90% training and 10% testing
    x_train,x_test,y_train, y_test=train_test_split(X,y, test_size=0.1)
    #create and train the support vector machine(Regressor)
    svr_rbf=SVR(kernel="rbf",C=1e3, gamma=0.1)
    svr_rbf.fit(x_train, y_train)
    #test Model:
    model1.svm_confidence=svr_rbf.score(x_test,y_test)
    #create and train the linear regression model
    #set x_forecast equal to the last 60 rows of the original data set from Adj.Close column
    x_forecast=np.array(df.drop(["Prediction"],1))
    #print the prictions for the next n days

    svm_prediction=svr_rbf.predict(x_forecast[-int(days):])
    return svm_prediction
