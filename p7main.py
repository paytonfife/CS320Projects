import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder

# project: p7
# submitter: pjfife
# partner: none
# hours: 3

class UserPredictor():
    def __init__(self):
        self.xcols = ["past_purchase_amt", "seconds", "age"]
        self.model = LogisticRegression()
    
    def fit(self, df1, df2, df3):
        self.train_df = pd.merge(df1, df2[["user_id", "seconds"]].groupby("user_id").sum(),how = "left", on = "user_id").fillna(0)
        self.train_df = pd.merge(self.train_df, df3, on = "user_id")
        self.model.fit(self.train_df[self.xcols], self.train_df["y"])
        scores = cross_val_score(self.model, self.train_df[self.xcols], self.train_df["y"])
        return f"AVG: {scores.mean()}, STD: {scores.std()}"
    
    def predict(self, df1, df2):
        self.test_df = pd.merge(df1, df2[["user_id", "seconds"]].groupby("user_id").sum(), how = "left", on = "user_id").fillna(0)
        return self.model.predict(self.test_df[self.xcols])