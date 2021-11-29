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
