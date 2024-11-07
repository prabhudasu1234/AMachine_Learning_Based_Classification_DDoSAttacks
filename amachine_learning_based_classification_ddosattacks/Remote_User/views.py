from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import openpyxl

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
import warnings
warnings.filterwarnings("ignore")
plt.style.use('ggplot')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

# Create your views here.
from Remote_User.models import ClientRegister_Model,ddos_attacks_prediction,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def predict_ddos_attack_type(request):
    if request.method == "POST":

        RID= request.POST.get('RID')
        Protocol= request.POST.get('Protocol')
        ip_src= request.POST.get('ip_src')
        ip_dst= request.POST.get('ip_dst')
        pro_srcport= request.POST.get('pro_srcport')
        pro_dstport= request.POST.get('pro_dstport')
        flags_ack= request.POST.get('flags_ack')
        ip_flags_mf= request.POST.get('ip_flags_mf')
        ip_flags_df= request.POST.get('ip_flags_df')
        ip_flags_rb= request.POST.get('ip_flags_rb')
        pro_seq= request.POST.get('pro_seq')
        pro_ack= request.POST.get('pro_ack')
        frame_time= request.POST.get('frame_time')
        Packets= request.POST.get('Packets')
        Bytes1= request.POST.get('Bytes1')
        Tx_Packets= request.POST.get('Tx_Packets')
        Tx_Bytes= request.POST.get('Tx_Bytes')
        Rx_Packets= request.POST.get('Rx_Packets')
        Rx_Bytes= request.POST.get('Rx_Bytes')




        df = pd.read_csv('Datasets.csv', encoding='latin-1')
        df
        df.columns

        def apply_results(results):
            if (results == "normal"):
                return 0
            elif (results == "smurf"):
                return 1
            elif (results == "Fraggile"):
                return 2

        df['Results'] = df['Label'].apply(apply_results)

        X = df['RID']
        y = df['Results']

        print("Reading ID")
        print(X)
        print("Label")
        print(y)

        # cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
        # X = cv.fit_transform(df['RID'].apply(lambda x: np.str_(x)))
        cv = CountVectorizer()
        X = cv.fit_transform(X)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Naive Bayes")

        from sklearn.naive_bayes import MultinomialNB
        NB = MultinomialNB()
        NB.fit(X_train, y_train)
        predict_nb = NB.predict(X_test)
        naivebayes = accuracy_score(y_test, predict_nb) * 100
        print(naivebayes)
        print(confusion_matrix(y_test, predict_nb))
        print(classification_report(y_test, predict_nb))
        models.append(('naive_bayes', NB))

        # SVM Model
        print("SVM")
        from sklearn import svm
        lin_clf = svm.LinearSVC()
        lin_clf.fit(X_train, y_train)
        predict_svm = lin_clf.predict(X_test)
        svm_acc = accuracy_score(y_test, predict_svm) * 100
        print(svm_acc)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, predict_svm))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, predict_svm))
        models.append(('svm', lin_clf))

        print("Logistic Regression")

        from sklearn.linear_model import LogisticRegression
        reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
        y_pred = reg.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('logistic', reg))



        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        RID1 = [RID]
        vector1 = cv.transform(RID1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if prediction == 0:
            val = 'Normal'
        elif prediction == 1:
            val = 'smurf'
        elif prediction == 2:
            val = 'Fraggile'



        print(val)
        print(pred1)

        ddos_attacks_prediction.objects.create(
        RID=RID,
        Protocol=Protocol,
        ip_src=ip_src,
        ip_dst=ip_dst,
        pro_srcport=pro_srcport,
        pro_dstport=pro_dstport,
        flags_ack=flags_ack,
        ip_flags_mf=ip_flags_mf,
        ip_flags_df=ip_flags_df,
        ip_flags_rb=ip_flags_rb,
        pro_seq=pro_seq,
        pro_ack=pro_ack,
        frame_time=frame_time,
        Packets=Packets,
        Bytes1=Bytes1,
        Tx_Packets=Tx_Packets,
        Tx_Bytes=Tx_Bytes,
        Rx_Packets=Rx_Packets,
        Rx_Bytes=Rx_Bytes,
       Prediction=val)

        return render(request, 'RUser/predict_ddos_attack_type.html',{'objs': val})
    return render(request, 'RUser/predict_ddos_attack_type.html')



