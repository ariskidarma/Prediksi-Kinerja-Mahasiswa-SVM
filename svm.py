# import Dependencies
import pandas as pd
import numpy as np

from collections import Counter

from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from imblearn.over_sampling import ADASYN

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import accuracy_score

class SVM():
    def __init__(self, C=100, kernel="rbf", gamma="auto", learning_rate=1e-4,random_state=101):
        self.C = C
        self.learning_rate = learning_rate
        self.random_state = random_state
        
        # Kernel trick
        kernel_list = ['linear', 'rbf', 'poly', 'sigmoid']
        if kernel in kernel_list:
            self.kernel = kernel
        else:
            print(f"Warning! There is no kernel '{kernel}'. Switching to default: RBF")
            self.kernel = 'rbf'
            
        # Gamma - koefisien kernel untuk rbf, poly, dan sigmoid
        if gamma == "auto":
            self.gamma = self.gamma_auto
        elif gamma == "scale":
            self.gamma = self.gamma_scale
        
        # Set polynomial degree
        self.degree_poly = 3
        # Koefisien / konstanta untuk kernel polynomial dan sigmoid
        self.coef0 = 0

    # Fungsi create_labelset, untuk membuat labelset
    # yang terdiri dari 3 jenis label latih untuk metode one vs rest
    def create_labelset(self, label):
        labelset = {}  # dictionary 3 jenis label latih berbeda
        for kelas in label.unique():
            label_temp = label.copy(deep=True)  # agar data asli tidak berubah & untuk map ulang
            label_temp = label_temp.map({kelas:1})  # kelas one bernilai 1
            label_temp = label_temp.fillna(-1)  # kelas rest (selain one) bernilai -1
            labelset[kelas] = label_temp
        return labelset
    
    
    # Kernel trick RBF
    def kernel_rbf(self, x1, x2):
        # ||x|| -> linear algebra normalization
        linalg_norm = np.linalg.norm(x1[:, np.newaxis] - x2[np.newaxis, :], axis=2)
        return np.exp(-self.gamma_value * linalg_norm ** 2)
    
    # Kernel trick - Poly
    def kernel_polynomial(self, x1, x2):
        return (self.gamma_value * np.dot(x1, x2.T) + self.coef0) ** self.degree_poly

    # Kernel trick - Sigmoid
    def kernel_sigmoid(self, x1, x2):
        return np.tanh(self.gamma_value * np.dot(x1, x2.T) + self.coef0)

    # Kernel Trick - Transformasi Data
    def kernel_trick(self, x1, x2):
        if self.kernel == 'rbf':
            return self.kernel_rbf(x1, x2)
        elif self.kernel == 'poly':
            return self.kernel_polynomial(x1, x2)
        elif self.kernel == 'sigmoid':
            return self.kernel_sigmoid(x1, x2)
        
    # Koefisien Kernel - Gamma auto
    def gamma_auto(self, x):
        n_fitur = x.shape[1]
        self.gamma_value = 1 / n_fitur
        
    # Koefisien Kernel - Gamma scale
    def gamma_scale(self, x):
        n_fitur = x.shape[1]
        self.gamma_value = 1 / (n_fitur * x.var())
    

    # Fungsi hitung cost gradien untuk menghitung nilai minimal / gradien
    # cost function / loss function
    def hitung_cost_gradient(self, W, X, Y):
        y_hat = np.dot(X, W)
        jarak = 1 - (Y * y_hat)
        dw = np.zeros(len(W))

        di = np.where(max(0, jarak) == 0, W, (W - (self.C * Y * X)))
        dw += di
        return dw
    
    # Fungsi SGD, untuk optimasi / meminimalkan cost function
    def sgd(self, X_train, Y_train, max_epoch=1000):
        x = X_train.copy(deep=True).to_numpy().astype(float)
        y = Y_train.copy(deep=True).to_numpy()
        
        # x / X_train initial, untuk kernel trick saat predict
        self.X_train_initial = x.copy()
        
        # Koefisien Kernel - Gamma
        self.gamma(x)
        
        # Kernel trick - Transformasi data
        if self.kernel != 'linear':
            x = self.kernel_trick(x, x)
        
        # menyimpan X_train setelah dilakukan kernel trick untuk dicek
        self.X_train_trick = x
        
        bobot = np.zeros(x.shape[1])  # bobot sejumlah fitur (disesuaikan kernel trick)
        # bias = 0.
            
        # stochastic gradient descent
        for epoch in range(1, max_epoch):
            X, Y = shuffle(x, y, random_state=self.random_state)

            for index, x_loop in enumerate(X):  # loop tiap baris data
                delta = self.hitung_cost_gradient(bobot, x_loop, Y[index])  # gradien
                bobot = bobot - (self.learning_rate * delta)  # optimizer SGD

        return bobot
    
    # Fungsi fit untuk melakukan training
    def fit(self, X_train, Y_train):
        # fitur = X_train; label = Y_train
        labelset = self.create_labelset(Y_train)

        w = {}
        for kelas in labelset.keys():
            label_latih = labelset[kelas]
            w[kelas] = self.sgd(X_train, label_latih)
        
        # Hasil fungsi fit adalah bobot
        self.Weight = w
    
    # Fungsi predict binary untuk melakukan binary testing
    def predict_binary(self, W, X_validation):
        prediksi = np.array([])
        for i in range(X_validation.shape[0]):
            y_hat = np.dot(X_validation[i], W)
            y_prediksi = np.sign(y_hat)  # hasil prediksi satu baris data
            prediksi = np.append(prediksi, y_prediksi)
        return prediksi

    # Fungsi predict untuk melakukan testing one vs rest
    def predict(self, X_validation):
        # data uji = X_validation
        x = X_validation.copy(deep=True).to_numpy().astype(float)
        
        # Kernel trick - Transformasi data
        if self.kernel != 'linear':
            x = self.kernel_trick(x, self.X_train_initial)
            # x = self.kernel_trick(self.X_train_initial, x)
            
        # menyimpan X_validation setelah dilakukan kernel trick untuk dicek
        self.X_validation_trick = x
        
        # mengambil kelas pada bobot W
        list_kelas = self.Weight.keys()
        # dataframe untuk menyimpan hasil prediksi
        hasil = pd.DataFrame(columns = list_kelas)
        
        # looping setiap kelas klasifikasi
        for kelas in list_kelas:
            # prediksi dilakukan dengan bobot setiap kelas satu-persatu
            hasil[kelas] = self.predict_binary(self.Weight[kelas], x)

        # hasil prediksi adalah kelas dengan nilai 1
        # sehingga mengambil nama kelas (kolom) setiap baris dengan melihat nilai maksimum 
        kelas_prediksi = hasil.idxmax(axis = 1)
        
        # kebutuhan cek isi
        self.temp_hasil = hasil
                
        return kelas_prediksi