# SSAFYmovie

https://www.themoviedb.org/

TMDB The Movie Api를 활용해 500여개의 영화 데이터를 끌어와 데이터 처리를 해보는 프로젝트입니다.

<h3>참여 인원</h3>
강민구 외 2명. 
  
<h3>프로젝트 참여 기간</h3>
2021-11-18 ~ 11-22

<h3>프로젝트에서 맡은 역할</h3>
  TMDB api로 RAW 영화 데이터의 수집, 분류, 형변환.<br>
  필요한 추가 데이터의 정제, 정리<br>
  영화 추천 알고리즘<br>
  연관 영화 분석 알고리즘<br>
  <h4>추가한 데이터</h4>
  장르정보만을 따로 저장하기 위한 구분키 'movies.genre'<br>
  영화디테일만을 따로 저장하기 위한 구분키 'movies.movie'<br>
  받아온 영화 고유 id를 구분하기 위해 따로 기록한 'pk'<br>
  IMDB 방식으로 인기도와 평점을 가중치 계산한 새로운 지표 'score'<br>
  overview 베이스로 유사도 측정하여 유사한 영화의 고유코드를 저장하는 'movie_reference_overview'<br>
  <br>
<h3>데이터 포맷</h3>
  main : json<br>


![캡처](https://user-images.githubusercontent.com/85283021/142834738-62a37e96-5113-42b5-9bf0-5ce656ea9441.PNG)
