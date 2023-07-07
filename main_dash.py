import pandas as pd
import numpy as np
import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import altair as alt

from collections import Counter

import mpld3
import streamlit.components.v1 as components

# Color
cmap_accent = [matplotlib.colors.rgb2hex(plt.get_cmap("Accent").colors[i]) for i in range(plt.get_cmap("Accent").N)]
cmap_set = [matplotlib.colors.rgb2hex(plt.get_cmap("Set3").colors[i]) for i in range(plt.get_cmap("Set3").N)]
cmap_summer = [matplotlib.colors.rgb2hex(plt.get_cmap("summer", 5)(i)) for i in range(plt.get_cmap("summer", 5).N)]


# fungsi mendapatkan data angkatan
def get_angkatan(df):
    return (df["NIM"] // 1e13).astype(int)


# fungsi mendapatkan pengelompokan mata kuliah yang diambil responden
def get_matakuliah(df):
    df_mk = df['Mata Kuliah'].copy(deep=True)
    df_mk = df_mk.replace(['PPM F'], 'PPM')
    df_mk = df_mk.replace(['IESI A'], 'IESI').replace(['IESI D'], 'IESI')
    df_mk = df_mk.replace(['ADSI B'], 'ADSI').replace(['ADSI E'], 'ADSI')
    df_mk = df_mk.replace(['DPSI C'], 'DPSI')
    df_mk = df_mk.replace(['DDAP E'], 'DDAP')
    df_mk = df_mk.replace(['DIMP A'], 'DIMP').replace(['DIMP C'], 'DIMP')
    return df_mk


def main_page():
    # Read Dataframe
    ## Dataset 
    df = pd.read_excel('Data/Data Result - over full-n8.xlsx', sheet_name='df')

    ## Dataframe After Oversampling
    df_oversampling = pd.read_excel('Data/Data Result - over full-n8.xlsx', sheet_name='df_a oversampling')

    ## 10 Fold Afektif dan Kategorikal Afektif
    eval_model = pd.read_excel('Data/Data Result - over full-n8.xlsx', sheet_name='Evaluasi Model')

    ## 10 Fold Hyperparameter Tuning
    eval_hypertune = pd.read_excel('Data/Hyperparameter Tuning - over full-n8.xlsx', sheet_name='Hypertune')

    ## Performance Metrics - Manual vs Library
    eval_svm = pd.read_excel('Data/Data Result - over full-n8.xlsx', sheet_name='Performance SVM')

    # Confusion Matrix SVM
    conf_SVM = pd.read_excel('Data/Data Result - over full-n8.xlsx', sheet_name='Confusion SVM')

    # Performance Metrics
    eval_predict = pd.read_excel('Data/Data Result - over full-n8.xlsx', sheet_name='Performance Metrics')


    fig = plt.figure(figsize=(30,15))
    gs =  fig.add_gridspec(8, 11)
    fig.suptitle("Prediksi Kinerja Mahasiswa Berdasarkan Faktor Afektif Pada HSS Learning\nMenggunakan Metode Support Vector Machine", fontsize=32.5, y=1)
    gs.update(wspace=.5, hspace=.5)
    # fig.tight_layout()
    # gs.tight_layout(pad=3)

    ax1 = fig.add_subplot(gs[0:2, 0:4])  # Jumlah Data
    bar_plot_jumlahdata(ax1, df, df_oversampling)

    ax2 = fig.add_subplot(gs[2:6, 0:4])  # Persebaran Nilai Mahasiswa
    bar_plot_nilai(ax2, df, df_oversampling)

    ax3 = fig.add_subplot(gs[6:, 0:2])  # Persentase Angkatan
    presentase_angkatan_plot(ax3, df)

    ax4 = fig.add_subplot(gs[6:, 2:4])  # Persentase Kelas
    presentase_kelas_plot(ax4, df)

    ax5 = fig.add_subplot(gs[0:3, 4:9])  # Performa Model SVM
    ax6 = fig.add_subplot(gs[0:3, 9:])  # Average Performa Model SVM
    kfold_bar_plot(ax5, ax6, eval_model)
    ## average use bar biasa, bkn barh

    ax7 = fig.add_subplot(gs[3:5, 4:])  # Hyperparameter Tuning
    hyperparameter_tuning_table(ax7, eval_hypertune)

    ax8 = fig.add_subplot(gs[5:8, 4:9])  # Performa SVM
    acc_bar_plot(ax8, eval_predict)

    ax9 = fig.add_subplot(gs[5:8, 9:])  # Confusion Matrix SVM
    confusion_matrix_table(ax9, conf_SVM)

    st.pyplot(fig)


# fungsi memberikan label value pada bar chart
def addlabels(ax, shift, data, size):
    for i in range(data.shape[0]):
        ax.text(i + shift, data[i] + 1, data[i], ha = 'center', fontsize=size)

# fungsi memberikan label value pada bar chart
def addlabels_svm(ax, shift, data, size):
    for i in range(data.shape[0]):
        ax.text(i + shift, data.iloc[i] + 1, data.iloc[i], ha = 'center', fontsize=size)


# fungsi mencetak bar plot jumlah data
def bar_plot_jumlahdata(ax, df, df_over):
    dict_data = {}
    dict_data["Sebelum\nOversampling"] = df.shape[0]
    dict_data["Setelah\nOversampling"] = df_over.shape[0]

    data_plot = pd.Series(dict_data).sort_values(ascending=False)

    # plotting average
    # fig = plt.figure(figsize=(10,2))
    ax = data_plot.plot(kind='barh', color=cmap_accent[1], width=0.75)

    for i, (p, pr) in enumerate(zip(data_plot.index, data_plot)):
        ax.text(s=p, x=7, y=i, color="black", verticalalignment="center", size=15)
        ax.text(s=str(pr), x=pr-40, y=i, color="black",
            verticalalignment="center", horizontalalignment="left", size=19)

    ax.set_title("Jumlah Data", y=.95, fontsize=18)
    # ax1.box(False)
    ax.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])
    # plt.tick_params(axis='y', length=0)

    # st.pyplot(fig)


# fungsi mencetak bar plot data nilai
def bar_plot_nilai(ax, df, df_over):
# def bar_plot_nilai(df, position):
    # Dictionary nilai
    dict_5cat = {}
    dict_5cat['Very Low'] = 0
    dict_5cat['Low'] = 0
    dict_5cat['Moderate'] = 0
    dict_5cat['High'] = 0
    dict_5cat['Very High'] = 0

    # mengambil data kategori nilai untuk divisualisasikan
    dict_nilai = dict_5cat.copy()
    dict_nilai.update(df['Nilai'].value_counts().to_dict())
    dict_nilai_over = dict_5cat.copy()
    dict_nilai_over.update(df_over['Nilai'].value_counts().to_dict())
    
    # membuat plot untuk memvisualisasikan persebaran data nilai setelah oversampling
    # fig = plt.figure(figsize=(10,5))

    X_axis = np.arange(len(dict_5cat))
    ax.bar(X_axis - 0.2, pd.Series(dict_nilai), 0.4, label = 'Sebelum Oversampling', color=cmap_accent[0])
    ax.bar(X_axis + 0.2, pd.Series(dict_nilai_over), 0.4, label = 'Setelah Oversampling', color=cmap_accent[2])

    addlabels(ax, -0.2, pd.Series(dict_nilai), size=14)
    addlabels(ax, 0.2, pd.Series(dict_nilai_over), size=14)

    ax.set_xticks(X_axis, dict_5cat.keys(), rotation=0)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_title("Persebaran Nilai Mahasiswa", y=1.015, fontsize=18)
    ax.set_ylabel("Jumlah Mahasiswa", fontsize=14)
    ax.set_xlabel("Kategori", fontsize=14)
    ax.legend(shadow=True, fontsize=14)
    ax.grid(True, axis='y')
    # st.pyplot(fig)


def presentase_angkatan_plot(ax, df):
    # mengesktrak data angkatan dari data NIM
    df_angkatan = get_angkatan(df)

    # mengurutkan dan memberikan postfix angkatan
    angkatan = df_angkatan.value_counts().rename_axis('Angkatan').reset_index(name='Jumlah').sort_values(by=['Angkatan'])
    angkatan = angkatan.replace({'Angkatan': {17: 'Angkatan 17', 18: 'Angkatan 18', 19:'Angkatan 19', 20:'Angkatan 20', 21:'Angkatan 21'}})

    # plotting
    # fig = plt.figure(figsize =(7, 7))
    ax.pie(angkatan['Jumlah'], labels=angkatan['Angkatan'],autopct='%1.1f%%',colors=cmap_accent[4::-1], labeldistance=None)
    ax.set_title("Persentase Angkatan Responden", y=.9, fontsize=16)
    # plt.ylabel('')
    ax.legend(bbox_to_anchor=(0.5, 0.075), loc='upper center', ncol=2, fontsize=12)
    # st.pyplot(fig)


def presentase_kelas_plot(ax, df):
    # membuat datafram baru berupa gabungan jumlah responden berdasarkan mata kuliah
    df_mk = get_matakuliah(df).value_counts().rename_axis('Kelas').reset_index(name='Jumlah').sort_values(by=['Kelas'])
    
    # plotting
    # fig = plt.figure(figsize =(7, 7))
    ax.pie(df_mk['Jumlah'], labels=df_mk['Kelas'],autopct='%1.2f%%',colors=cmap_accent, labeldistance=None)
    ax.set_title("Persentase Kelas Responden", y=.9, fontsize=16)
    # plt.ylabel('')
    ax.legend(bbox_to_anchor=(0.5, 0.075), loc='upper center', ncol=3, fontsize=12)
    # st.pyplot(fig)


def kfold_bar_plot(ax1, ax2, eval_model):
    # preprocessing untuk penyesuaian streamlit
    eval_model.rename(columns={eval_model.columns[0]: "Fold"}, inplace=True)
    eval_model = eval_model.astype({"Fold":str, "Afektif":float, "Kategorikal Afektif":float})
    eval_model.set_index(eval_model.columns[0], inplace=True)

    # plotting kfold
    # fig = plt.figure(figsize=(10,5))

    X_axis = np.arange(eval_model.shape[0] - 1)
    ax1.bar(X_axis - 0.2, eval_model["Afektif"][:-1], 0.4, label = 'Data Afektif', color=cmap_accent[0])
    ax1.bar(X_axis + 0.2, eval_model["Kategorikal Afektif"][:-1], 0.4, label = 'Data Kategorikal Afektif', color=cmap_accent[2])

    addlabels_svm(ax1, -0.2, eval_model['Afektif'][:-1].astype(float).round(1), 12)
    addlabels_svm(ax1, 0.2, eval_model['Kategorikal Afektif'][:-1].astype(float).round(1), 12)

    ax1.set_xticks(X_axis, eval_model[:-1].index, rotation=0)
    ax1.set_title("Performa Model SVM pada Dataset Afektif dan Dataset Kategorikal Afektif", y=1.015, fontsize=18)
    ax1.tick_params(axis='both', which='major', labelsize=14)
    ax1.set_ylabel("Akurasi", fontsize=14)
    ax1.set_xlabel("Fold", fontsize=14)
    ax1.legend(loc='lower right', shadow=True, fontsize=14)
    ax1.grid(True, axis='y')

    # st.pyplot(fig)


    ## Average kfold Plot
    data_average = eval_model.copy().iloc[-1].round(1).sort_values(ascending=False).rename({"Kategorikal Afektif": "Kategorikal\nAfektif"})
    # plotting
    ax2 = data_average.plot(kind='bar', color=cmap_accent[1])

    for container in ax2.containers:
        ax2.bar_label(container, fontsize=14)

    for tick in ax2.get_xticklabels():
        tick.set_rotation(0)

    ax2.set_title("Rata-rata Performa Model SVM", y=1.015, fontsize=18)
    ax2.tick_params(axis='both', which='major', labelsize=14)
    ax2.set_ylabel("Rata-rata Akurasi", fontsize=14)
    # ax2.set_xlabel("Data", fontsize=14)
    # ax2.set_xticks(data_average.index, rotation=0)
    ax2.grid(True, axis='y')


def hyperparameter_tuning_table(ax, eval_hypertune):
    eval_hypertune.set_index(eval_hypertune.columns[0], inplace=True)
    eval_hypertune.sort_values(by="average_score", ascending=False, inplace=True)
    eval_hypertune['average_score'] = eval_hypertune['average_score'].round(2).astype(str) + '%'
    # st.table(eval_hypertune.head(5))
    
    ax.axis('off')
    hypertune_table = ax.table(cellText=np.array(eval_hypertune.head(5)),
                        rowLabels=["Best {}".format(i) for i in range(1,6)],
                        colLabels=eval_hypertune.columns,
                        rowColours = [cmap_accent[2]] * 5,
                        colColours = [cmap_accent[0]] * len(eval_hypertune.columns),
                        cellLoc='center',
                        loc='center', bbox=[.1, .015, .85, .85])
    hypertune_table.set_fontsize(16)
    hypertune_table.scale(.85,2)
    ax.set_title("Hyperparameter Tuning SVM", y=.885, fontsize=18)


def acc_bar_plot(ax, eval_predict):
    # preprocessing untuk penyesuaian streamlit
    eval_predict.set_index(eval_predict.columns[0], inplace=True)

    # plotting
    # fig = plt.figure(figsize=(10,5))

    X_axis = np.arange(eval_predict.shape[0])
    ax.bar(X_axis - 0.2, eval_predict['Support Vector Machine'], 0.2, label = 'Support Vector Machine', color=cmap_accent[0])
    ax.bar(X_axis, eval_predict['K-Nearest Neighbor'], 0.2, label = 'K-Nearest Neighbor', color=cmap_accent[1])
    ax.bar(X_axis + 0.2, eval_predict['Decision Trees'], 0.2, label = 'Decision Trees', color=cmap_accent[2])

    addlabels_svm(ax, -0.2, eval_predict['Support Vector Machine'].astype(float).round(1), 14)
    addlabels_svm(ax, 0, eval_predict['K-Nearest Neighbor'].astype(float).round(1), 14)
    addlabels_svm(ax, 0.2, eval_predict['Decision Trees'].astype(float).round(1), 14)

    ax.set_xticks(X_axis, eval_predict.index, rotation=0)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.set_title("Performa Prediksi SVM", y=1.01, fontsize=18)
    ax.set_ylabel("Persentase", fontsize=14)
    ax.set_xlabel("Evaluasi", fontsize=14)
    ax.legend(loc='lower right', shadow=True, fontsize=14)
    ax.grid(True, axis='y')

    # st.pyplot(fig)


def confusion_matrix_table(ax, conf_SVM):
    conf_SVM.set_index(conf_SVM.columns[0], inplace=True)
    # st.table(conf_SVM)

    ax.axis('off')
    conf_table = ax.table(cellText=np.array(conf_SVM),
                        rowLabels=conf_SVM.index,
                        colLabels=conf_SVM.columns,
                        rowColours = [cmap_accent[2]] * len(conf_SVM.index),
                        colColours = [cmap_accent[0]] * len(conf_SVM.columns),
                        cellLoc='center',
                        loc='center', bbox=[.2, .25, .75, .5])
    conf_table.set_fontsize(16)
    conf_table.scale(.6,3)
    ax.set_title("Confusion Matrix SVM", y=.765, fontsize=18)
