import numpy as np
id_date = 2
Train_X = np.load('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/all_arrays2.npy', allow_pickle=True)
Train_Y = np.load('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/label_arrays.npy', allow_pickle=True)
while id_date <= 28:
    Train_X1 = np.load('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/all_arrays2.npy', allow_pickle=True)
    Train_Y1= np.load('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/label_arrays2.npy', allow_pickle=True)
    Train_X = np.vstack((Train_X,Train_X1))
    Train_Y = np.vstack((Train_Y,Train_Y1))
    id_date += 1
id_date = 30
Train_X1 = np.load('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/all_arrays2.npy', allow_pickle=True)
Train_Y1= np.load('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/label_arrays2.npy', allow_pickle=True)
Train_X = np.vstack((Train_X,Train_X1))
Train_Y = np.vstack((Train_Y,Train_Y1))
id_date = 31
Train_X1 = np.load('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/all_arrays2.npy', allow_pickle=True)
Train_Y1= np.load('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/label_arrays2.npy', allow_pickle=True)
Train_X = np.vstack((Train_X,Train_X1))
Train_Y = np.vstack((Train_Y,Train_Y1))
print(Train_X.shape)
print(Train_Y.shape)
np.save('all_arrays2.npy',Train_X)
np.save('label_arrays2.npy',Train_Y)