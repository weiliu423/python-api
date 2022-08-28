
import pandas as pd
import numpy as np


def KNN(df):  
    df['OSNR(dB)'] = pd.to_numeric(df['OSNR(dB)'])
    df['gOSNR(dB)'] = pd.to_numeric(df['gOSNR(dB)'])
    df = df.fillna(0)
    print(df)

    # Import train_test_split function
    from sklearn.model_selection import train_test_split 
    from sklearn.neighbors import KNeighborsClassifier   
    # Split dataset into training set and test set
    # X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.3) # 70% training and 30% test

    # #Create KNN Classifier
    # knn = KNeighborsClassifier(n_neighbors=5)

    # #Train the model using the training sets
    # knn.fit(X_train, y_train)

    # #Predict the response for test dataset
    # y_pred = knn.predict(X_test)

    #Import scikit-learn metrics module for accuracy calculation
    from sklearn import metrics
    # Model Accuracy, how often is the classifier correct?
    
    # f1 = open(filePath + "osnr_processed.txt", "w")
    # f1.write("Now the file has more content!")
    # print(f.read())
    # f1.close()    
    #print("Accuracy:",metrics.accuracy_score(y_test, y_pred))