코드 내 주요 관전 포인트

generator1 : 수동 생성
 - generator1.py : 수동 생성, 하드코딩
 - generator2.py : 수동 생성, 파일로부터 로딩

generator2 : 구조화, 객체화
 - main.py : user 데이터 생성을 객체지향 설계

generator3 : 코드 확장
 - main.py : 출력 포멧의 확장

generator4 : 코드 확장
 - store_generator.py : 새로운 데이터 타입의 추가

generator5 : 코드 리펙토링, 모듈화
 - generators/common/*
 - models/*
 - test/*
 - output.py

generator6 : 코드 확장
 - generators/item/* : 새로운 데이터 타입의 추가
 - models/item.py

generator7 : 리펙토링, 중복 제거 및 코드 간소화/구조화
 - main1.py : output.py 내용으로 중복 코드 이동 및 간소화
 - main2.py : 새로운 타입(order) 을 추가하기 위한 방안 리뷰
 - main3.py : 디자인 패턴(factory) 등을 적용하기 위한 방안 리뷰 및 구조화
 - main4.py : 새로운 패턴을 등록(register) 하기 위한 구조 설계

generator8 : 리펙토링, 구조개선 (객체 지향 설계 개선 및 디자인 패턴 적용) 
 - main5.py : 새로운 타입을 객체 지향적인 설계를 통해 구조 개선
 - generators/__init__.py

generator9 : 코드 확장
 - generators/order/* : 새로운 타입 (order/orderitem) 추가
 - models/order.py
 - models/orderitem.py

generator10 : 전체 리펙토링 및 중복 제거, 코드 간소화
 - main.py
 - output.py : 새로운 데이터 타입 추가로 인한 출력 시 불편함 해결
 - models/* : 출력코드등 모두 모델로 이동
 - models/basemodel.py : abstract class 와 상속을 통한 필수 함수 오버라이딩을 통한 개별 구현



====================

user.csv - 고객DB
Id,Name,Gender,Age,Birthdate,Address
2dfec01b-0a2e-49ce-80dd-3c1bc3388e4a,조지훈,Female,48,1974-07-13,대구 강남구 2로 59
1365f7d4-f7f3-4695-9609-b3e7f4904ba1,윤지아,Female,20,2003-04-10,대구 서구 54길 21
f46de106-5a36-408a-bab9-abf2287acf1d,윤지원,Male,52,1971-02-18,대구 서구 59길 71
d616ba74-822d-4047-8d22-f90dc5f280e2,윤민지,Female,19,2003-08-14,인천 중구 61로 18
a3500ca3-643c-4853-ba0c-98da276c5de9,김지아,Female,29,1993-08-09,대구 강서구 100길 61


store.csv - 상점DB
Id,Name,Type,Address
09046a45-9d98-465e-86fc-0dca8d68299e,스타벅스 신촌4호점,스타벅스,서울 남구 48로 53
1342b08e-6a37-42e3-be4a-737c74358300,투썸 홍대3호점,투썸,서울 강남구 34로 73
b713d31d-abfe-4085-85df-7759cd89453e,이디야 송파2호점,이디야,대구 중구 79로 80
2a2b7c2f-2d4c-43f1-8ee7-af7a22ff0f32,스타벅스 서초2호점,스타벅스,광주 강서구 66로 25
2b5458ff-f006-4792-9ac5-7dd6162adf86,이디야 송파7호점,이디야,대구 남구 86길 13


item.csv - 상품DB
Id,Name,Type,UnitPrice
72c09e2b-f170-40a7-ac71-b9b939ea8b47,Espresso Coffee,Coffee,2500
cb2e72af-1c19-4db8-a703-a41fcb895968,Americano Coffee,Coffee,3000
ac6e6e61-2d9d-40c0-9d41-80e675857eca,Grape Juice,Juice,3000
c09d0b02-3392-4061-ba0f-ce0cb421ae94,Mocha Coffee,Coffee,5000
65553ac2-1e11-479b-8605-2a28e469883e,Mocha Coffee,Coffee,5000


order.csv - 주문DB
Id,OrderAt,StoreId,UserId
42362a10-11db-4ab1-924a-62e232ca9e94,2023-02-08 20:34:13,2b5458ff-f006-4792-9ac5-7dd6162adf86,2dfec01b-0a2e-49ce-80dd-3c1bc3388e4a
8e4e5fce-e40d-4184-a310-86e451cabfaf,2023-07-27 10:08:18,2a2b7c2f-2d4c-43f1-8ee7-af7a22ff0f32,2dfec01b-0a2e-49ce-80dd-3c1bc3388e4a
e709ee4b-a56f-49e8-808b-a4cad78bc823,2023-09-16 08:06:53,2b5458ff-f006-4792-9ac5-7dd6162adf86,f46de106-5a36-408a-bab9-abf2287acf1d
ef12f5a2-4356-4603-8ba2-eb78e8eac0a4,2023-10-13 21:35:09,1342b08e-6a37-42e3-be4a-737c74358300,f46de106-5a36-408a-bab9-abf2287acf1d
81b64f16-853e-4914-bb34-4387d4c2cf8c,2023-03-19 21:35:41,1342b08e-6a37-42e3-be4a-737c74358300,2dfec01b-0a2e-49ce-80dd-3c1bc3388e4a


order_item.csv - 주문상품DB
Id,OrderId,ItemId
752766cb-18a1-44ce-87cf-c2851a923f7c,42362a10-11db-4ab1-924a-62e232ca9e94,65553ac2-1e11-479b-8605-2a28e469883e
7ed2c346-aba2-4f4b-a581-569c6af14b09,e709ee4b-a56f-49e8-808b-a4cad78bc823,c09d0b02-3392-4061-ba0f-ce0cb421ae94
88a4191b-73e6-4793-85cc-2ccb4fd0b1c1,81b64f16-853e-4914-bb34-4387d4c2cf8c,72c09e2b-f170-40a7-ac71-b9b939ea8b47
b1904f4b-3c26-4384-af25-729654b1370f,e709ee4b-a56f-49e8-808b-a4cad78bc823,c09d0b02-3392-4061-ba0f-ce0cb421ae94
406cfa69-2f8a-4951-9e8f-525b1f41e6c0,81b64f16-853e-4914-bb34-4387d4c2cf8c,c09d0b02-3392-4061-ba0f-ce0cb421ae94

