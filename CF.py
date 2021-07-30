import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine, correlation
from subprocess import check_output
import warnings
warnings.filterwarnings("ignore")
user_cols_name = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('movieles100k/ml-100k/u.user', sep='|', names=user_cols_name,
                    encoding='latin-1', parse_dates=True) 
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings_data = pd.read_csv('movieles100k/ml-100k/u.data', sep='\t', names=r_cols,
                      encoding='latin-1')
m_cols = ['movie_id', 'title', 'release_date', 'video_release_date', 'imdb_url']
movies_data = pd.read_csv('movieles100k/ml-100k/u.item', sep='|', names=m_cols, usecols=range(5),
                     encoding='latin-1')
movie_ratings_data = pd.merge(movies_data, ratings_data)
dataframe = pd.merge(movie_ratings_data, users)
dataframe.head(2)
ratings_data.head(1)
movies_data.head(1)
users.head(1)
dataframe.drop(dataframe.columns[[3,4,7]], axis=1, inplace=True)
ratings_data.drop( "unix_timestamp", inplace = True, axis = 1 ) 
movies_data.drop(movies_data.columns[[3,4]], inplace = True, axis = 1 )
dataframe.info()
movie_stats = dataframe.groupby('title').agg({'rating': [np.size, np.mean]})
movie_stats.head()
min_50 = movie_stats['rating']['size'] >= 50
movie_stats[min_50].sort_values([('rating', 'mean')], ascending=False).head()
ratings_data.rating.plot.hist(bins=50)
plt.title("Distribution of Users' ratings_data")
plt.ylabel('Number of ratings_data')
plt.xlabel('Rating (Out of 5)');
plt.show()
users.age.plot.hist(bins=25)
plt.title("Distribution of Users' Ages")
plt.ylabel('Number of Users')
plt.xlabel('Age');
plt.show()
ratings_data_matrix = ratings_data.pivot_table(index=['movie_id'],columns=['user_id'],values='rating').reset_index(drop=True)
ratings_data_matrix.fillna( 0, inplace = True )
ratings_data_matrix.head()
movie_similarity = 1 - pairwise_distances( ratings_data_matrix.as_matrix(), metric="cosine" )
np.fill_diagonal( movie_similarity, 0 ) #Filling diagonals with 0s for future use when sorting is done
ratings_data_matrix = pd.DataFrame( movie_similarity )
ratings_data_matrix.head(5)
user_inp=input('Enter Title to Recommendation:::')#"Toy Story (1995)"
inp=movies_data[movies_data['title']==user_inp].index.tolist()
inp=inp[0]
    
movies_data['similarity'] = ratings_data_matrix.iloc[inp]
movies_data.columns = ['movie_id', 'title', 'release_date','similarity']
movies_data.head(2)
print("Recommended movies_data based on your choice of ",user_inp ,": \n", movies_data['title'],movies_data.sort_values( ["similarity"], ascending = False )[1:10])
    
