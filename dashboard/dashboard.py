import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Layout
st.title('Submition Proyek Analisis Data Air Quality Dataset')
st.write('**Nama:** Dicky Ary Setiawan')
st.write('**Email:** DickyAry54@gmail.com')
st.write('**ID Dicoding:** ruhe54')

st.header('Menentukan Pertanyaan Bisnis')
st.write('- Apakah wilayah ini terjadi polusi udara ?')
st.write('- Apakah curah hujan mempengaruhi polusi udara ?')
st.write('- bagaimana pengaruh O3 dengan temperature udara ?')

# Data Wragling
st.subheader('Data Wrangling')
tiantan_df = pd.read_csv('main_data.csv')
st.write(tiantan_df.head())
print(tiantan_df.head())

# Cleaning Data
st.subheader('Cleaning Data')
st.write('Melakukan pengecekan apakah terdapat data yang hilang')
st.write(tiantan_df.isna().sum())
st.write('ternyata terdapat banyak sekali data yang hilang')
st.write('oleh karena itu akan dilakukan perbaikan data dengan menggunakan methode ffill')
tiantan_df = tiantan_df.fillna(method='ffill')
st.write(f'Setelah dilakukan ffill jumlah data yang hilang adalah sebagai berikut:')
st.write(tiantan_df.isna().sum())

# Exploratory Data Analysis (EDA)
st.subheader('Exploratory Data Analysis (EDA)')
st.write('Menggunakan metode Grouping untuk mengelompokkan Data berdasarkan hari')
day_df = tiantan_df.groupby(by=['year','month','day']).agg({
    'PM2.5': 'mean',
    'PM10': 'mean',
    'SO2': 'mean',
    'NO2': 'mean',
    'CO': 'mean',
    'O3': 'mean',
    'TEMP': 'mean',
    'PRES': 'mean',
    'DEWP': 'mean',
    'RAIN': 'mean',
    'WSPM': 'mean',
})
st.write(day_df.head())
st.write(f'Setelah di lakukan grouping ternyata jumlah row masih banyak yaitu {day_df.shape[0]},'
         f'Oleh karena itu akan dilakukan grouping berdasarkan bulan')
month_df = day_df.groupby(by=['year','month']).agg({
    'PM2.5' : 'mean',
    'PM10' : 'mean',
    'SO2' : 'mean',
    'NO2' : 'mean',
    'CO' : 'mean',
    'O3' : 'mean',
    'TEMP' : 'mean',
    'PRES' : 'mean',
    'DEWP' : 'mean',
    'RAIN' : 'mean',
    'WSPM' : 'mean',
})
st.write(month_df.head())
st.write(f'Setelah dilakukan grouping lagi jumlah row {month_df.shape[0]}')
st.write(f'Selanjutnya akan membuat colomn baru yang berisikan pengelompokan PM10 menjadi beberapa kategori')
month_df['air_condition'] = ['jelek' if x >= 150 else 'sedang' if x >= 50 or x < 150 else 'bagus' for x in month_df['PM10']]
st.write(month_df.head())
st.write('Dikutip dari website resmi BMKG.go.id')
st.write('PM10 adalah partikel udara yang berukuran lebih kecil dari 10 mikron.'
         'Nilai ambang batas adalah 150 µgram/m3 dimana jika nilai diantara 0 – 50 µgram/m3 dianggap kondisi udara maik baik ,'
         ' 51-150 µgram/m3 dianggap sedang, dan untuk jika lebih besar dari 150 µgram/m3 dianggap tidak sehat')

# Visualization & Explanatory Analysis
st.subheader('Visualization & Explanatory Analysis')

# Pertanyaan Pertama
st.write('Pertanyaan 1: Apakah wilayah ini terjadi polusi udara ?')

air_condition_df=month_df.groupby(by='air_condition').agg({
    'PM10': 'count',
})

plt.pie(x=air_condition_df.PM10,
        autopct='%1.1f%%',
        labels=('jelek','sedang')
        )
plt.title('Keadaan Udara pada Wilayah Tiantan')
st.pyplot(plt)

# Pertanyaan Kedua
st.write('Pertanyaan 2: Apakah curah hujan mempengaruhi nilai dari PM10 ?')

rain = month_df.sort_values(by=['RAIN'])
plt.figure(figsize=(10,6),dpi=300)

plt.plot(rain.RAIN,rain.PM10)
plt.xlabel("hujan mm/jam")
plt.ylabel("PM10 µgram/m3")

st.pyplot(plt)

# Pertanyaan ketiga
st.write('Pertanyaan 3: bagaimana pengaruh O3 dengan temperature udara ?')

Temperature = month_df.sort_values(by=['TEMP'])
plt.figure(figsize=(8,6),dpi=300)

plt.plot(Temperature.TEMP,Temperature.O3)

plt.xlabel('Temperature')
plt.ylabel('O3')

st.pyplot(plt)

st.write('''**Conclusion**

**Pertanyaan pertama**
Apakah wilayah ini terjadi polusi udara ?\n\n
Jawaban nya adalah Ya, wilayah ini dalam keadaan yang kurang baik ditunjukkan bahwa dalam 5 tahun kualitas udara tidak menunjukan keadaan yang baik dikarenakan nilai PM10 selalu tinggi

**Pertanyaan kedua**
Apakah curah hujan mempengaruhi nilai dari PM10 ?\n\n
curah hujan lah yang mempengaruhi tinggi dari nilai PM10 ketika curah hujan mulai tinggi nilai PM10 akan ditunjukkan semakin sedikit dan jika curah hujan sedang rendah maka nilai dari PM10 akan melonjak sangat tinggi sehingga kualitas udara akan memburuk

**Pertanyaan ketiga**
bagaimana pengaruh O3 dengan temperature udara ?\n\n
nilai O3 mempunyai pengaruh besar terhadap temperature udara dapat dilihat bahwa semakin tinggi nilai dari O3 maka temperature akan semakin naik dan jika nilai O3 sedang rendah maka temperature akan semakin dingin
''')