# Gerekli kütüphaneleri içe aktar
import pandas as pd #CSV dosyasını okuyup veriyi işler
from sklearn.model_selection import train_test_split #veriyi eğitim (%70) ve test (%30) olarak böler

from sklearn.ensemble import RandomForestClassifier #Modelimiz – bir saldırı tespit algoritması
from sklearn.metrics import accuracy_score, classification_report #Model ne kadar doğru tahmin etti, onu ölçer
import matplotlib.pyplot as plt #ileride grafikler çizmek için kullanacağız
import joblib # makine öğrenmesi modellerini daha verimli şekilde kaydetmek ve yüklemek için kullanılır.


df = pd.read_csv("loglar_cleaned.csv", delimiter=';')

df.dropna(inplace=True)

y = df["label"]


X = df.drop(columns=["timestamp", "label"])


X = pd.get_dummies(X)


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

model = RandomForestClassifier(class_weight='balanced')
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


print("\n🎯 Başarı Oranı (Accuracy):", accuracy_score(y_test, y_pred))
print("\n📋 Sınıflandırma Raporu:")
print(classification_report(y_test, y_pred))

print("🔍 Veri Önizleme:")
print(df.head())


y = df["label"]


X = df.drop(columns=["timestamp", "label"])

#sayısal olmayanları sayısala çevir (örneğin IP ve endpoint)
X = pd.get_dummies(X)

# %70 eğitim, %30 test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#modeli oluştur
model = RandomForestClassifier(class_weight='balanced')

model.fit(X_train, y_train)

# thmin yap
y_pred = model.predict(X_test)


print("\n🎯 Başarı Oranı (Accuracy):", accuracy_score(y_test, y_pred))


print("\n📋 Sınıflandırma Raporu:")
print(classification_report(y_test, y_pred))


joblib.dump(model, "ddos_model.pkl")
print("Model başarıyla 'ddos_model.pkl' olarak kaydedildi.")