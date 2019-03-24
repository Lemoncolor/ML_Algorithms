# encoding: utf-8
"""
 @project:ML_Algorithms
 @author: Jiang Hui
 @language:Python 3.7.2 [GCC 7.3.0] :: Anaconda, Inc. on linux
 @time: 3/24/19 1:43 PM
 @desc:
"""
"""
 1.AdaBoost算法的基本思路
 
    AdaBoost是adaptive boosting(自适应boosting)的缩写，它是训练一系列的弱学习器，最终组合成一个强学习器，训练过程如下：
    
    输入：训练数据集T={(x1,y1),(x2,y2),(x3,y3),...,(xN,yN),} ，其中xi为特征向量，yi∈{-1,+1}
    
    输出：最终分类器G(x)
    
    (1)初始化训练数据的权值分布(用向量D表示)
        D_1 = (w_1_1,w_1_2,w_1_3,...,w_1_N)  ， 其中 w_1_i  = 1/N ，i=1,2,3,...,N
    
    (2)假设有M个弱分类器，对m=1,2,3,...,M，有：
        (a)使用具有权值分布D_m的训练数据集学习，得到基本分类器G_m(x)
        
        (b)计算G_m(x)在训练数据集上的分类误差率e_m          !!! 注意计算误差率时要带上样本的权重哦
            e_m = sum w_mi * I(G_m(xi) != yi )  
            其中i=1,2,3,...,N，I(condition)为指示函数，True返回1，False返回0，w_mi表示第m个分类器训练时第i个样本的权重值
            
        (c)计算分类器G_m(x)的权重系数α_m
            α_m = 1/2 * log ((1-e_m) / e_m) ，log取自然对数，分类器的错误率越小，对应的权重就越大，在最终分类器中发挥的作用也就越大!
            
        (d)更新训练数据集的权重分布D_m+1
            D_m+1 = (w_m+1_1, w_m+1_2, w_m+1_3, ... , w_m+1_N)
            
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
    在上面讲述了AdaBoost算法的弱学习器的权重计算公式以及每一个样本的权重更新公式，现在来解释它们的由来.
    
    从另一个角度上来看，可以认为AdaBoost算法是 模型为加法模型，损失函数为指数函数、学习算法为前向分布算法 时的二类分类学习算法.
    
    (1)模型为加法模型好理解，因为我们的最终的强分类是若干个弱分类器加权平均得到的；
    
    (2)前向分布学习算法也好理解，我们的算法是通过一轮轮的弱学习器，利用前一个弱分类器的结果来更新后一个弱分类器的训练样本权重，迭代而成；
        比如说，第k-1轮的强学习器为：
            f_k-1(x) = sum α_i*G_i(x) ，其中 i = 1,2,3,...,k-1
        
        而第k轮的强学习器为：
            f_k(x) = sum α_i*G_i(x) ，其中 i = 1,2,3,...,k
        
        两式对比可知：
            f_k(x) = f_k-1(x) + α_k*G_k(x)  ， 可见强学习器的确是通过前向分步学习算法一步步而得到的
    
    (3)AdaBoost损失函数为指数函数，即定义损失函数为：
        
        L(y,f_k(x)) = exp(-y*f_k(x)) ， 其中(x,y)为样本特征和标签，f_k(x)为k个弱学习器最终线性组合成的强学习器
        
        其中，α_k和G_k(x)为：
            (α_k,G_k(x)) = arg min (sum exp(-yi*f_k(x))) ，i=1,2,3,...,N ，返回后面累加和最小时对应的α_k和G_k(x)
        
        利用前向学习算法的关系，可知：
            (α_k,G_k(x)) = arg min(sum exp(-yi*(f_k-1(x) + α*G(x)))) ，i=1,2,3,...,N ，返回后面累加和最小时对应的α_k和G_k(x).
            
        不妨令w_k_i = exp(-yi*f_k-1(x))，w_k_i是上一轮的值，不依赖于α_k和G_k(x)，所以与最小化无关，得：
            (α_k,G_k(x)) = arg min(sum w_ki_*exp(-yi*α*G(x)))
            
        首先，求满足损失函数最小时对应的G_k(x)，可得：
            G_k(x) = arg min(sum w_k_i * I(yi!=G(xi))) ，其中i=1,2,3,...,N
            
        将G_k(x)代入到损失函数，并对α求导，得到：
            α_k = 1/2 * log((1-e_k)/e_k) ，e_k为前面的分类误差率
            e_k = sum w_k_i*I(yi!=G(xi)) ，i=1,2,3,..,N
            
        最后看看样本权重的更新，由f_k(x) = f_k-1(x) + α_k*G_k(x) 和  w_ki_ = exp(-yi*f_k-1(x)) 得：
            w_k+1_i = w_k_i * exp(-yi*α_k*G_k(x))     
            
        因此，我们就得到了样本权重的更新式和弱分类器的权重计算式      
        
    
"""
