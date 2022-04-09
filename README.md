# Hexa Viewer

-라이브러리
PyQt5

- 기능
바이너리 파일을 열어서 line(=주소), hex, string 포맷으로 출력한다.

- 특징
파일을 한번에 다 열지 않고 필요한 line만 오픈하기 때문에 파일 크기 대비 ram 용량을 거의 차지하지 않는다.

pickle을 이용해 수집된 데이터를 파일로 저장하고, 불러올 수 있다.

16자리의 hex값을 2,4,8 자리로 split해서 볼 수 있다.

little / big endian을 설정할 수 있다.
