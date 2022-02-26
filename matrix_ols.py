#-------------------------------------------------------
#   Weonhyeok Chung weonhyeok.chung@gmail.com
#   OLS using Python Matrix
#   Feb-26-2022
#-------------------------------------------------------
import numpy as np 
import pandas as pd

df = pd.read_stata('matrix_ols.dta')  
df["intercept"] = 1

df = df[["intercept", "x1", "x2", "y"]]

X = df[["intercept", "x1", "x2"]].values
y = df[["y"]].values

n = X.shape[0]
k = X.shape[1]

# betas
XT = np.matrix.transpose(X)

XT_X = np.matmul(XT, X)

XT_X = np.matmul(XT, X)
XT_y = np.matmul(XT, y)

betas = np.matmul(np.linalg.inv(XT_X), XT_y)

# standard errors
res = y - np.matmul(X,betas)
resT = np.matrix.transpose(res)

VCM = np.true_divide(1,n-k)*np.matmul(resT,res)*np.linalg.inv(XT_X)
std = np.sqrt(VCM) # only the values in the diagonals

print(betas)
print(std)