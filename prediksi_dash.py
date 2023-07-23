import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import svm

def prediksi_page():                       
    st.markdown("<h2 style='text-align: center; color: system;'>Uji Coba Prediksi Kinerja Mahasiswa</h2>", unsafe_allow_html=True)
    st.markdown("<hr></hr>", unsafe_allow_html=True)

    kategori_aeq_positif = pd.DataFrame({"Kategori":["Low", "Moderate", "High"], "Rentang Nilai":["12 - 28", "29 - 44", "45 - 60"]}, index=[1,2,3])
    kategori_aeq_negatif = pd.DataFrame({"Kategori":["Low", "Moderate", "High"], "Rentang Nilai":["20 - 46", "47 - 73", "74 - 100"]}, index=[1,2,3])
    kategori_dass = pd.DataFrame({"Kategori":["Normal", "Mild", "Moderate", "Severe", "Extremely severe"], "Depression":["0 - 9", "10 - 13", "14 - 20", "21 - 27", "28+"], "Anxiety":["0 - 7", "8 - 9", "10 - 14", "15 - 19", "20+"], "Stress":["0 - 14", "15 - 18", "19 - 25", "26 - 33", "34+"]}, index=[1,2,3,4,5])
    kategori_erq_crf = pd.DataFrame({"Kategori":["Low", "Moderate", "High"], "Rentang Nilai":["6 - 18", "19 - 30", "31 - 42"]}, index=[1,2,3])
    kategori_erq_esf = pd.DataFrame({"Kategori":["Low", "Moderate", "High"], "Rentang Nilai":["4 - 12", "13 - 20", "21 - 28"]}, index=[1,2,3])

    ####### Glosarium #######
    st.markdown("### Glosarium")
    with st.expander("📗 -  Glosarium", expanded=False):
        st.write("""    
        - ##### AEQ-s\t: _Achievement Emotion Questionnaire short version_ (AEQ-s)\n
            - merupakan instrumen yang digunakan untuk mengukur emosi dalam pembelajaran dan kinerja siswa.
            - Pada AEQ-s terdapat tiga pengaturan yang diukur, yaitu _Class-related_, _Learning-related_, dan _Test-related_. Namun, pada penelitian ini hanya digunakan pengaturan _Class-related_ dan _Learning-related_ saja.
            Setiap pengaturan terdiri dari 8 skala emosi yang dibagi menjadi 3 emosi positif dan 5 emosi negatif.
                - _Class-related emotion_\n
                merujuk pada emosi yang dirasakan ketika berada pada kelas. Terdiri dari emosi _enjoyment_, _hope_, _pride_, _anger_, _anxiety_, _shame_, _hopelessness_, dan _boredom_.
                - _Learning-related emotion_\n
                merujuk pada emosi yang dirasakan ketika proses belajar. Terdiri dari emosi _enjoyment_, _hope_, _pride_, _anger_, _anxiety_, _shame_, _hopelessness_, dan _boredom_.
            - Kuesioner AEQ-s terdiri dari empat butir pertanyaan untuk setiap skala emosi. 
            - Skala likert 5-poin digunakan untuk merekam jawaban setiap butir pertanyaan.
            - Sumber:
                - Pekrun dkk. (2011)\t:  https://doi.org/10.1016/j.cedpsych.2010.10.002
                - Bieleke dkk. (2021)\t:  https://doi.org/10.1016/j.cedpsych.2020.101940
            - Pada penelitian ini, instrumen AEQ-s dikategorisasikan dengan metode _equal-width discretization_.
            Kategorisasi dilakukan menjadi tiga kategori umum, yaitu _low_, _moderate_, dan _high_ dengan rentang yang sama.
        """)
        col_cat1, col_cat2 = st.columns([.7,1])
        with col_cat1:
            st.write("Kategori pada _Class-related_ dan _Learning-related_ emosi positif")
            st.write(kategori_aeq_positif)
        with col_cat2:
            st.write("Kategori pada _Class-related_ dan _Learning-related_ emosi negatif")
            st.write(kategori_aeq_negatif)

        st.write("""
        - ##### DASS 21\t: _Depression, Anxiety, and Stress Scale_ (DASS) 21\n
            - merupakan instrumen yang digunakan untuk mengukur besarnya tiga emosi negatif, yaitu depresi (_depression_), kecemasan (_anxiety_), dan stres (_stress_).
                - _Depression_\n
                mengacu pada suasana hati rendah, motivasi, dan harga diri.
                - _Anxiety_\n
                mengacu pada gairah fisiologis, rasa panik, dan rasa takut.
                - _Stress_\n
                mengacu pada ketegangan dan sifat pemarah.
            - Kuesioner DASS-21 mengukur besarnya emosi negatif melalui 21 butir pertanyaan.
            - Skala 4 poin yang dimulai dari 0-3 digunakan untuk merekam jawaban setiap butir pertanyaan.
            - Besarnya emosi negatif beserta tingkat keparahannya diketahui melalui penjumlahan skor yang didapatkan pada setiap subskala.
            - Sumber:
                - Lovibond dan Lovibond (1995)\t: ISBN 0-7334-1423-0
                - Reznik, Binns dan Egger (2017)\t: https://doi.org/10.1016/B978-0-12-810401-9.00015-2
        """)
        st.write("Kategori pada DASS")
        st.write(kategori_dass)

        st.write("""
        - ##### ERQ\t: _Emotion Regulation Questionnaire_ (ERQ)\n
            - merupakan instrumen yang digunakan untuk mengukur regulasi emosi.
            - Pada ERQ terdapat dua strategi regulasi emosi, yaitu _Cognitive Reappraisal_ dan _Expressive Suppression_.
                - _Cognitive Reappraisal Facet_ (CRF)\n
                merujuk pada rendahnya depresi, kecemasan dan stres.
                - _Expressive Suppression Facet_ (ESF)\n
                merujuk pada tingginya depresi, kecemasan, dan stres.
            - Kuesioner ERQ terdiri atas total 10 butir pertanyaan dengan rincian 6 butir pada CRF dan 4 butir pada ESF.
            - Skala likert 7-poin digunakan untuk merekam jawaban setiap butir pertanyaan
            - Sumber:
                - Gross dan John (2003)\t: https://doi.org/10.1037/0022-3514.85.2.348
                - Preece dkk. (2021)\t: https://doi.org/10.1016/j.jad.2021.01.071
            - Pada penelitian ini, instrumen ERQ dikategorisasikan dengan metode _equal-width discretization_.
            Kategorisasi dilakukan menjadi tiga kategori umum, yaitu _low_, _moderate_, dan _high_ dengan rentang yang sama.
        """)
        col_cat3, col_cat4 = st.columns([.5,1])
        with col_cat3:
            st.write("Kategori pada ERQ emosi CRF")
            st.write(kategori_erq_crf)
        with col_cat4:
            st.write("Kategori pada ERQ emosi ESF")
            st.write(kategori_erq_esf)

        st.write("""
        - ##### Kinerja Mahasiswa
            - Kinerja mahasiswa atau disebut juga nilai mahasiswa, terdiri dari evaluasi kinerja melalui nilai _post-test_ platform HSS Learning mahasiswa.
            - Kinerja mahasiswa digunakan untuk mengetahui atau mengevaluasi kinerja mahasiswa sesudah menggunakan platform HSS Learning
            - Pada penelitian ini, kinerja mahasiswa dikategorisasikan lima kategori umum, yaitu _very low_, _low_, _moderate_, _high_ dan _very high_.
        """)


    ####### Petunjuk Penggunaan #######
    st.markdown("### Petunjuk Penggunaan Halaman")
    with st.expander("⚙️ -  Petunjuk Penggunaan Halaman", expanded=False):
        st.write("1. Bacalah informasi terkait uji coba prediksi melalui bagian Glosarium terlebih dahulu untuk mendapatkan pemahaman terkait prediksi kinerja mahasiswa berdasarkan faktor afektif.")
        st.image("Pictures/Step 1.png", width=720)
        st.write("2. Setiap kuesioner AEQ-s, DASS, dan ERQ dapat ditampilkan dengan menekan tombol \"Isi Kuesioner\".")
        st.image("Pictures/Step 2.png", width=720)
        st.write("3. Jawablah setiap pertanyaan pada kuesioner AEQ-s, DASS, dan ERQ dengan memilih salah satu jawaban yang paling sesuai dengan kondisi Anda.")
        st.image("Pictures/Step 3.png", width=720)
        st.write("4. Setelah kuesioner selesai diisikan, Anda dapat menekan tombol \"Submit\" untuk menyimpan jawaban kuesioner dan mendapatkan hasil prediksi kinerja.")
        st.image("Pictures/Step 4.png", width=720)
        st.write("5. Anda juga dapat menekan tombol \"Random Submit\" untuk mengisikan kuesioner secara acak jika tidak ingin mengisikan kuesioner satu per satu.")
        st.image("Pictures/Step 5.png", width=720)
        st.write("6. Jawaban kuesioner yang diberikan akan diolah oleh sistem berupa diagnosa kategori emosi yang Anda miliki dan hasil prediksi kinerja yang dapat dilihat pada bagian paling bawah dari halaman ini.")
        st.image("Pictures/Step 6.png", width=720)

    st.markdown("<hr></hr>", unsafe_allow_html=True)


    ####### Kuesioner #######
    # Read Questionnairre List
    global df_aeq_class
    global df_aeq_learn
    global df_dass
    global df_erq
    df_aeq_class = pd.read_excel('Data/questionnaire.xlsx', sheet_name='AEQ-s Class-Related', index_col=0)
    df_aeq_learn = pd.read_excel('Data/questionnaire.xlsx', sheet_name='AEQ-s Learning-Related', index_col=0)
    df_dass = pd.read_excel('Data/questionnaire.xlsx', sheet_name='DASS', index_col=0)
    df_erq = pd.read_excel('Data/questionnaire.xlsx', sheet_name='ERQ', index_col=0)

    # random_submit()

    # st.write(df_aeq_class['Question'])
    # st.write(df_aeq_learn['Question'])
    # st.write(df_dass['Question'])
    # st.write(df_erq['Question'])

    if 'num' not in st.session_state:
        st.session_state.num = 0


    ## Emosi pada AEQ
    emotion_aeq = ["Enjoyment", "Hope", "Pride", "Anger", "Anxiety", "Shame", "Hopelessness", "Boredom"]

    choices_aeq = ['Sangat Tidak Setuju', 'Tidak Setuju', 'Netral', 'Setuju', 'Sangat Setuju']
    choices_dass = ['Tidak Pernah Dialami', 'Pernah Dialami', 'Sering Dialami', 'Sangat Sering Dialami']
    choices_erq = ['Sangat Tidak Setuju', 'Tidak Setuju', 'Sedikit Tidak Setuju', 'Netral', 'Sedikit Setuju', 'Setuju', 'Sangat Setuju']

    qsaeq_class = [(question, choices_aeq) for question in df_aeq_class['Question']]
    qsaeq_learn = [(question, choices_aeq) for question in df_aeq_learn['Question']]
    qsdass = [(question, choices_dass) for question in df_dass['Question']]
    qserq = [(question, choices_erq) for question in df_erq['Question']]


    # variabel untuk menyimpan jawaban kuesioner
    answer_aeq_class = []
    answer_aeq_learn = []
    answer_dass = []
    answer_erq = []


    # Pembuatan form kuesioner
    questionnaire_fontsize = '16px'
    with st.form("afektif_form"):
        ### Kuesioner AEQ
        st.markdown("### Kuesioner AEQ-s")
        with st.expander("Isi Kuesioner", expanded=False):
            #### Class-related emotion
            st.markdown("#### Class-related emotion")
            num_question = 0  # untuk menampilkan nama emosi pada aeq
            num_emotion = 0  # untuk mengetahui urutan emosi yang dicetak pada aeq
            for question in qsaeq_class:
                if num_question == 0:  # jika num_question == 0, maka cetak emosi aeq
                    st.markdown("##### {}".format(emotion_aeq[num_emotion]))
                    num_emotion += 1
                answer_aeq_class.append(st.radio(question[0], options=question[1], horizontal=True))
                ChangeWidgetFontSize(question[0], questionnaire_fontsize)
                # mekanisme untuk menampilkan nama emosi tiap 4 pertanyaan
                num_question += 1
                if num_question == 4: num_question = 0

            #### Learning-related emotion
            st.markdown("#### Learning-related emotion")
            num_question = 0  # untuk menampilkan nama emosi pada aeq
            num_emotion = 0  # untuk mengetahui urutan emosi yang dicetak pada aeq
            for question in qsaeq_learn:
                if num_question == 0:  # jika num_question == 0, maka cetak emosi aeq
                    st.markdown("##### {}".format(emotion_aeq[num_emotion]))
                    num_emotion += 1
                answer_aeq_learn.append(st.radio(question[0], options=question[1], horizontal=True))
                ChangeWidgetFontSize(question[0], questionnaire_fontsize)
                # mekanisme untuk menampilkan nama emosi tiap 4 pertanyaan
                num_question += 1
                if num_question == 4: num_question = 0

        ### Kuesioner DASS
        st.markdown("### Kuesioner DASS")
        with st.expander("Isi Kuesioner", expanded=False):
            for question in qsdass:
                answer_dass.append(st.radio(question[0], options=question[1], horizontal=True))
                ChangeWidgetFontSize(question[0], questionnaire_fontsize)

        ### Kuesioner ERQ
        st.markdown("### Kuesioner ERQ")
        with st.expander("Isi Kuesioner", expanded=False):
            for question in qserq:
                answer_erq.append(st.radio(question[0], options=question[1], horizontal=True))
                ChangeWidgetFontSize(question[0], questionnaire_fontsize)
        

        # setiap form harus memiliki submit button
        col1, col2 = st.columns([.09,1])
        with col1:
            submitted = st.form_submit_button("Submit", help='Kirim jawaban kuesioner yang telah diisikan')
        with col2:
            rand_submit = st.form_submit_button("Random Submit", help='Kirim jawaban kuesioner yang diisikan secara acak')

        # behaviour ketika tombol submit / random submit ditekan
        if submitted:
            st.success("Jawaban Anda berhasil di-submit")
            normal_submit(answer_aeq_class, answer_aeq_learn, answer_dass, answer_erq)
        elif rand_submit:
            st.success("Jawaban Anda berhasil di-submit secara acak")
            random_submit()


def ChangeWidgetFontSize(wgt_txt, wch_font_size = '12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.fontSize='""" + wch_font_size + """';} } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + wgt_txt + "'")
    components.html(f"{htmlstr}", height=0, width=0)


# behaviour jika tombol submit ditekan
def normal_submit(answer_aeq_class, answer_aeq_learn, answer_dass, answer_erq):
    answer_aeq_class = encoding("AEQ-s", answer_aeq_class)
    answer_aeq_learn = encoding("AEQ-s", answer_aeq_learn)
    answer_dass = encoding("DASS", answer_dass)
    answer_erq = encoding("ERQ", answer_erq)

    process_data(answer_aeq_class, answer_aeq_learn, answer_dass, answer_erq)


# behaviour jika tombol random submit ditekan
def random_submit():
    answer_aeq_class = np.random.randint(low=1, high=5, size=32, dtype=int)
    answer_aeq_learn = np.random.randint(low=1, high=5, size=32, dtype=int)
    answer_dass = np.random.randint(low=0, high=3, size=21, dtype=int)
    answer_erq = np.random.randint(low=1, high=7, size=10, dtype=int)

    process_data(answer_aeq_class, answer_aeq_learn, answer_dass, answer_erq)


# mengubah jawaban kuesioner ke dalam bentuk ordinal
def encoding(data_name, data):
    data = pd.Series(data)

    if data_name == 'AEQ-s':
        data.replace("Sangat Tidak Setuju", 1, inplace=True)
        data.replace("Tidak Setuju", 2, inplace=True)
        data.replace("Netral", 3, inplace=True)
        data.replace("Setuju", 4, inplace=True)
        data.replace("Sangat Setuju", 5, inplace=True)
    
    elif data_name == "DASS":
        data.replace("Tidak Pernah Dialami", 0, inplace=True)
        data.replace("Pernah Dialami", 1, inplace=True)
        data.replace("Sering Dialami", 2, inplace=True)
        data.replace("Sangat Sering Dialami", 3, inplace=True)

    elif data_name == "ERQ":
        data.replace("Sangat Tidak Setuju", 1, inplace=True)
        data.replace("Tidak Setuju", 2, inplace=True)
        data.replace("Sedikit Tidak Setuju", 3, inplace=True)
        data.replace("Netral", 4, inplace=True)
        data.replace("Sedikit Setuju", 5, inplace=True)
        data.replace("Setuju", 6, inplace=True)
        data.replace("Sangat Setuju", 7, inplace=True)
        
    return np.array(data)


def process_data(answer_aeq_class, answer_aeq_learn, answer_dass, answer_erq):
    # st.write(answer_aeq_class)
    # st.write(answer_aeq_learn)
    # st.write(answer_dass)
    # st.write(answer_erq)

    df = pd.DataFrame()
    df = df.append(pd.DataFrame(answer_aeq_class, index=df_aeq_class['Question']))
    df = df.append(pd.DataFrame(answer_aeq_learn, index=df_aeq_learn['Question']))
    df = df.append(pd.DataFrame(answer_dass, index=df_dass['Question']))
    df = df.append(pd.DataFrame(answer_erq, index=df_erq['Question']))
    df = df.T
    # st.write("Process data df")
    # st.write(df)

    ##### kategorisasi #####
    df_cat = kategorisasi(df)

    st.markdown("### Hasil Diagnosa")
    st.write(df_cat.style.hide_index().to_html(), unsafe_allow_html=True)
    st.write('\n')

    ##### prediksi #####
    st.markdown("### Hasil Prediksi Kinerja")
    prediksi(df.iloc[:, 0:95])


def kategorisasi(df):
    ##### Mendapatkan total skor #####

    # ===== AEQ =====
    # terdiri dari pengaturan Class-related dan Learning-related dengan emosi positif dan negatif
    # Positif: Enjoyment, Hope, Pride
    # Negatif: Anger, Anxiety, Shame, Hopelessness, Boredom
    df['Class_Positive_Skor'] = df.iloc[:, 0:12].sum(axis=1)
    df['Class_Negative_Skor'] = df.iloc[:, 12:32].sum(axis=1)
    df['Learn_Positive_Skor'] = df.iloc[:, 32:44].sum(axis=1)
    df['Learn_Negative_Skor'] = df.iloc[:, 44:64].sum(axis=1)


    # ===== DASS =====
    # terdiri dari Depression, Anxiety, dan Stress
    # D / Depression:  3,5,10,13,16,17,21 = 7 butir
    # A / Anxiety: 2,4,7,9,15,19,20 = 7 butir
    # S / Stress: 1,6,8,11,12,14,18 = 7 butir
    df['Depression_Skor'] = df.iloc[:, [66,68,73,76,79,80,84]].sum(axis=1)
    df['Anxiety_Skor'] = df.iloc[:, [65,67,70,72,78,82,83]].sum(axis=1)
    df['Stress_Skor'] = df.iloc[:, [64,69,71,74,75,77,81]].sum(axis=1)


    # ===== ERQ =====
    # terdiri dari Cognitive Reappraisal Facet (CRF) dan Expressive Suppression Facet (ESF)
    # CRF: 1,3,5,7,8,10 = 6 butir
    # ESF: 2,4,6,9 = 4 butir
    df['CRF_Skor'] = df.iloc[:, [85,87,89,91,92,94]].sum(axis=1)
    df['ESF_Skor'] = df.iloc[:, [86,88,90,93]].sum(axis=1)


    ##### Melakukan kategorisasi #####

    # Label column
    df = pd.concat([df, pd.DataFrame(columns=[col[:-5] for col in list(df.columns[95:])])])
    df.iloc[:, 104:] = df.iloc[:, 95:104].values

    # ===== AEQ =====

    # Positive Emotion
    for col in ['Class_Positive', 'Learn_Positive']:
        df[col] = np.where(df[col].between(12,28), "Low", 
            np.where(df[col].between(29,44), "Moderate",
            np.where(df[col].between(45,60), "High", df[col])))

    # Negative Emotion
    for col in ['Class_Negative', 'Learn_Negative']:
        df[col] = np.where(df[col].between(20,46), "Low", 
            np.where(df[col].between(47,73), "Moderate",
            np.where(df[col].between(74,100), "High", df[col])))


    # ===== DASS =====

    # Depression
    df['Depression'] = np.where(df['Depression'].between(0,9), "Normal", 
        np.where(df['Depression'].between(10,13), "Mild",
        np.where(df['Depression'].between(14,20), "Moderate",
        np.where(df['Depression'].between(21,27), "Severe",
        np.where(df['Depression'] >= 28, "Extremely severe", df['Depression'])))))

    # Anxiety
    df['Anxiety'] = np.where(df['Anxiety'].between(0,7), "Normal",
        np.where(df['Anxiety'].between(8,9), "Mild",
        np.where(df['Anxiety'].between(10,14), "Moderate",
        np.where(df['Anxiety'].between(15,19), "Severe", 
        np.where(df['Anxiety'] >= 20, "Extremely severe", df['Anxiety'])))))

    # Stress
    df['Stress'] = np.where(df['Stress'].between(0,14), "Normal", 
        np.where(df['Stress'].between(15,18), "Mild", 
        np.where(df['Stress'].between(19,25), "Moderate", 
        np.where(df['Stress'].between(26,33), "Severe", 
        np.where(df['Stress'] >= 34, "Extremely severe", df['Stress'])))))


    # ===== ERQ =====

    # CRF
    df['CRF'] = np.where(df['CRF'].between(6,18), "Low", 
        np.where(df['CRF'].between(19,30), "Moderate",
        np.where(df['CRF'].between(31,42), "High", df['CRF'])))

    # ESF
    df['ESF'] = np.where(df['ESF'].between(4,12), "Low",
        np.where(df['ESF'].between(13,20), "Moderate",
        np.where(df['ESF'].between(21,28), "High", df['ESF'])))
    
    return df.iloc[:, 104:]


def prediksi(df):
    kinerja_cat = pd.DataFrame({})

    model_SVM = svm.SVM(gamma='auto', kernel='rbf', learning_rate=1e-6, C=7000, random_state=67)
    Weight = pd.read_excel('Data/Model SVM.xlsx', sheet_name='Weight', index_col=0)
    X_train_initial = pd.read_excel('Data/Model SVM.xlsx', sheet_name='X_train_initial', index_col=0)

    model_SVM.Weight = Weight.to_dict('list')
    model_SVM.X_train_initial = X_train_initial.to_numpy()
    model_SVM.gamma(model_SVM.X_train_initial)

    # st.write(df)
    # st.write(df.shape)
    # st.write(model_SVM.X_train_initial.shape)

    predictions_SVM = model_SVM.predict(df)
    predictions_SVM = predictions_SVM.iloc[0]

    if predictions_SVM == "Very Low":
        rentang_bawah, rentang_atas = 0, 20
        st.error("Kinerja Anda tergolong dalam kategori **{}**, yaitu pada rentang nilai **{} - {}**.".format(predictions_SVM, rentang_bawah, rentang_atas))
    elif predictions_SVM == "Low":
        rentang_bawah, rentang_atas = 21, 40
        st.error("Kinerja Anda tergolong dalam kategori **{}**, yaitu pada rentang nilai **{} - {}**.".format(predictions_SVM, rentang_bawah, rentang_atas))
    elif predictions_SVM == "Moderate":
        rentang_bawah, rentang_atas = 41, 60
        st.warning("Kinerja Anda tergolong dalam kategori **{}**, yaitu pada rentang nilai **{} - {}**.".format(predictions_SVM, rentang_bawah, rentang_atas))
    elif predictions_SVM == "High":
        rentang_bawah, rentang_atas = 61, 80
        st.info("Kinerja Anda tergolong dalam kategori **{}**, yaitu pada rentang nilai **{} - {}**.".format(predictions_SVM, rentang_bawah, rentang_atas))
    elif predictions_SVM == "Very High":
        rentang_bawah, rentang_atas = 81, 100
        st.success("Kinerja Anda tergolong dalam kategori **{}**, yaitu pada rentang nilai **{} - {}**.".format(predictions_SVM, rentang_bawah, rentang_atas))

    # Rentang nilai untuk kategori nilai
    # Kategori      Rentang Nilai       Rentang Nilai (skala 100)
    # Very Low      0 – 5               0-20
    # Low	        6 – 10              21-40
    # Moderate	    11 – 16             41-60
    # High	        17 – 21             61-80
    # Very High	    22 – 27             81-100
    # tiap kategori diberikan warna berbeda, sehingga ada perbedaan dalam penggunaan success, info, waring, dan error

