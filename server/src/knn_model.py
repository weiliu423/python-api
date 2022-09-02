
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
def KNN(df):  
    #Data Pre-Processing
    jsonData = json.loads(df)
    sig = pd.json_normalize(jsonData)
    sig.loc[sig['direction'] == 'Input', 'direction'] = 0
    sig.loc[sig['direction'] == 'Output', 'direction'] = 1
    sig.loc[sig['Channel'] == 'ch1:191.35THz', 'Channel'] = 1
    sig.loc[sig['Channel'] == 'ch2:191.40THz', 'Channel'] = 2
    sig.loc[sig['Channel'] == 'ch3:191.45THz', 'Channel'] = 3
    sig.loc[sig['Channel'] == 'ch4:191.50THz', 'Channel'] = 4
    sig.loc[sig['Channel'] == 'ch5:191.55THz', 'Channel'] = 5
    sig['Channel'] = pd.to_numeric(sig['Channel'])
    sig['direction'] = pd.to_numeric(sig['direction'])
    sig['ase_noise'] = pd.to_numeric(sig['ase_noise'])
    sig['nli_noise'] = pd.to_numeric(sig['nli_noise'])
    sig = sig.drop(['link'], axis=1)
    x = sig.drop(['Channel'], axis=1)
    y = sig.drop(['power', 'direction', 'ase_noise', 'nli_noise'], axis=1)
    y = y.iloc[:,0]

    #KNN Model
    from sklearn.preprocessing import MinMaxScaler
    x_data = MinMaxScaler().fit_transform(x)
    data = pd.DataFrame(x_data)
    # Import train_test_split function
    from sklearn.model_selection import train_test_split 
    from sklearn.neighbors import KNeighborsClassifier   
    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(data, y, test_size=0.3, random_state=12) # 70% training and 30% test

    #Import scikit-learn metrics module for accuracy calculation
    from sklearn import metrics
    accuracies = []
    for k in range(1,11):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        accuracies.append(['K = ' + str(k), 'Accuracy = ' + str(metrics.accuracy_score(y_test, y_pred) * 100)])
    # Plot the results s
    # fig, ax = plt.subplots(figsize=(10,5))
    # ax.plot(range(1,11), accuracies[1])
    # ax.set_xlabel('Nearest Neighbors Classification (k)')
    # ax.set_ylabel('Accuracy (%)')
    # plt.show()
    return accuracies