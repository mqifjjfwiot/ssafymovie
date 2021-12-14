import json
import pandas as pd
import numpy as np
from datetime import date

# 필요
# API 신청용 URL 조합용 클래스
class URLMaker:
  #api 기본 주소세팅. 뒤에 쿼리 덧붙여서 명령별 구별 
  url = 'https://api.themoviedb.org/3'

  def __init__(self, key):
    self.key = key

  # 영화/추천영화 한 페이지 긁어오기(ML용)
  # GET movie/popular (https://developers.themoviedb.org/3/movies/get-popular-movies)
  def get_movie_url(self, category='movie', feature='popular', page='1'):
    #위의 url(자기자신 소속 url 데이터 line 6)/movie/popular 로 기능 구동
    url = f'{self.url}/{category}/{feature}'
    #뒤에 쿼리로 인증용 필수 데이터 api_key(line 8), 옵션 데이터인 언어(한글-한국), 페이지수(1페이지) 덧붙임
    url += f'?api_key={self.key}&language=en-US&page={str(page)}'

    #그렇게 만든 최종 명령 url 반환
    return url

  # 영화/추천영화 한 페이지 긁어오기(한글판) 차후 overview, title은 영어가 아닌 한글로 출력하기 위함
  def get_movie_url_kr(self, category='movie', feature='popular', page='1'):
    #위의 url(자기자신 소속 url 데이터 line 6)/movie/popular 로 기능 구동
    url = f'{self.url}/{category}/{feature}'
    #뒤에 쿼리로 인증용 필수 데이터 api_key(line 8), 옵션 데이터인 언어(한글-한국), 페이지수(1페이지) 덧붙임
    url += f'?api_key={self.key}&language=ko-KR&page={str(page)}'

    #그렇게 만든 최종 명령 url 반환
    return url
  
  # 장르 정보 긁어오기 (https://developers.themoviedb.org/3/genres/get-movie-list)
  def get_genre_url(self):
    url = f'{self.url}/genre/movie/list?api_key={self.key}'
    return url

# 인증키(외부 API 시동용)
TMDB_KEY = '07893hhsf423498asdas2446f034b'
# 일부 변형하여 업로드함

# url 조합해주는 클래스 선언
url = URLMaker(TMDB_KEY)
# 1~1000 페이지의 범위를 설정하여 영화를 가져올 수 있음 (상수화하여 kr과 en버전이 상이해지는 경우를 방지)
# 당연히 불러오는 페이지의 수가 늘어날수록 API기동 딜레이가 길어짐. 이번 프로젝트는 200으로 고정.
PAGES = 200

def create_genre_data():
  # line 37에서 반환한 url값 받아와 저장
  genre_url = url.get_genre_url()
  # 리퀘스트 데이터 저장
  raw_data = requests.get(genre_url)
  # 해당 데이터 json화
  json_data = raw_data.json()
  # 시킨것에서 genres라는 키의 밸류값 추출
  genres = json_data.get('genres')

  # 장르 데이터 저장용 빈 리스트 생성. 여기에 딕셔너리 하나씩 넣을 예정
  genre_data = []

  # genres의 모든 원소들을 하나하나 tmp에 저장한뒤 genre_data에 하나하나 추가함
  for genre in genres:
    tmp = {

