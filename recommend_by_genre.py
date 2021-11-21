import pandas as pd 
import numpy as np
from ast import literal_eval

#tmdb.json 영화 데이터 표본
{
        "model": "movies.movie",
        "pk": 127585,
        "fields": {
            "adult": false,
            "backdrop_path": "/hUPgIibqZlwbhs4N08cPzzc4f5K.jpg",
            "genre_ids": [
                28,
                12,
                14,
                878
            ],
            "original_language": "en",
            "original_title": "X-Men: Days of Future Past",
            "overview": "\ub3cc\uc5f0\ubcc0\uc774\ub4e4\uc744 \uba78\uc885\uc2dc\ud0a4\uae30 \uc704\ud574 \uc81c\uc791\ub41c \ub85c\ubd07 \uc13c\ud2f0\ub12c\uc774 \uc778\uac04\ub4e4\uae4c\uc9c0 \ubaa8\uc870\ub9ac \ub9d0\uc0b4\ud558\ub294 2023\ub144. \uc778\ub958\uc758 \uc885\ub9d0\uc774 \ucf54\uc55e\uc5d0 \ub2e5\uce5c \uc0c1\ud669\uc5d0\uc11c \ud504\ub85c\ud398\uc11cX\uc640 \ub9e4\uadf8\ub2c8\ud1a0\ub294 \uacfc\uac70\ub97c \ud1b5\ud574 \ubbf8\ub798\uc758 \uc6b4\uba85\uc744 \ubc14\uafb8\uace0\uc790 \ud55c\ub2e4. \uc6b8\ubc84\ub9b0\uc740 \ud2b8\ub77c\uc2a4\ud06c\uac00 \uc13c\ud2f0\ub12c\uc744 \uac1c\ubc1c\ud558\ub294 \uac83\uc744 \ub9c9\uae30 \uc704\ud574 1973\ub144\uc73c\ub85c \ubcf4\ub0b4\uc9c4\ub2e4. 1973\ub144\uc758 \ucc30\uc2a4\ub294 \uc808\ub9dd\uc5d0 \ube60\uc9c4 \ucc44 \ud589\ud06c \ub9e5\ucf54\uc774\uc640 \ud568\uaed8 \uc740\ub454 \uc0dd\ud65c\uc744 \ud558\uace0 \uc788\uace0, \uc5d0\ub9ad\uc740 \ucf00\ub124\ub514 \ub300\ud1b5\ub839 \uc554\uc0b4 \uc6a9\uc758\uc790\ub85c \ubd99\uc7a1\ud600 \ud39c\ud0c0\uace4 \uc9c0\ud558 \uae4a\uc219\ud55c \uacf3\uc5d0 \uc704\uce58\ud55c \uc218\uc6a9\uc18c\uc5d0 \uac07\ud600 \uc788\ub2e4.",
            "popularity": 64.747,
            "poster_path": "/zm5zanw86TX2T7qJNTKilL3x3S8.jpg",
            "release_date": "2014-05-15",
            "title": "\uc5d1\uc2a4\ub9e8: \ub370\uc774\uc988 \uc624\ube0c \ud4e8\ucc98 \ud328\uc2a4\ud2b8",
            "vote_average": 7.5,
            "vote_count": 12889,
            "like_users": []
        }
    }

# +
df1=pd.read_csv('tmdb_5000_credits.csv')
df2=pd.read_csv('tmdb_5000_movies.csv')

df1.columns = ['id','tittle','cast','crew']
df2= df2.merge(df1, on='id')

features = ['cast', 'crew', 'keywords', 'genres']

# -

def recommend_by_genre():
    with open('tmdb.json', 'r+') as f:



# +
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)

# 디렉터 이름 줏어오기
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# 리스트 중 최상단 세 개까지 줏어오기
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []

# 키워드 모으기
df2['director'] = df2['crew'].apply(get_director)
features = ['cast', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)

# 스페이스 제거후 소문자를 추가하여, 키워드 헷갈리는 사고 방지
# 이 과정을 거치면 "Johnny Depp"과 "Johnny Galecki" 는 다른 키워드로 인식 됨
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

features = ['cast', 'keywords', 'director', 'genres']

for feature in features:
    df2[feature] = df2[feature].apply(clean_data)

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
df2['soup'] = df2.apply(create_soup, axis=1)

# Import CountVectorizer and create the count matrix
from sklearn.feature_extraction.text import CountVectorizer

# TF-IDF 대신 CountVectorizer()를 사용. 이 방식으로는 자주 반복되는 배우/감독에 가산점 부여 가능
# (상대적으로 더 많은 영화에 출연하거나 감독한 배우/감독의 존재감을 낮추고 싶지 않기 때문입니다. 별로 직관적이지 않습니다.)
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

from sklearn.metrics.pairwise import cosine_similarity

# 코사인 유사성
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# 영화 이름 입력시 인덱스를 식별하는 메커니즘이 필요하므로 영화 제목과 DataFrame 인덱스간의 역매핑
df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])

# 제목을 입력 받아 가장 유사한 10개의 영화목록을 출력하는 함수를 정의
def get_recommendations(title, cosine_sim=cosine_sim2):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    try:
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # 코사인 유사성 순으로 정렬
    except:
        print(title)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    if len(movie_indices) < 10:
        movie_indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
    return df2['title'].iloc[movie_indices]

#print(get_recommendations('The Dark Knight Rises', cosine_sim2))

answers = pd.DataFrame(columns=['title', 
                                'recommended1',
                                'recommended2',
                                'recommended3',
                                'recommended4',
                                'recommended5',
                                'recommended6',
                                'recommended7',
                                'recommended8',
                                'recommended9',
                                'recommended10'])
idx = 0
for d in df2['title']:
    answers_list = [d] + list(get_recommendations(d).values)
    if len(answers_list) == 11:
        answers.loc[idx] = answers_list
        idx += 1
    else:
        print('what?!')
answers.to_csv('recommended_movie_detail2.csv', index=False, encoding='utf-8')
