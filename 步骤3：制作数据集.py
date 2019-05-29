from geopy.distance import vincenty
import pandas as pd
import math
import numpy as np
import time
time_start = time.time()
with open("label2.txt", 'r') as ff:#label2.txt是没有加权值的标签
    label = eval(ff.read())
id_date = 30
while id_date <= 31:
    driver = open('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/大于25的司机id10-' + str(id_date) + '.txt', mode='r')
    print(id_date)
    label_list = []
    list_arrays = []
    for driver_id in driver:
        driver_id = driver_id.rstrip('\n')
        with open('E:/滴滴数据处理程序/单个司机数据文件/10-'+str(id_date)+'/司机' + driver_id + '.csv', mode='r', encoding='utf-8') as f:
            y = pd.read_csv(f)  #index_col=0指定第一列为行号,默认第一行为列标签，不读第一行
            tempSpeed = []
            a_speed = []
            aa_speed = []
            a_speed.append(np.nan)#加速度应该从第二次点时刻开始计算比较符合场景
            aa_speed.append(np.nan)  # 加加速度也从第二次点时刻开始计算，末尾补2个数
            timelist = []
            new_order_num = 1
            Bearing = []
            a_Bearing = []
            a_Bearing.append(np.nan)
            for i in range(len(y)-1):
                data_before = y.values[i]
                data_after = y.values[i+1]
                timelist.append(int(data_after[2])-int(data_before[2]))
                before_gps = eval(data_before[3])
                after_gps = eval(data_after[3])
                if data_after[1] != data_before[1]:
                    new_order_num += 1
                    tempSpeed.append(np.nan)
                    a_speed.append(np.nan)
                    Bearing.append(np.nan)
                    a_Bearing.append(np.nan)

                    if new_order_num > 50:
                        print('订单切换太多，说明共乘订单没有处理好')
                        exit()
                else:
                    tempSpeed.append(vincenty(before_gps, after_gps).meters / timelist[i])
                    # radians() 方法将角度转换为弧度  degrees() 将弧度转换为角度
                    yy = math.sin(math.radians(after_gps[0]) - math.radians(before_gps[0])) * math.radians(
                        math.cos(after_gps[1]))
                    xx = math.radians(math.cos(before_gps[1])) * math.radians(math.sin(after_gps[1])) - \
                         math.radians(math.sin(before_gps[1])) * math.radians(math.cos(after_gps[1])) \
                         * math.radians(math.cos(after_gps[0]) - math.radians(before_gps[0]))
                    # Convert radian from -pi to pi to [0, 360] degree
                    b = (math.atan2(yy, xx) * 180. / math.pi + 360) % 360
                    Bearing.append(b)
                    if i >= 1:
                        if np.isnan(tempSpeed[i]) or np.isnan(tempSpeed[i - 1]):
                            a_speed.append(np.nan)
                        else:
                            a_speed.append((tempSpeed[i] - tempSpeed[i - 1]) / timelist[i - 1])

                        if np.isnan(Bearing[i]) or np.isnan(Bearing[i - 1]):
                            a_Bearing.append(np.nan)
                        else:
                            a_Bearing.append((Bearing[i] - Bearing[i - 1]) / timelist[i - 1])
            for i in range(len(y) - 3):
                data_before = y.values[i]
                data_after = y.values[i + 1]
                if data_after[1] != data_before[1]:
                    aa_speed.append(np.nan)
                else:
                    if a_speed[i+1] == np.nan or a_speed[i] == np.nan:
                        aa_speed.append(np.nan)
                    else:
                        aa_speed.append((a_speed[i+1]-a_speed[i])/timelist[i])
            driver_id = data_before[0]
            tempSpeed.append(tempSpeed[-1]) #最后一组插入0否则不符合表的长度要求
            Bearing.append(Bearing[-1])
            a_Bearing.append(a_Bearing[-1])
            a_speed.append(a_speed[-1])
            aa_speed.append(aa_speed[-1])
            aa_speed.append(np.nan)
            y.insert(loc=4, column='speed', value=tempSpeed)
            y.insert(loc=5, column='a_speed', value=a_speed)
            y.insert(loc=6, column='aa_speed', value=aa_speed)
            y.insert(loc=7, column='bearing', value=Bearing)
            y.insert(loc=8, column='a_bearing', value=a_Bearing)
            print('****************************************')
            print('driver_id',driver_id)

            order_id = y.values[0][1]
            flag = 0
            for i in range(1,len(y)):#把它存成np.array
                if order_id == y.values[i][1]:
                    if flag == 0:
                        nparray_temp = np.delete(y.values[i], [0, 1, 2, 3, 7])
                        for er in range(4):
                            if np.isnan(nparray_temp[er]):
                                nparray_temp[er] = 0.0
                        flag = 1
                    else:
                        #nparray_temp1 = y.values[i]
                        nparray_temp1 = np.delete(y.values[i], [0, 1, 2, 3, 7])
                        for er in range(4):
                            if np.isnan(nparray_temp1[er]):
                                nparray_temp1[er] = 0.0
                        nparray_temp = np.vstack((nparray_temp,nparray_temp1))
                else:
                    #print(nparray_temp)
                    order_len = nparray_temp.shape[0]
                    #nparray_temp = np.nan_to_num(nparray_temp)
                    #print('订单长度为',order_len)
                    M = 100
                    Integer = int(order_len/M)
                    #print('Integer',Integer)
                    remainder = order_len%M
                    #print('remainder',remainder)
                    nn = Integer*M
                    temp = 0
                    while temp < Integer:
                        nparrays = nparray_temp[M*temp]
                        for index in range(1,M):
                            nparrays = np.vstack((nparrays,nparray_temp[index + M*temp]))
                        nparrays = np.reshape(nparrays,(1,100,4))
                        list_arrays.append(nparrays.tolist())
                        label_list.append(label[driver_id])
                        temp += 1
                    if remainder > M*0.75:
                        nparrays = nparray_temp[M * temp]
                        for index in range(1, remainder):
                            nparrays = np.vstack((nparrays, nparray_temp[index + M * temp]))
                        #补0，
                        num_0 = M - remainder
                        while num_0:
                            nparrays = np.vstack((nparrays, np.array([0.0,0.0,0.0,0.0])))
                            num_0 -= 1
                        label_list.append(label[driver_id])
                        nparrays = np.reshape(nparrays,(1,100,4))
                        list_arrays.append(nparrays.tolist())
                    order_id = y.values[i][1]#计算下一个订单信息
                    nparray_temp = np.delete(y.values[i], [0, 1, 2, 3, 7])
                    for er in range(4):
                        if np.isnan(nparray_temp[er]):
                            nparray_temp[er] = 0.0
    all_arrays = np.array(list_arrays)
    label_array = np.array(label_list)
    label_array = np.reshape(label_array, (-1, 1))
    np.save('E:/滴滴数据处理程序/单个司机数据文件/10-'+str(id_date)+'/'+'label_arrays2.npy', label_array)
    np.save('E:/滴滴数据处理程序/单个司机数据文件/10-'+str(id_date)+'/'+'all_arrays2.npy', all_arrays)

    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    id_date += 1

