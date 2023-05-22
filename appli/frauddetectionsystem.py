import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
# from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
import pickle


def load_and_use_pickled_model(account_number, cvv, customer_age, gender, marital_status, card_colour, card_type,
                              domain, amount, average_income_expenditure, customer_city_address
                              ):

    
    # Load the data
    data = pd.DataFrame([{
        "AcountNumber": account_number,
        "CVV": cvv,
        "CustomerAge": customer_age,
        "Gender": gender,
        "Marital Status": marital_status,
        "CardColour": card_colour,
        "CardType": card_type,
        "Domain": domain,
        "Amount": amount,
        "AverageIncomeExpendicture": average_income_expenditure,
        "Customer_City_Address": customer_city_address
    }])


    
    X = data

    # Load the pickled model
    with open("./frauddetectionmodel.pkl", "rb") as file:
        fraudmodel = pickle.load(file)
        
    with open("./kmeansmodel.pkl", "rb") as file:
        kmeansmodel = pickle.load(file)
        
        
    # Load the scaler object
    with open("./scaler.pkl", "rb") as file:
        scaler = pickle.load(file)
        
        
    # Scale numerical features
    numerical_features = ["AcountNumber", "CVV", "CustomerAge", "Amount", "AverageIncomeExpendicture"]
    X[numerical_features] = scaler.transform(X[numerical_features])


    # Load the encoder object
    with open('./CardColour_encoder.pkl', "rb") as file:
        cardencoder = pickle.load(file)

    # Transform the features using the encoder
    X["CardColour"] = cardencoder.transform(X["CardColour"])
    
    
    
    with open('./CardType_encoder.pkl', "rb") as file:
        cardtypeencoder = pickle.load(file)

    # Transform the features using the encoder
    X["CardType"] = cardtypeencoder.transform(X["CardType"])
    
    
    with open('./Customer_City_Address_encoder.pkl', "rb") as file:
        citytypeencoder = pickle.load(file)

    # Transform the features using the encoder
    X["Customer_City_Address"] = citytypeencoder.transform(X["Customer_City_Address"])


    with open('./Domain_encoder.pkl', "rb") as file:
        domaintypeencoder = pickle.load(file)

    # Transform the features using the encoder
    X["Domain"] = domaintypeencoder.transform(X["Domain"])
    
    
    with open('./Gender_encoder.pkl', "rb") as file:
        genderencoder = pickle.load(file)

    # Transform the features using the encoder
    X["Gender"] = genderencoder.transform(X["Gender"])
    
    
    with open('./Marital Status_encoder.pkl', "rb") as file:
        maritalencoder = pickle.load(file)

    # Transform the features using the encoder
    X["Marital Status"] = maritalencoder.transform(X["Marital Status"])


    # Predict clusters for new data
    pred = kmeansmodel.predict(X)
    print("pred value",pred)
    
    # Add the cluster labels as a new feature
    X["cluster_label"] = pred
    
    # Make predictions on the test set
    predictions = fraudmodel.predict(X)
    print("The prediction is ", predictions)
    print("The prediction is ", type(predictions))
    predictions = int(predictions)
    print("The prediction type now is ", type(predictions))
    print('predictions', predictions)
    return predictions

 


























    # Scale numerical features
    # numerical_features = ["AcountNumber", "CVV", "CustomerAge", "Amount", "AverageIncomeExpendicture"]
    # scaler = StandardScaler()
    # X[numerical_features] = scaler.fit_transform(X[numerical_features])

    # # Encode categorical variables
    # categorical_features = ["Gender", "Marital Status", "CardColour", "CardType", "Domain", "Customer_City_Address"]
    # for feature in categorical_features:
    #     encoder = LabelEncoder()
    #     X[feature] = encoder.fit_transform(X[feature])

    # # Perform K-means clustering
    # kmeans = KMeans(n_clusters=3, random_state=)  # Set the desired number of clusters and random state
    # kmeans.fit(X)

    # # Add the cluster labels as a new feature
    # X["cluster_label"] = kmeans.labels_

    # # Split the data into training and testing sets
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

    # # Train the Random Forest model
    # rf_model = RandomForestClassifier(random_state=random_state)
    # rf_model.fit(X_train, y_train)

    # # Make predictions on the test set
    # y_pred = rf_model.predict(X_test)

    # # Make predictions using the pickled model
    # predictions = rf_model.predict(features)
    # print(predictions)









    # Load the encoder object
    # with open(encoder_file, "rb") as file:
    #     encoder = pickle.load(file)

    # # Transform the features using the encoder
    # transformed_features = encoder.transform(features)

    # return transformed_features




    # Load the scaler object
    # with open(scaler_file, "rb") as file:
    #     scaler = pickle.load(file)

    # # Transform the data using the scaler
    # transformed_data = scaler.transform(data)

    # return transformed_data