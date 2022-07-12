import os
os.system("cls")
print("welcome")
years=5
import joblib
mind=joblib.load("model.pickle")
output=mind.predict([[years]])
print(output,"yes")