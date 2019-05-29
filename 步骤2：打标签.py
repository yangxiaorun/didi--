from geopy.distance import vincenty #vincenty公式  精度很高能达到0.5毫米，但是很慢
import pandas as pd
import math
import numpy as np
id_date = 1
while id_date <= 31:
    driver = open('E:/滴滴数据处理程序/单个司机数据文件/10-' + str(id_date) + '/大于25的司机id10-' + str(id_date) + '.txt', mode='r')
    print(id_date)
    for driver_id in driver:
        driver_id = driver_id.rstrip('\n')
        with open('E:/滴滴数据处理程序/单个司机数据文件/10-'+str(id_date)+'/司机' + driver_id + '.csv', mode='r', encoding='utf-8') as f:
            y = pd.read_csv(f)  #index_col=0指定第一列为行号,默认第一行为列标签，不读第一行
            tempSpeed = []
            a_speed = []
            aa_speed = []
            a_speed.append(np.nan)#加速度应该从第二次点时刻开始计算比较符合场景
            time = []
            new_order_num = 1
            v_more_167_num = 0 #车速超过16.7m/s的数量（60km/h）
            v_exist_num =0 #存在速度值的数量，有些轨迹点速度是空值
            a_v_more_pos02_num = 0 #加速度大于0.2的数量
            a_v_more_neg02_num = 0 #加速度小于-0.2的数量
            a_v_exist_num = 0 #加速度存在的数量
            for i in range(len(y)-1):
                data_before = y.values[i]
                data_after = y.values[i+1]
                time.append(int(data_after[2])-int(data_before[2]))
                before_gps = eval(data_before[3])
                after_gps = eval(data_after[3])
                if data_after[1] != data_before[1]:
                    new_order_num += 1
                    tempSpeed.append(np.nan)
                    a_speed.append(np.nan)
                    if new_order_num > 50:
                        print('订单切换太多，说明共乘订单没有处理好')
                        exit()
                else:
                    tempspeed = vincenty(before_gps, after_gps).meters / time[i]
                    tempSpeed.append(tempspeed)
                    v_exist_num += 1
                    if tempspeed > 16.7:
                        v_more_167_num += 1
                    if i >= 1:
                        if tempSpeed[i] == np.nan or tempSpeed[i-1] == np.nan:
                            a_speed.append(np.nan)
                        else:
                            temp_a_speed = (tempSpeed[i]-tempSpeed[i-1])/time[i-1]
                            a_v_exist_num += 1
                            a_speed.append(temp_a_speed)
                            if temp_a_speed > 3:
                                a_v_more_pos02_num += 1
                            elif temp_a_speed < -3:
                                a_v_more_neg02_num += 1
            for i in range(len(y) - 3):
                data_before = y.values[i]
                data_after = y.values[i + 1]
                if data_after[1] != data_before[1]:
                    aa_speed.append(np.nan)
                else:
                    if a_speed[i+1] == np.nan or a_speed[i] == np.nan:
                        aa_speed.append(np.nan)
                    else:
                        aa_speed.append((a_speed[i+1]-a_speed[i])/time[i])

            driver_id = data_before[0]
            tempSpeed.append(tempSpeed[-1]) #最后一组插入0否则不符合表的长度要求
            a_speed.append(a_speed[-1])
            aa_speed.append(aa_speed[-1])
            aa_speed.append(np.nan)

            print('****************************************')
            print('driver_id',driver_id)
            print('速度超过60km/h的比率',v_more_167_num/v_exist_num)
            print('加速度绝对值超过3的比例', (a_v_more_neg02_num + a_v_more_pos02_num)/a_v_exist_num)
            print('加速度超过3的比例', a_v_more_pos02_num / a_v_exist_num)
            print('加速度小于-3的比例', a_v_more_neg02_num / a_v_exist_num)
            columns_name = ['date','driver_id','num_order','average_order_num',
                            'speed_mean','speed_var','speed_max',
                            'a_speed_mean','a_speed_var','a_speed_max','a_speed_min',
                            'aa_speed_mean','aa_speed_var','aa_speed_max','aa_speed_min',
                            'rate of v over 60km/h','rate of over 3','rate of less -3','rate of over |3|']
            df = pd.DataFrame(columns=columns_name)
            df.loc[0] = [id_date,driver_id,new_order_num,len(y)/new_order_num,
                         np.nanmean(tempSpeed),np.nanvar(tempSpeed),np.nanmax(tempSpeed),
                         np.nanmean(a_speed),np.nanvar(a_speed),np.nanmax(a_speed),np.nanmin(a_speed),
                         np.nanmean(aa_speed),np.nanvar(aa_speed),np.nanmax(aa_speed),np.nanmin(aa_speed),
                         v_more_167_num/v_exist_num,a_v_more_pos02_num/a_v_exist_num,a_v_more_neg02_num /a_v_exist_num,
                         (a_v_more_neg02_num + a_v_more_pos02_num)/a_v_exist_num]
            df.to_csv('标签.csv', mode='a', index=False, header=False)
    id_date += 1

#把标签存入字典，并存入文件
'''
label = {}
with open('标签2.csv', mode='r', encoding='utf-8') as f:
    y = pd.read_csv(f)
    for i in range(len(y)):
        label[y.values[i][1]] = y.values[i][-1]
ff = open("label.txt", 'w')
ff.write(str(label))
ff.close()
'''