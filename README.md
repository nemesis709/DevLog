# Hexa Viewer

- 라이브러리

PyQt5

- 기능

바이너리 파일을 열어서 line(=주소), hex, string 포맷으로 출력한다.

- 특징

파일을 한번에 다 열지 않고 필요한 line만 오픈하기 때문에 대용량의 바이너리 파일도 빠르게 열 수 있다.

pickle을 이용해 수집된 데이터를 파일로 저장하고, 불러올 수 있다.

16자리의 hex값을 2,4,8 자리로 split해서 볼 수 있다.

little / big endian을 설정할 수 있다.

D2Coding 폰트 사용

- SIL OPEN FONT LICENSE

Version 1.1 - 26 February 2007

- 코드 설명

1. Items.py

QData : Dataframe을 표로 바꾸기

QTable : table이 위치하는 곳

QCentralLabel : 가운데 정렬 라벨

2. FindFunction.py

Find : 검색 -> memory location / hex and string / prev and nex item

GoTo : 검색 결과로 이동

