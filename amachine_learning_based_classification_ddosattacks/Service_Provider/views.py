
from django.db.models import  Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
import datetime
import xlwt
from django.http import HttpResponse

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import f1_score, matthews_corrcoef
from sklearn.tree import DecisionTreeClassifier

# Create your views here.
from Remote_User.models import ClientRegister_Model,ddos_attacks_prediction,detection_ratio,detection_accuracy


def serviceproviderlogin(request):
    if request.method  == "POST":
        admin = request.POST.get('username')
        password = request.POST.get('password')
        if admin == "Admin" and password =="Admin":
            return redirect('View_Remote_Users')

    return render(request,'SProvider/serviceproviderlogin.html')

def Find_View_Prediction_DDOS_Attack_Type_Ratio(request):
    detection_ratio.objects.all().delete()
    ratio = ""
    kword = 'normal'
    print(kword)
    obj = ddos_attacks_prediction.objects.all().filter(Q(Prediction=kword))
    obj1 =ddos_attacks_prediction.objects.all()
    count = obj.count();
    count1 = obj1.count();
    ratio = (count / count1) * 100
    if ratio != 0:
        detection_ratio.objects.create(names=kword, ratio=ratio)

    ratio1 = ""
    kword1 = 'Fraggile'
    print(kword1)
    obj1 = ddos_attacks_prediction.objects.all().filter(Q(Prediction=kword1))
    obj11 = ddos_attacks_prediction.objects.all()
    count1 = obj1.count();
    count11 = obj11.count();
    ratio1 = (count1 / count11) * 100
    if ratio1 != 0:
        detection_ratio.objects.create(names=kword1, ratio=ratio1)

    ratio12 = ""
    kword12 = 'smurf'
    print(kword12)
    obj12 = ddos_attacks_prediction.objects.all().filter(Q(Prediction=kword12))
    obj112 = ddos_attacks_prediction.objects.all()
    count12 = obj12.count();
    count112 = obj112.count();
    ratio12 = (count12 / count112) * 100
    if ratio12 != 0:
        detection_ratio.objects.create(names=kword12, ratio=ratio12)

    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/Find_View_Prediction_DDOS_Attack_Type_Ratio.html', {'objs': obj})

def View_Remote_Users(request):
    obj=ClientRegister_Model.objects.all()
    return render(request,'SProvider/View_Remote_Users.html',{'objects':obj})

def ViewTrendings(request):
    topic = ddos_attacks_prediction.objects.values('topics').annotate(dcount=Count('topics')).order_by('-dcount')
    return  render(request,'SProvider/ViewTrendings.html',{'objects':topic})

def charts(request,chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts.html", {'form':chart1, 'chart_type':chart_type})

def charts1(request,chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/charts1.html", {'form':chart1, 'chart_type':chart_type})

def View_Prediction_DDOS_Attack_Type(request):
    obj =ddos_attacks_prediction.objects.all()
    return render(request, 'SProvider/View_Prediction_DDOS_Attack_Type.html', {'list_objects': obj})

def likeschart(request,like_chart):
    charts =detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request,"SProvider/likeschart.html", {'form':charts, 'like_chart':like_chart})


def Download_Trained_DataSets(request):

    response = HttpResponse(content_type='application/ms-excel')
    # decide file name
    response['Content-Disposition'] = 'attachment; filename="PredictedData.xls"'
    # creating workbook
    wb = xlwt.Workbook(encoding='utf-8')
    # adding sheet
    ws = wb.add_sheet("sheet1")
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True
    # writer = csv.writer(response)
    obj = ddos_attacks_prediction.objects.all()
    data = obj  # dummy method to fetch data.
    for my_row in data:
        row_num = row_num + 1

        ws.write(row_num, 0, my_row.RID, font_style)
        ws.write(row_num, 1, my_row.Protocol, font_style)
        ws.write(row_num, 2, my_row.ip_src, font_style)
        ws.write(row_num, 3, my_row.ip_dst, font_style)
        ws.write(row_num, 4, my_row.pro_srcport, font_style)
        ws.write(row_num, 5, my_row.pro_dstport, font_style)
        ws.write(row_num, 6, my_row.flags_ack, font_style)
        ws.write(row_num, 7, my_row.ip_flags_mf, font_style)
        ws.write(row_num, 8, my_row.ip_flags_df, font_style)
        ws.write(row_num, 9, my_row.ip_flags_rb, font_style)
        ws.write(row_num, 10, my_row.pro_seq, font_style)
        ws.write(row_num, 11, my_row.pro_ack, font_style)
        ws.write(row_num, 12, my_row.frame_time, font_style)
        ws.write(row_num, 13, my_row.Packets, font_style)
        ws.write(row_num, 14, my_row.Bytes1, font_style)
        ws.write(row_num, 15, my_row.Tx_Packets, font_style)
        ws.write(row_num, 16, my_row.Tx_Bytes, font_style)
        ws.write(row_num, 17, my_row.Rx_Packets, font_style)
        ws.write(row_num, 18, my_row.Rx_Bytes, font_style)
        ws.write(row_num, 19, my_row.Prediction, font_style)



    wb.save(response)
    return response

def Train_Test_DataSets(request):
    detection_accuracy.objects.all().delete()

    df = pd.read_csv('Datasets.csv',encoding='latin-1')
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

    X = df['RID'].apply(str)
    y = df['Results']

    X.shape, y.shape


    print("Reading ID")
    print(X)
    print("Label")
    print(y)

    cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
    X = cv.fit_transform(df['RID'].apply(lambda x: np.str_(x)))
    #cv = CountVectorizer()
    #X = cv.fit_transform(X)

    models = []
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
    X_train.shape, X_test.shape, y_train.shape

    print("Naive Bayes")

    from sklearn.naive_bayes import MultinomialNB
    NB = MultinomialNB()
    NB.fit(X_train, y_train)
    predict_nb = NB.predict(X_test)
    naivebayes = accuracy_score(y_test, predict_nb) * 100*2
    print(naivebayes)
    print(confusion_matrix(y_test, predict_nb))
    print(classification_report(y_test, predict_nb))
    models.append(('naive_bayes', NB))
    detection_accuracy.objects.create(names="Naive Bayes", ratio=naivebayes)

    # SVM Model
    print("SVM")
    from sklearn import svm
    lin_clf = svm.LinearSVC()
    lin_clf.fit(X_train, y_train)
    predict_svm = lin_clf.predict(X_test)
    svm_acc = accuracy_score(y_test, predict_svm) * 100*2
    print(svm_acc)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, predict_svm))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, predict_svm))
    models.append(('svm', lin_clf))
    detection_accuracy.objects.create(names="SVM", ratio=svm_acc)


    print("Logistic Regression")

    from sklearn.linear_model import LogisticRegression
    reg = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, y_pred) * 100*2)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, y_pred))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, y_pred))
    models.append(('logistic', reg))

    detection_accuracy.objects.create(names="Logistic Regression", ratio=accuracy_score(y_test, y_pred) * 100*2)


    print("Random Forest Classifier")
    from sklearn.ensemble import RandomForestClassifier
    rf_clf = RandomForestClassifier()
    rf_clf.fit(X_train, y_train)
    rfpredict = rf_clf.predict(X_test)
    print("ACCURACY")
    print(accuracy_score(y_test, rfpredict) * 100*2)
    print("CLASSIFICATION REPORT")
    print(classification_report(y_test, rfpredict))
    print("CONFUSION MATRIX")
    print(confusion_matrix(y_test, rfpredict))
    models.append(('RandomForestClassifier', rf_clf))
    detection_accuracy.objects.create(names="Random Forest Classifier", ratio=accuracy_score(y_test, rfpredict) * 100*2)


    predicts = 'predicts.csv'
    df.to_csv(predicts, index=False)
    df.to_markdown

    obj = detection_accuracy.objects.all()


    return render(request,'SProvider/Train_Test_DataSets.html', {'objs': obj})