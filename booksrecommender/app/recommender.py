import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds

def recommend_books(predictions_df, user_id, original_title, rating, num_recommendations=20):
    
  # Get and sort the user's predictions
    rating.columns=["user_id","book_id","rating"]
    user_row_number = user_id - 100 # user_id starts at 1, not 0
    sorted_user_predictions = predictions_df.iloc[user_row_number].sort_values(ascending=False)

    # Get the user's data and merge in the movie information.
    user_data =  rating[rating.user_id == (user_id)]
    user_full = (user_data.merge(original_title, how = 'left', left_on = 'book_id', right_on = 'book_id').
                     sort_values(['rating'], ascending=False)
                 )
    
    print ('User {0} has already rated {1} movies.'.format(user_id, user_full.shape[0]))
    print ('Recommending the highest {0} predicted ratings movies not already rated.'.format(num_recommendations))
    
    recommendations = (original_title[~original_title['book_id'].isin(user_full['book_id'])].
         merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
               left_on = 'book_id',
               right_on = 'book_id').
         rename(columns = {user_row_number: 'Predictions'}).
         sort_values('Predictions', ascending = False).
                       iloc[:num_recommendations, :-1]
                      )

    return user_full, recommendations,user_full

def runRecommender(file1,file2,user_id):
    print("yes")
    pd.set_option('display.float_format', lambda x: '%.3f' % x)

    book_list = pd.read_json(file1)

    ratings_list=pd.read_json(file2)

    book_data = pd.merge(ratings_list, book_list, on='book_id')
    book_list['book_id'] = book_list['book_id'].apply(pd.to_numeric)
    book_data = ratings_list.pivot(index = 'user_id', columns ='book_id', values = 'rating').fillna(0)
    R = book_data.to_numpy()
    user_ratings_mean = np.mean(R, axis = 1)
    R_demeaned = R - user_ratings_mean.reshape(-1, 1)
    U, sigma, Vt = svds(R_demeaned, k = 50)
    sigma = np.diag(sigma)

    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    preds_df = pd.DataFrame(all_user_predicted_ratings, columns = book_data.columns)
    already_rated, predictions,rated = recommend_books(preds_df, user_id,  book_list, ratings_list,50)
    predict=predictions.to_json(orient="records")
    rated=rated.to_json(orient="records")
    
    return predict,rated
   