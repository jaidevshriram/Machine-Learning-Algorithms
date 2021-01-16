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


yish = []
fname = "./Q1_data/data.pkl"
outfile = open(fname,'rb')

dataset = np.array(pickle.load(outfile))
outfile.close()
test_data = np.array([[]])
np.random.shuffle(dataset)
size = int(len(dataset)/10.0)
test_data = dataset[0:size,:]
dataset = np.delete(dataset,[i for i in range(0,size)],axis=0)

mean_bias =0
mean_variance = 0
coef_list = np.array([[]])
intercept_list = np.array([])

for i in range(1,10):
    x_train = np.copy([dataset[:,0]]).reshape(-1,1)
    y_train = np.copy([dataset[:,1]]).reshape(-1,1)
    x_test = np.copy([test_data[:,0]]).reshape(-1,1)
    y_test = np.copy([test_data[:,1]]).reshape(-1,1)
        
    
    size = int(x_train.shape[0]/10)
    full_size = x_train.shape[0]
    start =0
    end = size
    mean_bias =0
    mean_variance = 0
    coef_list = np.array([])
    intercept_list = np.array([])

    poly = PolynomialFeatures(i,include_bias=False)
    x_train = poly.fit_transform(x_train)
    
    poly = PolynomialFeatures(i,include_bias=False)
    x_test = poly.fit_transform(x_test)
    
    count = 0
    for xx in range(10):
        regressor = LinearRegression()  

        regressor.fit(x_train[start:end,:], y_train[start:end,:]) #training the algorithm

        #To retrieve the intercept:
        intercept = regressor.intercept_
        intercept_list = np.append(intercept_list,float(intercept))

        #For retrieving the slope:
        coef = regressor.coef_
        coef_list = np.append(coef_list,coef[0])

        start += size
        end += size
        count +=1
    coef_list=np.resize(coef_list,(10,i))
    for calc in range(int(test_data.shape[0])):
        mean_bias += bias_calc(x_test[calc,:],intercept_list,coef_list,y_test[calc,0])
        mean_variance += variance_calc(x_test[calc,:],intercept_list,coef_list)

    mean_bias /= test_data.shape[0]
    mean_variance /= test_data.shape[0]
    print("FOR DEGREE ",i)
    print(mean_bias)
    print(mean_variance)
    yish.append(mean_variance)

plt.plot([i for i in range(1,10)],yish)
plt.show()



