# encoding: utf-8
"""
 @project:ML_Algorithms
 @author: Jiang Hui
 @language:Python 3.7.2 [GCC 7.3.0] :: Anaconda, Inc. on linux
 @time: 3/24/19 1:43 PM
 @desc: 针对AdaBoost算法的分类与回归两种实现方式给出算法原理解释，代码暂无!
"""
"""
 1.AdaBoost算法分类问题的基本思路
 
    AdaBoost是adaptive boosting(自适应boosting)的缩写，它是训练一系列的弱学习器，最终组合成一个强学习器，训练过程如下：
    
    输入：训练数据集T={(x1,y1),(x2,y2),(x3,y3),...,(xN,yN),} ，其中xi为特征向量，yi∈{-1,+1}
    
    输出：最终分类器G(x)，G(x) = sign(f(x))，f(x) = α_1*G_1(x) + α_2*G_2(x) + α_3*G_3(x) +...+ α_m*G_m(x)
    
    (1)初始化训练数据的权值分布(用向量D表示)
        D_1 = (w_1_1,w_1_2,w_1_3,...,w_1_N)  ， 其中 w_1_i  = 1/N ，i=1,2,3,...,N
    
    (2)假设有M个弱分类器，对m=1,2,3,...,m，有：
        (a)使用具有权值分布D_m的训练数据集学习，得到基本分类器G_m(x)
            G_m(x)的输出为{+1,-1}，表示第m个弱分类器的输出为±1，m=1,2,3,...,M
        
        (b)计算G_m(x)在训练数据集上的分类误差率e_m  
            e_m = sum w_m_i * I(G_m(xi) != yi )       其中i=1,2,3,...,N，w_m_i表示第m个分类器训练时第i个样本的权重值
            
        (c)计算分类器G_m(x)的权重系数α_m
            α_m = 1/2 * log ((1-e_m) / e_m) ，log取自然对数，分类器的错误率越小，对应的权重就越大，在最终分类器中发挥的作用也就越大!
            
        (d)更新训练数据集的权重分布D_m+1
            D_m+1 = (w_m+1_1, w_m+1_2, w_m+1_3, ... , w_m+1_N)      【这里把 m+1 当成一个整体看待!】
            
            其中，对于第i个样本的权重更新式为：
                 w_m+1_i = w_m_i * exp(-α_m*yi*G_m(xi))
            
            当G_m(xi) = yi时:    
                 w_m+1_i = w_m_i * exp(-α_m) / Z_m 
                 
            当G_m(xi) != yi时:
                 w_m+1_i = w_m_i * exp(α_m)  / Z_m 
                 
            Z_m是规范化因子，它是第m个分类器对应的数据集的权重之和，作用是让所有样本权重归一化
    
    (3)构建基本分类器的线性组合
        G(x) = sign(sum α_m*G_m(x))，其中m=1,2,3,..,M，这里的α_m之和并不为1，最终得出m个分类器的加权和，再用sign函数进行转换为±1
    
    推荐阅读《统计学习方法》P140 例8.1来熟悉AdaBoost的算法过程
    
 2.AdaBoost分类问题的损失函数优化
    在上面讲述了AdaBoost算法的弱学习器的权重α_m的计算公式以及每一个样本的权重w_m_i的更新公式，现在来解释它们的由来.
    
    从另一个角度上来看，可以认为AdaBoost算法是(模型为加法模型，损失函数为指数函数、学习算法为前向分布算法)时的二类分类学习算法.
    
    (1)模型为加法模型好理解，因为我们的最终的强分类器是若干个弱分类器加权平均得到的；
    
    (2)前向分布学习算法也好理解，我们的算法是通过一轮轮的弱学习器，利用前一个弱分类器的结果来更新后一个弱分类器的训练样本权重，迭代而成；
        比如说，第m-1轮的强学习器为：
            f_m-1(x) = sum α_i*G_i(x) ，其中 i = 1,2,3,...,m-1     【这里把 m-1 当成一个整体看待!】
        
        而第k轮的强学习器为：
            f_m(x) = sum α_i*G_i(x) ，其中 i = 1,2,3,...,m
        
        两式对比可知：
            f_m(x) = f_m-1(x) + α_k*G_m(x)  ， 可见强学习器的确是通过前向分步学习算法一步步而得到的
            
        前向分布算法具有专门的求解思路，损失函数为 L(y,f(x)) ，f(x) = sum β_i*b_i(x) ,i=1,2,3,...,m
        而f(x) = sum β_i*b_i(x) + β_m*b_m(x) , i = 1,2,3,...,m-1
        而假设我们经过m-1轮的迭代，β_1*b_1(x) + β_2*b_2(x) + β_3*b_3(x) +...+ β_m-1 * b_m-1(x) 已经定下来了，
        那么我们按照从后往前的顺序，每次只优化一组基函数b_m(x)及其系数β_m即可! AdaBoost算法就是前项分布算法的特例.
        
            
    (3)AdaBoost损失函数为指数函数，即定义损失函数为：
        
        一个样本(x,y)所带来的损失为:
        L(y,f_m(x)) = exp(-y*f_m(x))      其中f_m(x) = α_1*G_1(x) + α_2*G_2(x) + α_3*G_3(x) +...+ α_m*G_m(x)
        
        定义α_m和G_m(x)为损失最小时对应的系数和基函数：
            α_m,G_m(x) = arg min (sum exp(-yi*f_m(xi)))         (其中i=1,2,3,...,N)
        
        利用前向学习算法的关系，可知：
            α_m,G_m(x) = arg min(sum exp(-yi*(f_m-1(xi) + α*G(xi))))        (其中i=1,2,3,...,N) 
            
        不妨令w_m_i' = exp(-yi*f_m-1(xi)) ， w_m_i' 是上一轮的值，不依赖于α_m和G_m(x)，所以与最小化无关，得：
            α_m,G_m(x) = arg min(sum w_m_i' * exp(-yi*α*G(xi)))
            
        首先，我们定义每一个分类器的权重系数α是大于等于0的，于是G_m(x) = arg min(sum w_m_i' * exp(-yi*α*G(xi))) 等价于
            G_m(x) = arg min(sum w_m_i' * exp(-yi*G(xi)))       其中 yi*G(xi) = ±1
            
        然后，根据性质 “极小化指数函数等价于最小化分类误差”，参考《统计学习方法》P143 定理8.1   可将上式等价转换为:
            G_m(x) = arg min(sum w_m_i' * I(yi!=G(xi)))         其中I(yi!=G(xi)) = 0或1
            
        将G_k(x)代入到损失函数，并对α求导，得到最优解α_m：
            α_m = 1/2 * log((1-e_m)/e_m)                        其中e_m为分类误差率
            
            e_m = sum w_m_i' * I(yi!=G(xi)) / sum w_m_i'        其中i=1,2,3,..,N 
                = sum w_m_i * I(yi!=G(xi))                      其中w_m_i为第m轮训练中第i个样本的权重
        
        最后看看样本权重的更新，由f_m(x) = f_m-1(x) + α_k*G_m(x) 和  w_m_i' = exp(-yi*f_k-1(xi)) 得：
        
            w_k+1_i' = w_k_i' * exp(-yi*α_k*G_k(x)) , 与前面样本权重的更新式只差归一化因子，因而等价   
            
        因此，我们就得到了样本权重的更新式和弱分类器的权重计算式.      
        
 3.AdaBoost回归问题的算法流程
    
    输入：训练数据集T={(x1,y1),(x2,y2),(x3,y3),...,(xN,yN),} ，其中xi为特征向量，yi∈{-1,+1}
    
    输出：最终分类器f(x)

    (1)初始化训练数据的权值分布(用向量D表示)
        D_1 = (w_1_1,w_1_2,w_1_3,...,w_1_N)  ， 其中 w_1_i  = 1/N ，i=1,2,3,...,N
    
    (2)假设有M个弱分类器，对m=1,2,3,...,m，有
        (a)使用具有权值分布D_m的训练数据集学习，得到基本分类器G_m(x)
            G_m(x)的输出为{+1,-1}，表示第m个弱分类器的输出为±1，m=1,2,3,...,M
        
        (b)计算训练集上的最大误差E_max
            E_max = max |yi-G_m(xi)|   ，其中i=1,2,3,...,N
            
        (c)计算每个样本的相对误差
            如果是线性误差，则e_m_i = |yi-G_m(xi)| / E_max
            如果是平方误差，则e_m_i = (yi-G_m(xi))^2 / E_max^2
            如果是指数误差，则e_m_i = 1 - exp(-|yi-G_m(xi)| / E_max)
        
        (d)计算回归误差率
            e_m = sum w_m_i*e_k_i  ，i=1,2,3,..,N
            
        (e)计算弱学习器的系数α_m
            α_m = 1/2 * log ((1-e_m) / e_m)
        
        (f)更新样本集的权重分布
            w_m+1_i = w_m_i * α_m^(1-e_m_i) / Z_m  ，Z_m为归一化因子，第m+1轮所有样本权重之和
        
        (g)构建最终强学习器：
            f(x) = G_k* (x)   其中k*是一个整体，G_k* (x)是将 ln 1/α_k，k=1,2,3,..,m，排完序的中位数对应序号k*对应的弱学习器.
            
 4.AdaBoost算法的正则化
    为了防止AdaBoost过拟合，我们通常会加入正则化项，通常称为步长(learning rate)，定义为ν，对于弱学习器的迭代
            f_m(x) = f_m-1(x) + α_m*G_m(x)
    
    加上正则化项之后，则有:
            f_m(x) = f_m-1(x) + ν*α_m*G_m(x)    v的取值范围为0<ν≤1，
    
    对于同样的训练集学习效果，较小的ν意味着我们需要更多的弱学习器的迭代次数，通常我们用步长和迭代最大次数一起来决定算法的拟合效果
    
 5.AdaBoost小结
    理论上，任何学习器都可以用于AdaBoost，但是一般来说，使用最广泛的AdaBoost弱学习器是决策树(CART)和神经网络
    
    优点:
        (1)AdaBoost作为分类器时，分类精度很高
        (2)泛化错误率低，不容易发生过拟合(调节正则化参数)
        (3)可以选择的弱学习器很多，十分灵活
        
    缺点:
        (1)对异常样本敏感，异常样本在迭代中可能会获得较高的权重，影响最终的强学习器的预测准确性
"""
