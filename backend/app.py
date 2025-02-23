from fastapi import FastAPI
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import pymysql
pymysql.install_as_MySQLdb()
app = FastAPI()

# Load the Titanic dataset
df = pd.read_csv("titanic.csv")

@app.get("/query/")
def query(question: str):
    question = question.lower()
    
    if "percentage of passengers were male" in question:
        male_percentage = (df['Sex'].value_counts(normalize=True) * 100).get('male', 0)
        return {"answer": f"{male_percentage:.2f}% of passengers were male."}
    
    elif "average ticket fare" in question:
        avg_fare = df["Fare"].mean()
        return {"answer": f"The average ticket fare was ${avg_fare:.2f}."}
    
    elif "how many passengers embarked from each port" in question:
        embarked_counts = df["Embarked"].value_counts().to_dict()
        return {"answer": f"Passengers from each port: {embarked_counts}"}
    
    return {"answer": "Question not recognized."}

@app.get("/visualize/")
def visualize(query: str):
    fig, ax = plt.subplots()
    
    if "histogram of passenger ages" in query:
        sns.histplot(df["Age"].dropna(), bins=20, kde=True, ax=ax)
        ax.set_title("Passenger Age Distribution")
    
    elif "passengers embarked from each port" in query:
        sns.barplot(x=df["Embarked"].value_counts().index, y=df["Embarked"].value_counts().values, ax=ax)
        ax.set_title("Number of Passengers by Embarkation Port")
        ax.set_xlabel("Embarkation Port")
        ax.set_ylabel("Number of Passengers")
    
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    encoded = base64.b64encode(img.read()).decode()
    return {"image": encoded}