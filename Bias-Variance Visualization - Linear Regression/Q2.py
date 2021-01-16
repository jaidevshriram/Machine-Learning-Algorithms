import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt

def hypotheis(xt,intercepts,coeff):
    intercept = np.copy(intercepts)
    coef = np.copy(coeff)
    x = np.copy(xt) 
    x = np.transpose(x)
    hyp = coeff.dot(x)
    hyp += intercept
    return hyp


def variance_calc(xt,intercepts,coeff):
    intercept = np.copy([intercepts])
    coef = np.copy(coeff)
    x = np.copy([xt])
    intercept = np.array([intercept]).reshape(-1,1)


    hyp = hypotheis(x,intercept,coef)
    
    expec_hyp =np.sum(hyp)
    expec_hyp /= intercept.size

    expec_hyp_list = np.array([expec_hyp for i in range(intercept.size)]).reshape(-1,1)

    temp = hyp-expec_hyp_list
    temp = np.square(temp)
    variance = np.sum(temp)
    variance /= intercept.size
    

    return variance




def bias_calc(xt,intercepts,coeff,ans):
    intercept = np.copy([intercepts])
    coef = np.copy(coeff)
    x = np.copy([xt])
    intercept = np.array([intercept]).reshape(-1,1)
    hyp = hypotheis(x,intercept,coef)
    expec_hyp =np.sum(hyp)
    expec_hyp /= intercept.size
    bias = abs(expec_hyp-ans)
    return bias

fname = "./Q2_data/X_train.pkl"
outfile = open(fname,'rb')
X_train = np.array(pickle.load(outfile))
outfile.close()

fname = "./Q2_data/Y_train.pkl"
outfile = open(fname,'rb')
Y_train = np.array(pickle.load(outfile))
outfile.close()

fname = "./Q2_data/X_test.pkl"
outfile = open(fname,'rb')
X_test = np.array(pickle.load(outfile))
outfile.close()

fname = "./Q2_data/Fx_test.pkl"
outfile = open(fname,'rb')
Y_test = np.array(pickle.load(outfile))
outfile.close()

X_test = np.array([X_test]).reshape(-1,1)
Y_test = np.array([Y_test]).reshape(-1,1)

mean_bias =0
mean_variance = 0
coef_list = np.array([[]])
intercept_list = np.array([])

sih = []

for degree in range(1,10):
    
    mean_bias =0
    mean_variance = 0
    coef_list = np.array([[]])
    intercept_list = np.array([])
    
    x_test = np.copy(X_test)
    
    for model in range(0,20):
        cur_x_train = X_train[model,:].reshape(-1,1)
        cur_y_train = Y_train[model,:].reshape(-1,1)
        cur_dataset = np.append(cur_x_train,cur_y_train,axis=1)
        np.random.shuffle(cur_dataset)
        cur_x_train = cur_dataset[:,0].reshape(-1,1)
        cur_y_train = cur_dataset[:,1].reshape(-1,1)

        poly = PolynomialFeatures(degree,include_bias=False)
        cur_x_train = poly.fit_transform(cur_x_train)

        regressor = LinearRegression()  
        regressor.fit(cur_x_train, cur_y_train)

        intercept = regressor.intercept_
        intercept_list = np.append(intercept_list,float(intercept))

        coef = regressor.coef_
        coef_list = np.append(coef_list,coef[0])


    coef_list=np.resize(coef_list,(20,degree))
    poly = PolynomialFeatures(degree,include_bias=False)
    x_test = poly.fit_transform(x_test)

    
    for calc in range(int(X_test.shape[0])):
        mean_bias += bias_calc(x_test[calc,:],intercept_list,coef_list,Y_test[calc,0])
        mean_variance += variance_calc(x_test[calc,:],intercept_list,coef_list)

    mean_bias/= (x_test.shape[0])
    mean_variance/= (x_test.shape[0])

    sih.append(mean_bias**2)

    print("FOR DEGREE ",degree)
    print(mean_bias**2,mean_variance)

plt.plot([i for i in range(1,10)],sih)
plt.show()

