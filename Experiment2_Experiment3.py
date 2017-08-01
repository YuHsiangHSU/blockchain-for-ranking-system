
# coding: utf-8

# ## 將資料做亂數排序（Shuffle）

# In[16]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

data = pd.read_csv("ratings.csv")
data.convert_objects(convert_numeric=True).dtypes


'''
#################
no_shuffle_final_group = data.groupby('userId').userId.count()
all_index = no_shuffle_final_group.index.values
#################
'''
'''
#################
df_to_list = data.values.tolist()


import random

r = {a: random.random() for a, b, c, d in df_to_list}
df_to_list.sort(key=lambda item: r[item[0]])

shuffle_final = pd.DataFrame(df_to_list)
#print (shuffle_final)
shuffle_final.columns = ['userId','movieId','rating','timestamp']
#print (shuffle_final)
shuffle_final_group = shuffle_final.groupby('userId').userId.count()
#print (shuffle_final_group.index)
all_index = shuffle(shuffle_final_group.index.values)
#print (all_index)
###################
'''
all_index = shuffle(data)

#all_index = all_index_1.values.tolist()

'''
import random

r = {e: random.random() for a, b, c, d, e in df_to_list}
#df_to_list.sort()

shuffle_final = pd.DataFrame(df_to_list)
#print (shuffle_final)
shuffle_final.columns = ['userId','movieId','rating','timestamp','index']
print (shuffle_final)
#shuffle_final_group = shuffle_final.userId.count()
#print (shuffle_final_group.index)
all_index = shuffle(shuffle_final)
'''
print (all_index)


# ## 驗證多小的樣本可以使用本評分優化系統使評分優化，則相製作相關趴數的小樣本的暫存檔

# In[17]:

#10%_data
rating_adjust_41 =all_index[:2440410]
#print (rating_adjust_41)
rating_adjust_41.to_csv('ratings_adjust_few_1.csv', index=False)

#20%_data
rating_adjust_42 =all_index[:4880819]
#print (rating_adjust_42)
rating_adjust_42.to_csv('ratings_adjust_few_2.csv', index=False)

#30%_data
rating_adjust_43 =all_index[:7321229]
#print (rating_adjust_43)
rating_adjust_43.to_csv('ratings_adjust_few_3.csv', index=False)

#40%_data
rating_adjust_44 =all_index[:9761638]
#print (rating_adjust_44)
rating_adjust_44.to_csv('ratings_adjust_few_4.csv', index=False)

#50%_data
rating_adjust_45 =all_index[:12202049]
#print (rating_adjust_45)
rating_adjust_45.to_csv('ratings_adjust_few_5.csv', index=False)

#60%_data
rating_adjust_46 =all_index[:14642458]
#print (rating_adjust_46)
rating_adjust_46.to_csv('ratings_adjust_few_6.csv', index=False)

#70%_data
rating_adjust_47 =all_index[:17082867]
#print (rating_adjust_47)
rating_adjust_47.to_csv('ratings_adjust_few_7.csv', index=False)

#80%_data
rating_adjust_48 =all_index[:19523278]
#print (rating_adjust_48)
rating_adjust_48.to_csv('ratings_adjust_few_8.csv', index=False)

#90%_data
rating_adjust_49 =all_index[:21963687]
#print (rating_adjust_49)
rating_adjust_49.to_csv('ratings_adjust_few_9.csv', index=False)

'''
#20%_data
fetch_front = all_index[:4880819]
#print (fetch_front)
rating_adjust_42 = data[data['userId'].isin(fetch_front)]
#print (rating_adjust_42)
rating_adjust_42.to_csv('ratings_adjust_full_2.csv', index=False)
      
#30%_data
fetch_front = all_index[:7321229]
#print (fetch_front)
rating_adjust_43 = data[data['userId'].isin(fetch_front)]
#print (rating_adjust_43)
rating_adjust_43.to_csv('ratings_adjust_full_3.csv', index=False)

#40%_data
fetch_front = all_index[:9761638]
#print (fetch_front)
rating_adjust_44 = data[data['userId'].isin(fetch_front)]
print (rating_adjust_44)
rating_adjust_44.to_csv('ratings_adjust_full_4.csv', index=False)

#50%_data
fetch_front = all_index[:12202049]
#print (fetch_front)
rating_adjust_45 = data[data['userId'].isin(fetch_front)]
print (rating_adjust_45)
rating_adjust_45.to_csv('ratings_adjust_full_5.csv', index=False)

#60%_data
fetch_front = all_index[:14642458]
#print (fetch_front)
rating_adjust_46 = data[data['userId'].isin(fetch_front)]
print (rating_adjust_46)
rating_adjust_46.to_csv('ratings_adjust_full_6.csv', index=False)

#70%_data
fetch_front = all_index[:17082867]
#print (fetch_front)
rating_adjust_47 = data[data['userId'].isin(fetch_front)]
print (rating_adjust_47)
rating_adjust_47.to_csv('ratings_adjust_full_7.csv', index=False)

#80%_data
fetch_front = all_index[:19523278]
#print (fetch_front)
rating_adjust_48 = data[data['userId'].isin(fetch_front)]
print (rating_adjust_48)
rating_adjust_48.to_csv('ratings_adjust_full_8.csv', index=False)


#90%_data
fetch_front = all_index[:21963687]
#print (fetch_front)
rating_adjust_49 = data[data['userId'].isin(fetch_front)]
print (rating_adjust_49)
rating_adjust_49.to_csv('ratings_adjust_full_9.csv', index=False)
'''


# ## 將所有的電影/餐廳資料做調整

# In[62]:

#df.assign(normalized=df.bought.div(df.user.map(df.groupby('user').bought.sum())))
import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data = pd.read_csv("ratings_res.csv")
data.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min = data.assign(normalized=data.rating.subtract(data.userId.map(data.groupby('userId').rating.mean())))
data_nor = data_min.assign(normalized=data_min.normalized.div(data_min.userId.map(data_min.groupby('userId').normalized.std())))
data_nor = data_nor.fillna(0)

#將正規化的分數做非線性調整
data_change = ((data_nor['normalized']-min(data_nor['normalized'])) / (max(data_nor['normalized']) - min(data_nor['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor['data_change'] = data_change
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor['data_change']))
print (min(data_nor['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new = result.assign(normalized_second=data_nor.data_change.subtract(result.movieId.map(result.groupby('movieId').data_change.mean())))
data_nor_new = data_min_new.assign(normalized_second=data_min_new.normalized_second.div(data_min_new.movieId.map(data_min_new.groupby('movieId').normalized_second.std())))
data_final = data_nor_new.assign(normalized_second=abs(data_nor_new['normalized_second']))
data_final_2 = data_final.sort(['movieId'])
#print (data_final_2)


# In[63]:

#total_len = int(len(data_final.index))
data_final['credit'] = np.where(data_final['normalized_second'] <= 2*data_final['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())


group_mean = data_final.assign(credit_sum=data_final.userId.map(data_final.groupby('userId').credit.mean()))
#print (group_mean)

total_score = group_mean.assign(adj_rating=(group_mean['rating'] + group_mean['rating']*group_mean['credit_sum'])/2)
grouped_sum_all = total_score.groupby('movieId').adj_rating.mean()
#print (grouped_sum_all)

print (max(grouped_sum_all))
print (min(grouped_sum_all))
grouped_sum_all.to_csv('grouped_sum_all.csv')


# ## 分別將九組與全部調整資料做比較的小樣本做分數調整

# In[64]:

#df.assign(normalized=df.bought.div(df.user.map(df.groupby('user').bought.sum())))
import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data = pd.read_csv("ratings_adjust_full_res_1.csv")
data.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min = data.assign(normalized=data.rating.subtract(data.userId.map(data.groupby('userId').rating.mean())))
data_nor = data_min.assign(normalized=data_min.normalized.div(data_min.userId.map(data_min.groupby('userId').normalized.std())))
data_nor = data_nor.fillna(0)

#將正規化的分數做非線性調整
data_change = ((data_nor['normalized']-min(data_nor['normalized'])) / (max(data_nor['normalized']) - min(data_nor['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor['data_change'] = data_change
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor['data_change']))
print (min(data_nor['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new = result.assign(normalized_second=data_nor.data_change.subtract(result.movieId.map(result.groupby('movieId').data_change.mean())))
data_nor_new = data_min_new.assign(normalized_second=data_min_new.normalized_second.div(data_min_new.movieId.map(data_min_new.groupby('movieId').normalized_second.std())))
data_final = data_nor_new.assign(normalized_second=abs(data_nor_new['normalized_second']))


# In[65]:

#total_len = int(len(data_final.index))
data_final['credit'] = np.where(data_final['normalized_second'] <= 2*data_final['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())


group_mean = data_final.assign(credit_sum=data_final.userId.map(data_final.groupby('userId').credit.mean()))
#print (group_mean)

total_score = group_mean.assign(adj_rating=(group_mean['rating'] + group_mean['rating']*group_mean['credit_sum'])/2)
grouped_sum = total_score.groupby('movieId').adj_rating.mean()
#print (grouped_sum)

print (max(grouped_sum))
print (min(grouped_sum))

grouped_sum.to_csv('grouped_sum.csv')


# 第二次

# In[66]:

import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data_2 = pd.read_csv("ratings_adjust_full_res_2.csv")
data_2.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min_2 = data_2.assign(normalized=data_2.rating.subtract(data_2.userId.map(data_2.groupby('userId').rating.mean())))
data_nor_2 = data_min_2.assign(normalized=data_min_2.normalized.div(data_min_2.userId.map(data_min_2.groupby('userId').normalized.std())))
data_nor_2 = data_nor.fillna(0)

#將正規化的分數做非線性調整
data_change_2 = ((data_nor_2['normalized']-min(data_nor_2['normalized'])) / (max(data_nor_2['normalized']) - min(data_nor_2['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor_2['data_change'] = data_change_2
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor_2['data_change']))
print (min(data_nor_2['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp_2 = data_nor_2.assign(normalized_std=data_nor_2.movieId.map(data_nor_2.groupby('movieId').data_change.std()))
result_2 = temp_2.assign(normalized_mean=temp_2.movieId.map(temp_2.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new_2 = result_2.assign(normalized_second=data_nor_2.data_change.subtract(result_2.movieId.map(result_2.groupby('movieId').data_change.mean())))
data_nor_new_2 = data_min_new_2.assign(normalized_second=data_min_new_2.normalized_second.div(data_min_new_2.movieId.map(data_min_new_2.groupby('movieId').normalized_second.std())))
data_final_2 = data_nor_new_2.assign(normalized_second=abs(data_nor_new_2['normalized_second']))


# In[67]:

data_final_2['credit'] = np.where(data_final_2['normalized_second'] <= 2*data_final_2['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())

group_mean_2 = data_final_2.assign(credit_sum=data_final_2.userId.map(data_final_2.groupby('userId').credit.mean()))
#print (group_mean)

total_score_2 = group_mean_2.assign(adj_rating=(group_mean_2['rating'] + group_mean_2['rating']*group_mean_2['credit_sum'])/2)
grouped_sum_2 = total_score_2.groupby('movieId').adj_rating.mean()
#print (grouped_sum_2)

print (max(grouped_sum_2))
print (min(grouped_sum_2))
grouped_sum_2.to_csv('grouped_sum_2.csv')


# 第三筆

# In[68]:

import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data_3 = pd.read_csv("ratings_adjust_full_res_3.csv")
data_3.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min_3 = data_3.assign(normalized=data_3.rating.subtract(data_3.userId.map(data_3.groupby('userId').rating.mean())))
data_nor_3 = data_min_3.assign(normalized=data_min_3.normalized.div(data_min_3.userId.map(data_min_3.groupby('userId').normalized.std())))
data_nor_3 = data_nor.fillna(0)

#將正規化的分數做非線性調整
data_change_3 = ((data_nor_3['normalized']-min(data_nor_3['normalized'])) / (max(data_nor_3['normalized']) - min(data_nor_3['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor_3['data_change'] = data_change_3
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor_3['data_change']))
print (min(data_nor_3['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp_3 = data_nor_3.assign(normalized_std=data_nor_3.movieId.map(data_nor_3.groupby('movieId').data_change.std()))
result_3 = temp_3.assign(normalized_mean=temp_3.movieId.map(temp_3.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new_3 = result_3.assign(normalized_second=data_nor_3.data_change.subtract(result_3.movieId.map(result_3.groupby('movieId').data_change.mean())))
data_nor_new_3 = data_min_new_3.assign(normalized_second=data_min_new_3.normalized_second.div(data_min_new_3.movieId.map(data_min_new_3.groupby('movieId').normalized_second.std())))
data_final_3 = data_nor_new_3.assign(normalized_second=abs(data_nor_new_3['normalized_second']))


# In[69]:

data_final_3['credit'] = np.where(data_final_3['normalized_second'] <= 2*data_final_3['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())

group_mean_3 = data_final_3.assign(credit_sum=data_final_3.userId.map(data_final_3.groupby('userId').credit.mean()))
#print (group_mean)

total_score_3 = group_mean_3.assign(adj_rating=(group_mean_3['rating'] + group_mean_3['rating']*group_mean_3['credit_sum'])/2)
grouped_sum_3 = total_score_3.groupby('movieId').adj_rating.mean()
#print (grouped_sum_2)

print (max(grouped_sum_3))
print (min(grouped_sum_3))
grouped_sum_3.to_csv('grouped_sum_3.csv')


# 第四筆

# In[70]:

import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data_4 = pd.read_csv("ratings_adjust_full_res_4.csv")
data_4.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min_4 = data_4.assign(normalized=data_4.rating.subtract(data_4.userId.map(data_4.groupby('userId').rating.mean())))
data_nor_4 = data_min_4.assign(normalized=data_min_4.normalized.div(data_min_4.userId.map(data_min_4.groupby('userId').normalized.std())))
data_nor_4 = data_nor.fillna(0)

#將正規化的分數做非線性調整
data_change_4 = ((data_nor_4['normalized']-min(data_nor_4['normalized'])) / (max(data_nor_4['normalized']) - min(data_nor_4['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor_4['data_change'] = data_change_4
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor_4['data_change']))
print (min(data_nor_4['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp_4 = data_nor_4.assign(normalized_std=data_nor_4.movieId.map(data_nor_4.groupby('movieId').data_change.std()))
result_4 = temp_4.assign(normalized_mean=temp_4.movieId.map(temp_4.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new_4 = result_4.assign(normalized_second=data_nor_4.data_change.subtract(result_4.movieId.map(result_4.groupby('movieId').data_change.mean())))
data_nor_new_4 = data_min_new_4.assign(normalized_second=data_min_new_4.normalized_second.div(data_min_new_4.movieId.map(data_min_new_4.groupby('movieId').normalized_second.std())))
data_final_4 = data_nor_new_4.assign(normalized_second=abs(data_nor_new_4['normalized_second']))


# In[71]:

data_final_4['credit'] = np.where(data_final_4['normalized_second'] <= 2*data_final_4['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())

group_mean_4 = data_final_4.assign(credit_sum=data_final_4.userId.map(data_final_4.groupby('userId').credit.mean()))
#print (group_mean)

total_score_4 = group_mean_4.assign(adj_rating=(group_mean_4['rating'] + group_mean_4['rating']*group_mean_4['credit_sum'])/2)
grouped_sum_4 = total_score_4.groupby('movieId').adj_rating.mean()
#print (grouped_sum_2)

print (max(grouped_sum_4))
print (min(grouped_sum_4))
grouped_sum_4.to_csv('grouped_sum_4.csv')


# In[36]:

import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data_5 = pd.read_csv("ratings_adjust_full_res_5.csv")
data_5.convert_objects(convert_numeric=True).dtypes
data_nor = data_nor.fillna(0)

#對userId做正規化
data_min_5 = data_5.assign(normalized=data_5.rating.subtract(data_5.userId.map(data_5.groupby('userId').rating.mean())))
data_nor_5 = data_min_5.assign(normalized=data_min_5.normalized.div(data_min_5.userId.map(data_min_5.groupby('userId').normalized.std())))
data_nor = data_nor.fillna(0)

#將正規化的分數做非線性調整
data_change_5 = ((data_nor_5['normalized']-min(data_nor_5['normalized'])) / (max(data_nor_5['normalized']) - min(data_nor_5['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor_5['data_change'] = data_change_5
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor_5['data_change']))
print (min(data_nor_5['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp_5 = data_nor_5.assign(normalized_std=data_nor_5.movieId.map(data_nor_5.groupby('movieId').data_change.std()))
result_5 = temp_5.assign(normalized_mean=temp_5.movieId.map(temp_5.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new_5 = result_5.assign(normalized_second=data_nor_5.data_change.subtract(result_5.movieId.map(result_5.groupby('movieId').data_change.mean())))
data_nor_new_5 = data_min_new_5.assign(normalized_second=data_min_new_5.normalized_second.div(data_min_new_5.movieId.map(data_min_new_5.groupby('movieId').normalized_second.std())))
data_final_5 = data_nor_new_5.assign(normalized_second=abs(data_nor_new_5['normalized_second']))


# In[37]:

data_final_5['credit'] = np.where(data_final_5['normalized_second'] <= 2*data_final_5['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())

group_mean_5 = data_final_5.assign(credit_sum=data_final_5.userId.map(data_final_5.groupby('userId').credit.mean()))
#print (group_mean)

total_score_5 = group_mean_5.assign(adj_rating=(group_mean_5['rating'] + group_mean_5['rating']*group_mean_5['credit_sum'])/2)
grouped_sum_5 = total_score_5.groupby('movieId').adj_rating.mean()
#print (grouped_sum_2)

print (max(grouped_sum_5))
print (min(grouped_sum_5))
grouped_sum_5.to_csv('grouped_sum_5.csv')


# In[38]:

import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data_6 = pd.read_csv("ratings_adjust_full_res_6.csv")
data_6.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min_6 = data_6.assign(normalized=data_6.rating.subtract(data_6.userId.map(data_6.groupby('userId').rating.mean())))
data_nor_6 = data_min_6.assign(normalized=data_min_6.normalized.div(data_min_6.userId.map(data_min_6.groupby('userId').normalized.std())))

#將正規化的分數做非線性調整
data_change_6 = ((data_nor_6['normalized']-min(data_nor_6['normalized'])) / (max(data_nor_6['normalized']) - min(data_nor_6['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor_6['data_change'] = data_change_6
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor_6['data_change']))
print (min(data_nor_6['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp_6 = data_nor_6.assign(normalized_std=data_nor_6.movieId.map(data_nor_6.groupby('movieId').data_change.std()))
result_6 = temp_6.assign(normalized_mean=temp_6.movieId.map(temp_6.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new_6 = result_6.assign(normalized_second=data_nor_6.data_change.subtract(result_6.movieId.map(result_6.groupby('movieId').data_change.mean())))
data_nor_new_6 = data_min_new_6.assign(normalized_second=data_min_new_6.normalized_second.div(data_min_new_6.movieId.map(data_min_new_6.groupby('movieId').normalized_second.std())))
data_final_6 = data_nor_new_6.assign(normalized_second=abs(data_nor_new_6['normalized_second']))


# In[39]:

data_final_6['credit'] = np.where(data_final_6['normalized_second'] <= 2*data_final_6['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())

group_mean_6 = data_final_6.assign(credit_sum=data_final_6.userId.map(data_final_6.groupby('userId').credit.mean()))
#print (group_mean)

total_score_6 = group_mean_6.assign(adj_rating=(group_mean_6['rating'] + group_mean_6['rating']*group_mean_6['credit_sum'])/2)
grouped_sum_6 = total_score_6.groupby('movieId').adj_rating.mean()
#print (grouped_sum_2)

print (max(grouped_sum_6))
print (min(grouped_sum_6))
grouped_sum_6.to_csv('grouped_sum_6.csv')


# In[40]:

import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data_7 = pd.read_csv("ratings_adjust_full_res_7.csv")
data_7.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min_7 = data_7.assign(normalized=data_7.rating.subtract(data_7.userId.map(data_7.groupby('userId').rating.mean())))
data_nor_7 = data_min_7.assign(normalized=data_min_7.normalized.div(data_min_7.userId.map(data_min_7.groupby('userId').normalized.std())))

#將正規化的分數做非線性調整
data_change_7 = ((data_nor_7['normalized']-min(data_nor_7['normalized'])) / (max(data_nor_7['normalized']) - min(data_nor_7['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor_7['data_change'] = data_change_7
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor_7['data_change']))
print (min(data_nor_7['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp_7 = data_nor_7.assign(normalized_std=data_nor_7.movieId.map(data_nor_7.groupby('movieId').data_change.std()))
result_7 = temp_7.assign(normalized_mean=temp_7.movieId.map(temp_7.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new_7 = result_7.assign(normalized_second=data_nor_7.data_change.subtract(result_7.movieId.map(result_7.groupby('movieId').data_change.mean())))
data_nor_new_7 = data_min_new_7.assign(normalized_second=data_min_new_7.normalized_second.div(data_min_new_7.movieId.map(data_min_new_7.groupby('movieId').normalized_second.std())))
data_final_7 = data_nor_new_7.assign(normalized_second=abs(data_nor_new_7['normalized_second']))


# In[41]:

data_final_7['credit'] = np.where(data_final_7['normalized_second'] <= 2*data_final_7['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())

group_mean_7 = data_final_7.assign(credit_sum=data_final_7.userId.map(data_final_7.groupby('userId').credit.mean()))
#print (group_mean)

total_score_7 = group_mean_7.assign(adj_rating=(group_mean_7['rating'] + group_mean_7['rating']*group_mean_7['credit_sum'])/2)
grouped_sum_7 = total_score_7.groupby('movieId').adj_rating.mean()
#print (grouped_sum_2)

print (max(grouped_sum_7))
print (min(grouped_sum_7))
grouped_sum_7.to_csv('grouped_sum_7.csv')


# In[42]:

import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data_8 = pd.read_csv("ratings_adjust_full_res_8.csv")
data_8.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min_8 = data_8.assign(normalized=data_8.rating.subtract(data_8.userId.map(data_8.groupby('userId').rating.mean())))
data_nor_8 = data_min_8.assign(normalized=data_min_8.normalized.div(data_min_8.userId.map(data_min_8.groupby('userId').normalized.std())))

#將正規化的分數做非線性調整
data_change_8 = ((data_nor_8['normalized']-min(data_nor_8['normalized'])) / (max(data_nor_8['normalized']) - min(data_nor_8['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor_8['data_change'] = data_change_8
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor_8['data_change']))
print (min(data_nor_8['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp_8 = data_nor_8.assign(normalized_std=data_nor_8.movieId.map(data_nor_8.groupby('movieId').data_change.std()))
result_8 = temp_8.assign(normalized_mean=temp_8.movieId.map(temp_8.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new_8 = result_8.assign(normalized_second=data_nor_8.data_change.subtract(result_8.movieId.map(result_8.groupby('movieId').data_change.mean())))
data_nor_new_8 = data_min_new_8.assign(normalized_second=data_min_new_8.normalized_second.div(data_min_new_8.movieId.map(data_min_new_8.groupby('movieId').normalized_second.std())))
data_final_8 = data_nor_new_8.assign(normalized_second=abs(data_nor_new_8['normalized_second']))


# In[43]:

data_final_8['credit'] = np.where(data_final_8['normalized_second'] <= 2*data_final_8['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())

group_mean_8 = data_final_8.assign(credit_sum=data_final_8.userId.map(data_final_8.groupby('userId').credit.mean()))
#print (group_mean)

total_score_8 = group_mean_8.assign(adj_rating=(group_mean_8['rating'] + group_mean_8['rating']*group_mean_8['credit_sum'])/2)
grouped_sum_8 = total_score_8.groupby('movieId').adj_rating.mean()
#print (grouped_sum_2)

print (max(grouped_sum_8))
print (min(grouped_sum_8))
grouped_sum_8.to_csv('grouped_sum_8.csv')


# In[44]:

import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data_9 = pd.read_csv("ratings_adjust_full_res_9.csv")
data_9.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min_9 = data_9.assign(normalized=data_9.rating.subtract(data_9.userId.map(data_9.groupby('userId').rating.mean())))
data_nor_9 = data_min_9.assign(normalized=data_min_9.normalized.div(data_min_9.userId.map(data_min_9.groupby('userId').normalized.std())))

#將正規化的分數做非線性調整
data_change_9 = ((data_nor_9['normalized']-min(data_nor_9['normalized'])) / (max(data_nor_9['normalized']) - min(data_nor_9['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor_9['data_change'] = data_change_9
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor_9['data_change']))
print (min(data_nor_9['data_change']))


#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp_9 = data_nor_9.assign(normalized_std=data_nor_9.movieId.map(data_nor_9.groupby('movieId').data_change.std()))
result_9 = temp_9.assign(normalized_mean=temp_9.movieId.map(temp_9.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new_9 = result_9.assign(normalized_second=data_nor_9.data_change.subtract(result_9.movieId.map(result_9.groupby('movieId').data_change.mean())))
data_nor_new_9 = data_min_new_9.assign(normalized_second=data_min_new_9.normalized_second.div(data_min_new_9.movieId.map(data_min_new_9.groupby('movieId').normalized_second.std())))
data_final_9 = data_nor_new_9.assign(normalized_second=abs(data_nor_new_9['normalized_second']))


# In[45]:

data_final_9['credit'] = np.where(data_final_9['normalized_second'] <= 2*data_final_9['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())

group_mean_9 = data_final_9.assign(credit_sum=data_final_9.userId.map(data_final_9.groupby('userId').credit.mean()))
#print (group_mean)

total_score_9 = group_mean_9.assign(adj_rating=(group_mean_9['rating'] + group_mean_9['rating']*group_mean_9['credit_sum'])/2)
grouped_sum_9 = total_score_9.groupby('movieId').adj_rating.mean()
#print (grouped_sum_2)

print (max(grouped_sum_9))
print (min(grouped_sum_9))
grouped_sum_9.to_csv('grouped_sum_9.csv')


# ## 算出小樣本中每一部電影的平均分數（未調整分數）

# In[2]:

import pandas as pd
import numpy as np
import math

#20%全
data_adj_1 = pd.read_csv("ratings_adjust_full_res_1.csv")
data_adj_1.convert_objects(convert_numeric=True).dtypes
data_adj_1 = data_adj_1.groupby('movieId').rating.mean()
data_adj_1 = pd.DataFrame(data_adj_1) 
data_adj_1['movieId'] = data_adj_1.index
#print (data_adj_1)

data_adj_2 = pd.read_csv("ratings_adjust_full_res_2.csv")
data_adj_2.convert_objects(convert_numeric=True).dtypes
data_adj_2 = data_adj_2.groupby('movieId').rating.mean()
data_adj_2 = pd.DataFrame(data_adj_2) 
data_adj_2['movieId'] = data_adj_2.index

data_adj_3 = pd.read_csv("ratings_adjust_full_res_3.csv")
data_adj_3.convert_objects(convert_numeric=True).dtypes
data_adj_3 = data_adj_3.groupby('movieId').rating.mean()
data_adj_3 = pd.DataFrame(data_adj_3) 
data_adj_3['movieId'] = data_adj_3.index

data_adj_4 = pd.read_csv("ratings_adjust_full_res_4.csv")
data_adj_4.convert_objects(convert_numeric=True).dtypes
data_adj_4 = data_adj_4.groupby('movieId').rating.mean()
data_adj_4 = pd.DataFrame(data_adj_4) 
data_adj_4['movieId'] = data_adj_4.index

data_adj_5 = pd.read_csv("ratings_adjust_full_res_5.csv")
data_adj_5.convert_objects(convert_numeric=True).dtypes
data_adj_5 = data_adj_5.groupby('movieId').rating.mean()
data_adj_5 = pd.DataFrame(data_adj_5) 
data_adj_5['movieId'] = data_adj_5.index

data_adj_6 = pd.read_csv("ratings_adjust_full_res_6.csv")
data_adj_6.convert_objects(convert_numeric=True).dtypes
data_adj_6 = data_adj_6.groupby('movieId').rating.mean()
data_adj_6 = pd.DataFrame(data_adj_6) 
data_adj_6['movieId'] = data_adj_6.index

data_adj_7 = pd.read_csv("ratings_adjust_full_res_7.csv")
data_adj_7.convert_objects(convert_numeric=True).dtypes
data_adj_7 = data_adj_7.groupby('movieId').rating.mean()
data_adj_7 = pd.DataFrame(data_adj_7) 
data_adj_7['movieId'] = data_adj_7.index

data_adj_8 = pd.read_csv("ratings_adjust_full_res_8.csv")
data_adj_8.convert_objects(convert_numeric=True).dtypes
data_adj_8 = data_adj_8.groupby('movieId').rating.mean()
data_adj_8 = pd.DataFrame(data_adj_8) 
data_adj_8['movieId'] = data_adj_8.index

data_adj_9 = pd.read_csv("ratings_adjust_full_res_9.csv")
data_adj_9.convert_objects(convert_numeric=True).dtypes
data_adj_9 = data_adj_9.groupby('movieId').rating.mean()
data_adj_9 = pd.DataFrame(data_adj_9) 
data_adj_9['movieId'] = data_adj_9.index


# ## 將之前算過調整過的資料（因為資料量太大，所以每一次算完都有存在暫存檔中）引入，並將所有調整的分數合併成一張表

# In[47]:

grouped_sum_all = pd.read_csv("grouped_sum_all.csv",header=None)
grouped_sum_all.convert_objects(convert_numeric=True).dtypes
grouped_sum_all.columns = ['movieId','score']
#grouped_sum_all.set_index('movieId', inplace=True)
#print (grouped_sum_all)

grouped_sum = pd.read_csv("grouped_sum.csv",header=None)
grouped_sum.convert_objects(convert_numeric=True).dtypes
grouped_sum.columns = ['movieId','score']
#grouped_sum.set_index('movieId', inplace=True)
#print (grouped_sum)

grouped_sum_2 = pd.read_csv("grouped_sum_2.csv",header=None)
grouped_sum_2.convert_objects(convert_numeric=True).dtypes
grouped_sum_2.columns = ['movieId','score']

grouped_sum_3 = pd.read_csv("grouped_sum_3.csv",header=None)
grouped_sum_3.convert_objects(convert_numeric=True).dtypes
grouped_sum_3.columns = ['movieId','score']

grouped_sum_4 = pd.read_csv("grouped_sum_4.csv",header=None)
grouped_sum_4.convert_objects(convert_numeric=True).dtypes
grouped_sum_4.columns = ['movieId','score']

grouped_sum_5 = pd.read_csv("grouped_sum_5.csv",header=None)
grouped_sum_5.convert_objects(convert_numeric=True).dtypes
grouped_sum_5.columns = ['movieId','score']

grouped_sum_6 = pd.read_csv("grouped_sum_6.csv",header=None)
grouped_sum_6.convert_objects(convert_numeric=True).dtypes
grouped_sum_6.columns = ['movieId','score']

grouped_sum_7 = pd.read_csv("grouped_sum_7.csv",header=None)
grouped_sum_7.convert_objects(convert_numeric=True).dtypes
grouped_sum_7.columns = ['movieId','score']

grouped_sum_8 = pd.read_csv("grouped_sum_8.csv",header=None)
grouped_sum_8.convert_objects(convert_numeric=True).dtypes
grouped_sum_8.columns = ['movieId','score']

grouped_sum_9 = pd.read_csv("grouped_sum_9.csv",header=None)
grouped_sum_9.convert_objects(convert_numeric=True).dtypes
grouped_sum_9.columns = ['movieId','score']

combine = grouped_sum_all.merge(grouped_sum, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(data_adj_1, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(grouped_sum_2, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(data_adj_2, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(grouped_sum_3, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(data_adj_3, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(grouped_sum_4, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(data_adj_4, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(grouped_sum_5, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(data_adj_5, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(grouped_sum_6, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(data_adj_6, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(grouped_sum_7, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(data_adj_7, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(grouped_sum_8, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(data_adj_8, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(grouped_sum_9, left_on='movieId', right_on='movieId', how='outer')
combine = combine.merge(data_adj_9, left_on='movieId', right_on='movieId', how='outer')
combine.columns = ['movieId','all', '10_adjust', '10_average','20_adjust', '20_average','30_adjust', '30_average','40_adjust', '40_average','50_adjust', '50_average','60_adjust', '60_average','70_adjust', '70_average','80_adjust', '80_average','90_adjust', '90_average']
#print (combine)


# In[48]:

#combine = combine.set_index('movieId')
print (combine)


# ## 算出最後的Error總值及差距小比例

# In[50]:

'''
combine = pd.concat([grouped_sum_all, grouped_sum, data_adj_1, grouped_sum_2, data_adj_2, grouped_sum_3, data_adj_3, grouped_sum_4, data_adj_4, grouped_sum_5, data_adj_5, grouped_sum_6, data_adj_6, grouped_sum_7, data_adj_7, grouped_sum_8, data_adj_8, grouped_sum_9, data_adj_9], axis=1)
#combine.rename(columns={'aa': 'adj_rating', '0': 'std_rating', 'rating': 'all_rating'}, inplace=True)
combine.columns = ['all', '10_adjust', '10_average', '20_adjust', '20_average', '30_adjust', '30_average', '40_adjust', '40_average', '50_adjust', '50_average', '60_adjust', '60_average', '70_adjust', '70_average', '80_adjust', '80_average', '90_adjust', '90_average']
#print (combine)
'''


total_combine = combine.assign(all_adj_10_adjust=abs(combine['all'] - combine['10_adjust']))
total_combine = total_combine.assign(all_adjust_10_average=abs(combine['all'] - combine['10_average']))
all_adj_10_adjust = total_combine['all_adj_10_adjust'].sum()
all_adjust_10_average = total_combine['all_adjust_10_average'].sum()
error = [all_adj_10_adjust, all_adjust_10_average]

total_combine = total_combine.assign(all_adj_20_adjust=abs(combine['all'] - combine['20_adjust']))
total_combine = total_combine.assign(all_adjust_20_average=abs(combine['all'] - combine['20_average']))
all_adj_20_adjust = total_combine['all_adj_20_adjust'].sum()
all_adjust_20_average = total_combine['all_adjust_20_average'].sum()
error.append(all_adj_20_adjust)
error.append(all_adjust_20_average)
#print (total_combine)

total_combine = total_combine.assign(all_adj_30_adjust=abs(combine['all'] - combine['30_adjust']))
total_combine = total_combine.assign(all_adjust_30_average=abs(combine['all'] - combine['30_average']))
all_adj_30_adjust = total_combine['all_adj_30_adjust'].sum()
all_adjust_30_average = total_combine['all_adjust_30_average'].sum()
error.append(all_adj_30_adjust)
error.append(all_adjust_30_average)

total_combine = total_combine.assign(all_adj_40_adjust=abs(combine['all'] - combine['40_adjust']))
total_combine = total_combine.assign(all_adjust_40_average=abs(combine['all'] - combine['40_average']))
all_adj_40_adjust = total_combine['all_adj_40_adjust'].sum()
all_adjust_40_average = total_combine['all_adjust_40_average'].sum()
error.append(all_adj_40_adjust)
error.append(all_adjust_40_average)

total_combine = total_combine.assign(all_adj_50_adjust=abs(combine['all'] - combine['50_adjust']))
total_combine = total_combine.assign(all_adjust_50_average=abs(combine['all'] - combine['50_average']))
all_adj_50_adjust = total_combine['all_adj_50_adjust'].sum()
all_adjust_50_average = total_combine['all_adjust_50_average'].sum()
error.append(all_adj_50_adjust)
error.append(all_adjust_50_average)

total_combine = total_combine.assign(all_adj_60_adjust=abs(combine['all'] - combine['60_adjust']))
total_combine = total_combine.assign(all_adjust_60_average=abs(combine['all'] - combine['60_average']))
all_adj_60_adjust = total_combine['all_adj_60_adjust'].sum()
all_adjust_60_average = total_combine['all_adjust_60_average'].sum()
error.append(all_adj_60_adjust)
error.append(all_adjust_60_average)

total_combine = total_combine.assign(all_adj_70_adjust=abs(combine['all'] - combine['70_adjust']))
total_combine = total_combine.assign(all_adjust_70_average=abs(combine['all'] - combine['70_average']))
all_adj_70_adjust = total_combine['all_adj_70_adjust'].sum()
all_adjust_70_average = total_combine['all_adjust_70_average'].sum()
error.append(all_adj_70_adjust)
error.append(all_adjust_70_average)

total_combine = total_combine.assign(all_adj_80_adjust=abs(combine['all'] - combine['80_adjust']))
total_combine = total_combine.assign(all_adjust_80_average=abs(combine['all'] - combine['80_average']))
all_adj_80_adjust = total_combine['all_adj_80_adjust'].sum()
all_adjust_80_average = total_combine['all_adjust_80_average'].sum()
error.append(all_adj_80_adjust)
error.append(all_adjust_80_average)

total_combine = total_combine.assign(all_adj_90_adjust=abs(combine['all'] - combine['90_adjust']))
total_combine = total_combine.assign(all_adjust_90_average=abs(combine['all'] - combine['90_average']))
all_adj_90_adjust = total_combine['all_adj_90_adjust'].sum()
all_adjust_90_average = total_combine['all_adjust_90_average'].sum()
error.append(all_adj_90_adjust)
error.append(all_adjust_90_average)


#print (error)
error = pd.DataFrame(error)
error = error.T
error.columns = ['10_adjust','10_average','20_adjust','20_average','30_adjust','30_average','40_adjust','40_average','50_adjust','50_average','60_adjust','60_average','70_adjust','70_average','80_adjust','80_average','90_adjust','90_average']
print (error)


total_combine['credit_10'] = np.where(total_combine['all_adj_10_adjust'] <= total_combine['all_adjust_10_average'],1,0)
total_combine.loc[((np.isnan(combine['10_adjust'])==True) | (np.isnan(combine['10_average'])==True)), 'credit_10'] = 'NAN'
credit_10 = total_combine.groupby('credit_10').credit_10.count()
credit_combine = pd.DataFrame(credit_10)

total_combine['credit_20'] = np.where(total_combine['all_adj_20_adjust'] <= total_combine['all_adjust_20_average'],1,0)
total_combine.loc[((np.isnan(combine['20_adjust'])==True) | (np.isnan(combine['20_average'])==True)), 'credit_20'] = 'NAN'
credit_20 = total_combine.groupby('credit_20').credit_20.count()
credit_combine = credit_combine.assign(credit_20 = credit_20)

total_combine['credit_30'] = np.where(total_combine['all_adj_30_adjust'] <= total_combine['all_adjust_30_average'],1,0)
total_combine.loc[((np.isnan(combine['30_adjust'])==True) | (np.isnan(combine['30_average'])==True)), 'credit_30'] = 'NAN'
credit_30 = total_combine.groupby('credit_30').credit_30.count()
credit_combine = credit_combine.assign(credit_30 = credit_30)

total_combine['credit_40'] = np.where(total_combine['all_adj_40_adjust'] <= total_combine['all_adjust_40_average'],1,0)
total_combine.loc[((np.isnan(combine['40_adjust'])==True) | (np.isnan(combine['40_average'])==True)), 'credit_40'] = 'NAN'
credit_40 = total_combine.groupby('credit_40').credit_40.count()
credit_combine = credit_combine.assign(credit_40 = credit_40)

total_combine['credit_50'] = np.where(total_combine['all_adj_50_adjust'] <= total_combine['all_adjust_50_average'],1,0)
total_combine.loc[((np.isnan(combine['50_adjust'])==True) | (np.isnan(combine['50_average'])==True)), 'credit_50'] = 'NAN'
credit_50 = total_combine.groupby('credit_50').credit_50.count()
credit_combine = credit_combine.assign(credit_50 = credit_50)

total_combine['credit_60'] = np.where(total_combine['all_adj_60_adjust'] <= total_combine['all_adjust_60_average'],1,0)
total_combine.loc[((np.isnan(combine['60_adjust'])==True) | (np.isnan(combine['60_average'])==True)), 'credit_60'] = 'NAN'
credit_60 = total_combine.groupby('credit_60').credit_60.count()
credit_combine = credit_combine.assign(credit_60 = credit_60)

total_combine['credit_70'] = np.where(total_combine['all_adj_70_adjust'] <= total_combine['all_adjust_70_average'],1,0)
total_combine.loc[((np.isnan(combine['70_adjust'])==True) | (np.isnan(combine['70_average'])==True)), 'credit_70'] = 'NAN'
credit_70 = total_combine.groupby('credit_70').credit_70.count()
credit_combine = credit_combine.assign(credit_70 = credit_70)

total_combine['credit_80'] = np.where(total_combine['all_adj_80_adjust'] <= total_combine['all_adjust_80_average'],1,0)
total_combine.loc[((np.isnan(combine['80_adjust'])==True) | (np.isnan(combine['80_average'])==True)), 'credit_80'] = 'NAN'
credit_80 = total_combine.groupby('credit_80').credit_80.count()
credit_combine = credit_combine.assign(credit_80 = credit_80)

total_combine['credit_90'] = np.where(total_combine['all_adj_90_adjust'] <= total_combine['all_adjust_90_average'],1,0)
total_combine.loc[((np.isnan(combine['90_adjust'])==True) | (np.isnan(combine['90_average'])==True)), 'credit_90'] = 'NAN'
credit_90 = total_combine.groupby('credit_90').credit_90.count()
credit_combine = credit_combine.assign(credit_90 = credit_90)
print (credit_combine)

credit_combine = credit_combine.T
credit_rate = (credit_combine[1]/(74258 - credit_combine['NAN']))
print (credit_rate)
#39443
#total_combine.to_csv("total_combine_1.csv")

#result = pd.concat([error,credit_rate])
#print (result)
#credit_rate.to_csv("credit_rate.csv")



# In[ ]:




# In[ ]:



