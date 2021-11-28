import json
import pandas as pd
import numpy as np
from datetime import date

# 필요
# API 신청용 URL 조합용 클래스
class URLMaker:
  #api 기본 주소세팅. 뒤에 쿼리 덧붙여서 명령별 구별 
  url = 'https://api.themoviedb.org/3'

