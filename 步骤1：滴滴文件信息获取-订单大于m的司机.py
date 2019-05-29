import os
id_date = 10
while id_date <= 31:
    os.makedirs(r'E:\滴滴数据处理程序\司机订单大于20的集合\10-'+str(id_date))
    f = open('F:/滴滴数据西安10月/10-'+str(id_date)+'/xian/gps_201610'+str(id_date),encoding='utf-8',mode='r')
    newf = open('E:/滴滴数据处理程序/司机订单大于20的集合/10-'+str(id_date)+'/大于20的司机id10-'+str(id_date)+'.txt',mode='x')
    driver_num = 0
    Order_num = 0
    line_num = 0
    driver_id = ''
    Order_id = ''
    driverlist = []
    orderlist = []
    order_num_more_ten = 0
    for line in f:
        line_num += 1
        line = line.rstrip('\n').split(',')
        if driver_id != line[0]:
            if len(orderlist) > 20:
                order_num_more_ten += 1
                print(driver_id, '司机有', len(orderlist), '个订单')
                newf.write(driver_id+'\n')
            driver_num += 1
            driver_id = line[0]
            orderlist = []
        else:
            if line[1] not in orderlist:
                orderlist.append(line[1])
    f.close()
    newf.close()
    print('数据集中共有',line_num,'行数据')
    print('数据集中共有',driver_num,'位司机在开车')#17855位司机
    #print('20161001数据集中共有',Order_num,'个订单')
    print(str(id_date)+'号数据集中订单大于20的司机有',order_num_more_ten,'个')
    #20161001数据集中订单大于10的司机有 3839 个
    #20161001数据集中订单大于15的司机有 1265 个
    #20161001数据集中订单大于20的司机有 261 个
    #20161001数据集中订单大于25的司机有 34 个

    driver = open('E:/滴滴数据处理程序/司机订单大于20的集合/10-'+str(id_date)+'/大于20的司机id10-'+str(id_date)+'.txt',mode='r')
    f = open('F:/滴滴数据西安10月/10-'+str(id_date)+'/xian/gps_201610'+str(id_date),encoding='utf-8',mode='r')
    driver_id = driver.readline().rstrip('\n')
    nem = 0
    for line in f:
        line1 = line.rstrip('\n').split(',')
        if driver_id == line1[0]:
            if nem == 0:
                newf = open('E:/滴滴数据处理程序/司机订单大于20的集合/10-'+str(id_date)+'/司机' + driver_id + '.csv', mode='w', encoding='utf-8')
                newf.write('driver_id' + ',' + 'order_id' + ',' + 'time' + ',' + 'long_lat\n')
                datalist = []
                datalist.append([line1[0],line1[1],int(line1[2]),line1[3],line1[4]])
                nem = 1
            elif nem == 1:
                datalist.append([line1[0], line1[1], int(line1[2]), line1[3], line1[4]])
        else:
            if nem == 1:
                datalist.sort(key=lambda x: (x[1], x[2]))
                for data in datalist:
                    newf.write(data[0] + ',' + data[1] + ',' + str(data[2]) + ',' + '"' + data[3] + ',' + data[
                        4] + '"' + '\n')  # 直接处理成高德地图要求的数据格式
                newf.close()
                driver_id = driver.readline().rstrip('\n')
                print(driver_id)
                nem = 0
    f.close()
    id_date += 1