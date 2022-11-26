from flask import Flask, render_template, request
import pickle
#import pandas as pd
import numpy as np

popular = pickle.load(open('topbooks.pkl', 'rb'))
pt = pickle.load(open('pivottable.pkl', 'rb'))
books_re = pickle.load(open('books.pkl', 'rb'))
similar_books_scores = pickle.load(open('similarity.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular['Book-Title'].values),
                           author=list(popular['Book-Author'].values),
                           image=list(popular['Image-URL-M'].values),
                           votes=list(popular['num_ratings'].values),
                           rating=list(popular['avg-rating'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('result.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    
    index = np.where(pt.index==user_input)[0][0]
    '''in this next step we will get the index place in similar_books_index 
    and then will find all those books having close similarity to the book_name 
    provided as input.'''
    similar_items = sorted(list(enumerate(similar_books_scores[index])), 
                           key=lambda x:x[1], reverse=True)[0:6]
    #book_searched = sorted(list(enumerate(similar_books_index[index])), 
                           #key=lambda x:x[1], reverse=True)[0]
    data = []
    
    for i in similar_items:
        item = []
        temp_df = books_re[books_re['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df['Book-Title'].values))
        item.extend(list(temp_df['Book-Author'].values))
        item.extend(list(temp_df['Image-URL-M'].values))
        data.append(item)  
    
    print(data)
    return render_template('result.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
