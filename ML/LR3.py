 
import pandas as pd


def doML(inputData):
   # try:

      data=pd.read_csv(r'Toddler_dataset.csv')

      #data.head()

      #data.info()

      #data.isnull().any()

      #delete non contributing columns
      data.drop('Case_No',axis=1,inplace=True)
      data.drop('Qchat-10-Score',axis=1,inplace=True)
      data.drop('Who completed the test',axis=1,inplace=True)
      # data.drop('A8',axis=1,inplace=True)
      data.rename(columns={"Age_Mons":"Age_Month","Class/ASD Traits ": "Class/ASD"},inplace=True)




      #data.isnull().sum()

      m=(data.dtypes=='object')

      object_cols=list(m[m].index)

      #object_cols

      #print('unique Values',data['Sex'].unique())

      #print('unique Values',data['Ethnicity'].unique())

      #print('unique Values',data['Jaundice'].unique())

      #print('unique Values',data['Family_mem_with_ASD'].unique())

      #print('unique Values',data['Class/ASD'].unique())



      from sklearn.preprocessing import LabelEncoder,OneHotEncoder


      #-----------------------oneHotEncoding-------


      object_cols=['Ethnicity']

      oh_encoder=OneHotEncoder(handle_unknown='ignore',sparse_output=False)


      oh_data=pd.DataFrame(oh_encoder.fit_transform(data[object_cols].values))

      


      

      oh_test = oh_encoder.transform([[inputData[-1]]])

      oh_test = oh_test.ravel()

      oh_test = list(map(int, oh_test))

      inputData = inputData[:-1]

      inputData.extend(oh_test)




      oh_new=data.drop(object_cols,axis=1)

      oh_train=pd.concat([oh_new,oh_data],axis=1)


      y=oh_train['Class/ASD']

      x_old=oh_train.drop('Class/ASD',axis=1)

      #x.info()


      #-----------------------label Encoding-------------------



      lb_encoder=LabelEncoder()

      y=lb_encoder.fit_transform(y)

      

      feature_names=['Sex','Jaundice','Family_mem_with_ASD']

      x_data=pd.DataFrame(oh_train[feature_names])

      for col in x_data:
         x_data[col]=lb_encoder.fit_transform(x_data[col])



      #oh_train.info()

      del_oh_train=x_old.drop(['Sex','Jaundice','Family_mem_with_ASD'],axis=1)
      # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
      #    print(del_oh_train)

      # print(del_oh_train)

      x_old=pd.concat([del_oh_train,x_data],axis=1)

      #x.info()

      #x.info()

      #x_old.info()

      #----------------train/test split---------------

      x=x_old.iloc[:,:].values


      from sklearn.model_selection import train_test_split



      x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.4,random_state=42)



      #----------------------Normalization--------------
      from sklearn.preprocessing import StandardScaler

      sc=StandardScaler()

      x_train=sc.fit_transform(x_train)

      x_test=sc.transform(x_test)



      #--------------Analyising------------------

      # test-size=.262

      from sklearn.linear_model import LogisticRegression

      model=LogisticRegression()

      model.fit(x_train,y_train)

      y_predict_LR=model.predict(x_test)
      



      from sklearn.tree import DecisionTreeClassifier

      dt_model=DecisionTreeClassifier(criterion='entropy',random_state=0)

      dt_model.fit(x_train,y_train)

      y_predict_DT=dt_model.predict(x_test)


      from sklearn.metrics import accuracy_score,confusion_matrix


      accuracy_LR=accuracy_score(y_test, y_predict_LR)

      conf_LR=confusion_matrix(y_test, y_predict_LR)

      accuracy_DT=accuracy_score(y_test, y_predict_DT)

      conf_DT=confusion_matrix(y_test, y_predict_DT)

      #print(accuracy_LR)

      #print(conf_LR)

      #print(accuracy_DT)

      #print(conf_DT)




      #----------------------------------------------------
   #  [1, 1, 1, 1, 1, 1, 1,0,0,0,28,0,0,0,0,1,0,0,0,0,0,0,1,1,1]
      #x_old.info()inputData
      new_data_sample = [inputData]


      new_data_sample_scaled = sc.transform(new_data_sample)

      # Predict the class/ASD for the new data
      new_data_sample_pred = dt_model.predict(new_data_sample_scaled)

      # Convert the predicted value back to its original label
      new_data_sample_pred_label = lb_encoder.inverse_transform(new_data_sample_pred)

      # Print the predicted class/ASD value

      # print('\n****************************************************\n')
      # print("Predicted Class/ASD for the new data sample:")

      #print(new_data_sample_pred_label[0])

#resuuuuuuuuuuuuuuuuuuuuuuult
      # print(new_data_sample_pred_label)

      return new_data_sample_pred_label[0]

      print('\n****************************************************\n')
      print('Accuracy_Score using Decission Tree is:\n\n%.2f'
         %( accuracy_LR *100),'%')

      print('\n****************************************************\n')


      #df=pd.DataFrame(data['Class/ASD'])


      #df2=pd.DataFrame(y_test)

      #df['Class/ASD'].value_counts()

      #df2[0].value_counts()

      #print(conf_LR)


   # except Exception as e:
   #             return{"Error33:", e}
               

















