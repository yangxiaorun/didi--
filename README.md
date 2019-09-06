# didi--
滴滴轨迹处理
摘要：轨迹数据包含了丰富的地理空间信息与人类活动信息，其中通过浮动车轨迹信息可以分析驾驶员的驾驶风格，为驾驶员雇主、驾驶员以及车辆保险公司提供分析依据。本文利用原始轨迹数据，只包含时间与经纬度的二维序列，利用卷积神经网络将驾驶员按照驾驶风格分为危险、相对危险、相对安全、安全四种类型。本文的主要贡献在于创造性对利用卷积神经网络提取轨迹特征用于分析驾驶风格，以及将原始轨迹处理为CNN的输入的方法。经过对CNN网络的训练，合适的网络结构与参数的选择，本文的方法取得了74%的分类准确率。
