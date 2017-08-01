
# coding: utf-8

# In[1]:

#df.assign(normalized=df.bought.div(df.user.map(df.groupby('user').bought.sum())))
import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data = pd.read_csv("ratings.csv")
data.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min = data.assign(normalized=data.rating.subtract(data.userId.map(data.groupby('userId').rating.mean())))
data_nor = data_min.assign(normalized=data_min.normalized.div(data_min.userId.map(data_min.groupby('userId').normalized.std())))

#將正規化的分數做非線性調整
data_change = ((data_nor['normalized']-min(data_nor['normalized'])) / (max(data_nor['normalized']) - min(data_nor['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor['data_change'] = data_change
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor['data_change']))
print (min(data_nor['data_change']))


#用movieId再做一次正規化
#data_min_new = data_nor.assign(normalized_second=data_nor.data_change.subtract(data_nor.movieId.map(data_nor.groupby('movieId').data_change.mean())))
#data_nor_new = data_min_new.assign(normalized_second=data_min_new.normalized_second.div(data_min_new.movieId.map(data_min_new.groupby('movieId').normalized_second.std())))

#這部分是要算調整分數的標準差和平均數，但公式有錯要記得修改
#temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
#result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))
temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new = result.assign(normalized_second=data_nor.data_change.subtract(result.movieId.map(result.groupby('movieId').data_change.mean())))
data_nor_new = data_min_new.assign(normalized_second=data_min_new.normalized_second.div(data_min_new.movieId.map(data_min_new.groupby('movieId').normalized_second.std())))
data_final = data_nor_new.assign(normalized_second=abs(data_nor_new['normalized_second']))
print (data_final)


# In[2]:

#total_len = int(len(data_final.index))
data_final['credit'] = np.where(data_final['normalized_second'] <= 2*data_final['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())

group_mean = data_final.assign(credit_sum=data_final.userId.map(data_final.groupby('userId').credit.mean()))
#print (group_mean)

total_score = group_mean.assign(adj_rating=(group_mean['rating'] + group_mean['rating']*group_mean['credit_sum'])/2)
grouped_sum = total_score.groupby('movieId').adj_rating.mean()
print (grouped_sum)
 
#print (max(grouped_sum))
#print (min(grouped_sum))


# In[11]:

'''
adj_mean = total_score.adj_rating.mean()
adj_std = total_score.adj_rating.std()

adj_pos = total_score.assign(adj_pos = adj_mean + adj_std)
adj_all = adj_pos.assign(adj_neg = adj_mean - adj_std)
#print (adj_all)
adj_all['point'] = np.where((adj_all['adj_neg'] <= adj_all['adj_rating']) & (adj_all['adj_rating'] <= adj_all['adj_pos']),1,0)
point_sum = adj_all.groupby('userId').point.sum()
point_count = adj_all.groupby('userId').point.count()
point = pd.DataFrame(point_sum)
point['point_count'] = point_count
point['point_avg'] = point['point'] / point['point_count']
#print (point)
get_index = point[(point['point_avg'] > 0.8) & (point['point_count'] > 50)]
get_index_value = get_index.index.values
print (get_index_value)
'''
'''
total_mean = total_score.rating.mean()
total_std = total_score.rating.std()
total_pos = total_score.assign(total_pos = total_mean + total_std)
total_all = total_pos.assign(total_neg = total_mean - total_std)
#print (total_all)
total_all['point'] = np.where((total_all['total_neg'] <= total_all['adj_rating']) & (total_all['adj_rating'] <= total_all['total_pos']),1,0)
#print (total_all)
point_sum = total_all.groupby('userId').point.sum()
point_count = total_all.groupby('userId').point.count()
point = pd.DataFrame(point_sum)
point['point_count'] = point_count
point['point_avg'] = point['point'] / point['point_count']
point.to_csv('point.csv')
get_index = point[(point['point_avg'] > 0.8) & (point['point_count'] > 50)]
get_index_value = get_index.index.values
print (get_index_value)
'''

'''
adj_pos = total_score.assign(adj_pos = adj_mean + adj_std)
adj_all = adj_pos.assign(adj_neg = adj_mean - adj_std)
#print (adj_all)
adj_all['point'] = np.where((adj_all['adj_neg'] <= adj_all['adj_rating']) & (adj_all['adj_rating'] <= adj_all['adj_pos']),1,0)
point_sum = adj_all.groupby('userId').point.sum()
point_count = adj_all.groupby('userId').point.count()
point = pd.DataFrame(point_sum)
point['point_count'] = point_count
point['point_avg'] = point['point'] / point['point_count']
#print (point)
get_index = point[(point['point_avg'] > 0.8) & (point['point_count'] > 50)]
get_index_value = get_index.index.values
print (get_index_value)
'''
'''
people_mean = total_score.groupby('userId').adj_rating.mean()
people_mean = pd.DataFrame(people_mean)

total_mean = total_score.rating.mean()
total_std = total_score.rating.std()
people_mean['point'] = np.where((total_mean-total_std <= people_mean['adj_rating']) & (people_mean['adj_rating'] <= total_mean+total_std),1,0)
#aa = people_mean.sort(['point'])
#print (people_mean)
get_index = people_mean[(people_mean['point'] == 1) ]
get_index_value = get_index.index.values
print (get_index_value)
'''
'''
adj_mean = total_score.adj_rating.mean()
adj_std = total_score.adj_rating.std()

people_mean = total_score.groupby('userId').rating.mean()
people_mean = pd.DataFrame(people_mean)
people_mean['point'] = np.where((adj_mean-adj_std <= people_mean['rating']) & (people_mean['rating'] <= adj_mean+adj_std),1,0)
print (people_mean.sum())
'''
adj_df = grouped_sum.add_suffix('').reset_index()
#print (adj_df)


adj_df_std = adj_df['adj_rating'].std()
adj_df_mean = adj_df['adj_rating'].mean()
adj_df_pos = adj_df_mean + adj_df_std
adj_df_neg = adj_df_mean - adj_df_std


original_data_rating_mean = data.groupby('userId').rating.mean()
#print (original_data_rating_mean)
original_data_rating_mean_df = pd.DataFrame(original_data_rating_mean)
#print (original_data_rating_mean_df)


original_data_rating_mean_df['point'] = np.where((adj_df_neg <= original_data_rating_mean_df['rating']) & (original_data_rating_mean_df['rating'] <= adj_df_pos),1,0)

#print (original_data_rating_mean_df)

get_index = original_data_rating_mean_df[(original_data_rating_mean_df['point'] == 1)]
#print (get_index)

get_index_value = get_index.index.values
print (get_index_value)


# In[12]:

rating_change_new_16 = data[~data['userId'].isin(get_index_value)]
#print (rating_change_new_14)
rating_change_new_16.to_csv('ratings_change_new_16.csv', index=False)

rating_std_new_16 = data[data['userId'].isin(get_index_value)]
#print (rating_change_new_14)
rating_std_new_16.to_csv('ratings_std_new_16.csv', index=False)


# In[100]:

#df.assign(normalized=df.bought.div(df.user.map(df.groupby('user').bought.sum())))
import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data = pd.read_csv("ratings_change_new_16.csv")
data.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min = data.assign(normalized=data.rating.subtract(data.userId.map(data.groupby('userId').rating.mean())))
data_nor = data_min.assign(normalized=data_min.normalized.div(data_min.userId.map(data_min.groupby('userId').normalized.std())))

#將正規化的分數做非線性調整
data_change = ((data_nor['normalized']-min(data_nor['normalized'])) / (max(data_nor['normalized']) - min(data_nor['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor['data_change'] = data_change
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor['data_change']))
print (min(data_nor['data_change']))

temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new = result.assign(normalized_second=data_nor.data_change.subtract(result.movieId.map(result.groupby('movieId').data_change.mean())))
data_nor_new = data_min_new.assign(normalized_second=data_min_new.normalized_second.div(data_min_new.movieId.map(data_min_new.groupby('movieId').normalized_second.std())))
data_final = data_nor_new.assign(normalized_second=abs(data_nor_new['normalized_second']))


# In[101]:

#total_len = int(len(data_final.index))
data_final['credit'] = np.where(data_final['normalized_second'] <= 1*data_final['normalized_std'],1,0)
#print (data_final)
#print (data_final.credit.sum())


group_mean = data_final.assign(credit_sum=data_final.userId.map(data_final.groupby('userId').credit.mean()))
#print (group_mean)

total_score = group_mean.assign(adj_rating=(group_mean['rating'] + group_mean['rating']*group_mean['credit_sum'])/2)
grouped_sum = total_score.groupby('movieId').adj_rating.mean()
#print (grouped_sum)

print (max(grouped_sum))
print (min(grouped_sum))


# In[102]:

#df.assign(normalized=df.bought.div(df.user.map(df.groupby('user').bought.sum())))
import pandas as pd
import numpy as np
import math

#將csv匯入進來轉type
data = pd.read_csv("ratings_std_new_16.csv")
data.convert_objects(convert_numeric=True).dtypes

#對userId做正規化
data_min = data.assign(normalized=data.rating.subtract(data.userId.map(data.groupby('userId').rating.mean())))
data_nor = data_min.assign(normalized=data_min.normalized.div(data_min.userId.map(data_min.groupby('userId').normalized.std())))

#將正規化的分數做非線性調整
data_change = ((data_nor['normalized']-min(data_nor['normalized'])) / (max(data_nor['normalized']) - min(data_nor['normalized'])))*5
#data_change = round(data_nor['normalized'] *1000  + 1000)
#print (data_change)
data_nor['data_change'] = data_change
#rating_two_di = data_nor.assign(rating_change_alert = np.tanh(data_nor['data_change'].values))
print (max(data_nor['data_change']))
print (min(data_nor['data_change']))

temp = data_nor.assign(normalized_std=data_nor.movieId.map(data_nor.groupby('movieId').data_change.std()))
result = temp.assign(normalized_mean=temp.movieId.map(temp.groupby('movieId').data_change.mean()))

#根據movieId來做正規化，並作絕對值
data_min_new = result.assign(normalized_second=data_nor.data_change.subtract(result.movieId.map(result.groupby('movieId').data_change.mean())))
data_nor_new = data_min_new.assign(normalized_second=data_min_new.normalized_second.div(data_min_new.movieId.map(data_min_new.groupby('movieId').normalized_second.std())))
data_final = data_nor_new.assign(normalized_second=abs(data_nor_new['normalized_second']))


# In[105]:

#total_len = int(len(data_final.index))
data_final['credit'] = np.where(data_final['normalized_second'] <= 2*data_final['normalized_std'],1,0)
print (data_final)
#print (data_final.credit.sum())


group_mean = data_final.assign(credit_sum=data_final.userId.map(data_final.groupby('userId').credit.mean()))
#print (group_mean)

total_score = group_mean.assign(adj_rating=(group_mean['rating'] + group_mean['rating']*group_mean['credit_sum'])/2)
std = total_score.groupby('movieId').adj_rating.mean()
#print (grouped_sum)

#print (max(grouped_sum))
#print (min(grouped_sum))


# In[104]:

import pandas as pd
import numpy as np
import math


#將csv匯入進來轉type
#data_std = pd.read_csv("ratings_std_new_16.csv")
#data_std.convert_objects(convert_numeric=True).dtypes

#std = data_std.groupby('movieId').rating.mean()
#std.rename(columns={'rating': 'std_rating'}, inplace=True)
#print (std)


data_all = pd.read_csv("ratings_change_new_16.csv")
data_all.convert_objects(convert_numeric=True).dtypes

data_all = data_all.groupby('movieId').rating.mean()

combine = pd.concat([grouped_sum, std, data_all], axis=1)
#combine.rename(columns={'aa': 'adj_rating', '0': 'std_rating', 'rating': 'all_rating'}, inplace=True)
combine.columns = ['adj_rating', 'std_rating', 'all_rating']
#print (combine)

total_combine = combine.assign(std_adj=abs(combine['std_rating'] - combine['adj_rating']))
total_combine = total_combine.assign(std_all=abs(combine['std_rating'] - combine['all_rating']))
#total_combine.to_csv('1.csv')
std_adj = total_combine['std_adj'].sum()
std_all = total_combine['std_all'].sum()
error = [std_adj, std_all]
error = pd.DataFrame(error)
error = error.T
error.columns = ['std_adj','std_all']
print (error)

total_combine['credit'] = np.where(total_combine['std_adj'] <= total_combine['std_all'],1,0)
total_combine.loc[((np.isnan(total_combine['std_adj'])==True) | (np.isnan(total_combine['std_all'])==True)), 'credit'] = 'NAN'
credit = total_combine.groupby('credit').credit.count()
credit_combine = pd.DataFrame(credit)
#print (credit_combine)

credit_combine = credit_combine.T
print (credit_combine['NAN'].sum())
credit_rate = (credit_combine[1]/(9066 - credit_combine['NAN']))
print (credit_rate)

'''
total_combine['credit'] = np.where(total_combine['std_adj'] <= total_combine['std_all'],1,0)
print (total_combine.credit.sum())
#print (total_combine)
total_combine.to_csv('mm.csv')
#combine.to_csv('compare_v2.csv')
#aa.to_csv('original_score.csv')
'''

