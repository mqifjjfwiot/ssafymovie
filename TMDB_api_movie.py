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
