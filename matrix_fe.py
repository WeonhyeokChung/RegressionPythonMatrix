#-------------------------------------------------------
#   Weonhyeok Chung weonhyeok.chung@gmail.com
#   FE using Python Matrix
#   Feb-26-2022
#-------------------------------------------------------
import numpy as np 
import pandas as pd

df = pd.read_stata('matrix_fe.dta')  
df["intercept"] = 1

df = df[["intercept", "x1", "x2", "x3", "theta_i", "phi_j", "y"]]

X = df[["intercept", "x1", "x2", "x3"]].values
y = df[["y"]].values

n = X.shape[0]
k = X.shape[1]

###############################################################################
#                         OLS Regression
###############################################################################
# betas
XT = np.matrix.transpose(X)

XT_X = np.matmul(XT, X)
XT_y = np.matmul(XT, y)

betas_ols = np.matmul(np.linalg.inv(XT_X), XT_y)

# standard errors
res = y - np.matmul(X,betas_ols)
resT = np.matrix.transpose(res)

VCM = np.true_divide(1,n-k)*np.matmul(resT,res)*np.linalg.inv(XT_X)
std_ols = np.sqrt(VCM) # only the values in the diagonals

print(betas_ols)
print(std_ols)

###############################################################################
#                         FE Regression
###############################################################################

theta_dummies = pd.get_dummies(df["theta_i"])
phi_dummies = pd.get_dummies(df["phi_j"])

theta_dummies = theta_dummies.values
phi_dummies = phi_dummies.values

A = df[["intercept", "x1", "x2", "x3"]].values
A = np.concatenate((A, theta_dummies, phi_dummies), axis=1)

_k = A.shape[1]
# betas
_y = y-y.mean()
_X = A-A.mean()

_XT = np.matrix.transpose(_X)

_XT_X = np.matmul(_XT, _X)
_XT_y = np.matmul(_XT, _y)

betas_fe = np.matmul(np.linalg.inv(_XT_X), _XT_y)

print(betas_fe)

# standard errors
_res = _y - np.matmul(_X,betas_fe)
_resT = np.matrix.transpose(_res)

f_VCM = np.true_divide(1,n-_k)*np.matmul(_resT,_res)*np.linalg.inv(_XT_X)
std_fe = np.sqrt(f_VCM) # only the values in the diagonals

print(std_fe)

fe_sum = np.zeros(shape=(k-1,3))
fe_sum[0:k-1,0:1]=betas_fe[1:k,0:1]
for n in range(1,k): 
    fe_sum[n-1:n,1:2]=std_fe[n:n+1,n:n+1]

col_names    = ['coef', 'std','t']
row_names    = ['x1', 'x2', 'x3']
fe_output = pd.DataFrame(fe_sum, columns=col_names, index=row_names)

fe_output.to_excel (r'fe_output.xlsx', index = True, header=True)    
#fe_sum[0:1,1:2]=std_fe[1:2,1:2]
#fe_sum[1:2,1:2]=std_fe[2:3,2:3]

print(fe_sum)
# I am still in the process of updating t-statistics and p-value.
