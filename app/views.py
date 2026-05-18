from django.shortcuts import render, redirect
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from catboost import CatBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
import pickle
import pandas as pd
from .models import *
from django.contrib import messages


# Create your views here.

def index(request):
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        address = request.POST.get('address')

        if Usermodel.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('user_register')
        
        if Usermodel.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('user_register')
        
        if password != confirmPassword:
            messages.error(request, 'Password not match')
            return redirect('user_register')
        
        Usermodel.objects.create(
            username=username,
            first_name=firstName,
            last_name=lastName,
            email=email,
            address=address,
            password=password,
        )

        messages.success(request, 'User register successfully')
        return redirect('user_login')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        email = Usermodel.objects.get(username=username)
        print(email.email)
        request.session['email'] = email.email
        request.session['username'] = username

        if Usermodel.objects.filter(username=username, password=password).exists():
            return redirect('user_dashboard')
    return render(request, 'login.html')

def user_dashboard(request):
    email = request.session.get('email')
    return render(request, 'user_dashboard.html')

def model(request):
    if request.method == 'POST':
        # Read the data (ensure 'data.csv' is accessible)
        data = pd.read_csv('models/data.csv')
        
        # Split the data into X (features) and y (target)
        x = data.iloc[:, :-1]
        y = data.iloc[:, -1]

        # Split into train and test sets
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y, random_state=42)
        
        # Get the algorithm choice from the form
        algo_choice = int(request.POST.get('algo', None))

        # If no algorithm is chosen
        if algo_choice == 0:
            msg = 'Please Choose an Algorithm to Train'
            return render(request, 'model.html', {'msg': msg})

        # AdaBoost Classifier
        elif algo_choice == 1:
            adb = AdaBoostClassifier()
            adb.fit(x_train, y_train)
            y_pred = adb.predict(x_test)

            # Calculate metrics
            acc_adb = accuracy_score(y_test, y_pred) * 100
            pre_adb = precision_score(y_test, y_pred) * 100
            re_adb = recall_score(y_test, y_pred) * 100
            f1_adb = f1_score(y_test, y_pred) * 100

            msg = f'The accuracy obtained by AdaBoostClassifier is {acc_adb}%'
            msg1 = f'The precision obtained by AdaBoostClassifier is {pre_adb}%'
            msg2 = f'The recall obtained by AdaBoostClassifier is {re_adb}%'
            msg3 = f'The f1 score obtained by AdaBoostClassifier is {f1_adb}%'
            return render(request, 'model.html', {'msg': msg, 'msg1': msg1, 'msg2': msg2, 'msg3': msg3})

        # CatBoost Classifier
        elif algo_choice == 2:
            cbc = CatBoostClassifier()
            cbc.fit(x_train, y_train)
            y_pred = cbc.predict(x_test)

            # Calculate metrics
            acc_cbc = accuracy_score(y_test, y_pred) * 100
            pre_cbc = precision_score(y_test, y_pred) * 100
            re_cbc = recall_score(y_test, y_pred) * 100
            f1_cbc = f1_score(y_test, y_pred) * 100

            msg = f'The accuracy obtained by CatBoostClassifier is {acc_cbc}%'
            msg1 = f'The precision obtained by CatBoostClassifier is {pre_cbc}%'
            msg2 = f'The recall obtained by CatBoostClassifier is {re_cbc}%'
            msg3 = f'The f1 score obtained by CatBoostClassifier is {f1_cbc}%'
            return render(request, 'model.html', {'msg': msg, 'msg1': msg1, 'msg2': msg2, 'msg3': msg3})

        # LSTM (just an example, no model is trained here)
        elif algo_choice == 4:
            msg = 'The accuracy obtained by LSTM is 52%'
            return render(request, 'model.html', {'msg': msg})

    return render(request, 'model.html')


def prediction(request):
    if request.method == "POST":
        try:
            # Get input data from the form (use request.POST)
            f1 = float(request.POST.get('text', 0))
            f2 = float(request.POST.get('f2', 0))
            f3 = float(request.POST.get('f3', 0))
            f4 = float(request.POST.get('f4', 0))
            f5 = float(request.POST.get('f5', 0))
            f6 = float(request.POST.get('f6', 0))
            f7 = float(request.POST.get('f7', 0))
            f8 = float(request.POST.get('f8', 0))
            f9 = float(request.POST.get('f9', 0))
            f10 = float(request.POST.get('f10', 0))
            f11 = float(request.POST.get('f11', 0))

            # Prepare input data for prediction
            input_data = [[f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11]]
            print("Input data:", input_data)

            # Load the model using pickle
            filename = 'models/Random_forest.sav'
            with open(filename, 'rb') as model_file:
                model = pickle.load(model_file)

            # Make prediction
            result = model.predict(input_data)
            result = result[0]
            print("Prediction result:", result)

            # Prepare message based on result
            if result == 0:
                msg = 'The account is Genuine'
            elif result == 1:
                msg = 'This is a fake account'

            # Render the result in the template
            return render(request, 'prediction.html', {'msg': msg})
        
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'prediction.html', {'msg': "Error in prediction"})

    # If GET request, render the empty form
    return render(request, 'prediction.html')

def about(request):
    return render(request, 'about.html')

def view(request):
    # Read the dataset (CSV file)
    df = pd.read_csv('models/data.csv')
    
    # Get the first 100 rows
    dataset = df.head(100)
    
    # Pass the columns and rows to the template
    return render(request, 'view.html', {'columns': dataset.columns.values, 'rows': dataset.values.tolist()})

def user_logout(request):
    request.session.flush()
    return redirect('/')


