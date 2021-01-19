# wecode-14-brandi-team-project-backend

![브랜디](/img/brandi_logo.png)

<br>

# 프로젝트 개요

### 1. 프로젝트 설명
여성 온라인 쇼핑몰 [브랜디](https://www.brandi.co.kr/) 의 서비스/어드민 기능 구현 프로젝트.
* **`서비스`** - 실제 유저가 웹사이트에 들어와 상품을 보고 구매를 진행하는 등의 기능.
* **`어드민`** - 관리자 기능으로써 회원관리(유저, 셀러, 관리자)와 상품 관리 및 결제 완료 후의 과정에 대한 기능.

### 2. 프로젝트 목적
* E-Commerce 애플리케이션의 실제 업무 중 발생할 수 있는 이슈에 대한 고려, 그에 따른 정책 설정.
* 대량 데이터 적재/확장성을 고려한 데이터 베이스 모델링
* Flask Web Framework 채용하여 Raw Query 로 DAO 단을 처리 및 Service/DAO 개념 도입 (MVC)
* Transaction 처리의 이해
* 서비스 및 관리자 기능에 대한 비지니스 로직 설계/구현

### 3. 프로젝트 기간 / 참여 인원
+ 2020/12/14 ~ 2021/01/07
+ 총 12인
    - **`Frontend`**
        * **이승윤 (서비스)**
        * **장호철 (어드민1)**
        * **장재윤 (어드민2)**
        
    - **`Backend`**  : 
        * **고수희, 김기용, 김민구 (서비스)** 
        * **강두연, 김민서, 이성보 (어드민1)**
        * **김영환, 심원두(PM), 이영주 (어드민2)**


### 4. 모델링
[모델링 보러 가기](https://aquerytool.com:443/aquerymain/index/?rurl=0887ed6d-54f3-4ce7-a4be-ca4cd385cc77) : password (***8sc484***)


### 5. API문서 보러가기
* [클릭](https://www.notion.so/14th-Brandi-API-a35616653ef147818e228c9920d87a96)


### 6. 사용한 기술 스택
+ Bankend
    - Python 3.7
    - MySQL
    - Flask Web Framework
    - Package(Boto3, Pillow, bcrypt, PyJWT, PyMySQL)
    - AWS (Amazon S3)

<br>

# 기능 구현 및 담당자

|구분       | 앱 이름     | API 설명             | 담당자   |
|:---------|:-----------|:--------------------|:--------|
| SERVICE  | user       | 회원가입               | 김민구      |
| SERVICE  | user       | 로그인                | 김민구      |
| SERVICE  | user       | 소셜 로그인            | 김민구      |
| SERVICE  | product    | 메인 상품 카테고리 출력  | 김민구      |
| SERVICE  | product    | 메인 상품 리스트        | 김민구      |
| SERVICE  | product    | 상품 검색              | 김기용     |
| SERVICE  | product    | 상품 상세 정보 조회      | 김기용     |
| SERVICE  | product    | 상품 Q&A 리스트 조회    | 김민구      |
| SERVICE  | product    | 상품 Q&A 작성          | 김민구      |
| SERVICE  | product    | 상품 Q&A 삭제          | 김민구      |
| SERVICE  | shop       | 셀러 상품 리스트()      | 고수희      |
| SERVICE  | shop       | 셀러 카테고리          | 고수희      |
| SERVICE  | shop       | 셀러 상품 검색         | 고수희      |
| SERVICE  | shop       | 셀러 정보 조회         | 고수희      |
| SERVICE  | checkout   | [바로구매] 장바구니 상품 추가        | 고수희    |
| SERVICE  | checkout   | [바로구매] 장바구니 상품 조회        | 고수희    |
| SERVICE  | checkout   | [바로구매] 상품 결제 추가           | 고수희    |
| SERVICE  | checkout   | [바로구매] 상품 결제 완료 결과 조회   | 고수희    |
| SERVICE  | checkout   | 주문자 정보 조회                  | 고수희    |
| SERVICE  | checkout   | 배송지 정보 생성                  | 김기용    |
| SERVICE  | checkout   | 회원의 배송지 정보 조회            | 김기용    |
| SERVICE  | checkout   | 배송지 정보 상세 조회             | 김기용    |
| SERVICE  | checkout   | 배송지 정보 수정                 | 김기용    |
| SERVICE  | checkout   | 배송지 정보 삭제                 | 김기용    |
| SERVICE  | mypage   | 주문 정보 리스트 조회 | 김기용    |
| SERVICE  | mypage   | 주문 정보 상세 조회   | 김기용    |
| SERVICE  | mypage   | 주문 취소/ 구매 확정  | 김기용    |
| SERVICE  | mypage   | QA 리스트 조회       | 김기용    |
| SERVICE  | event | 기획전 베너 리스트 조회     | 김민구    |
| SERVICE  | event | 기획전 상세 정보 조회       | 김민구    |
| SERVICE  | event | 기획전 상세 버튼 리스트 조회 | 김민구    |
| SERVICE  | event | 기획전 상세 상품 리스트 조회 | 김민구    |
| SERVICE  | event | 상품 북마크 추가           | 김민구    |
| SERVICE  | event | 상품 북마크 삭제           | 김민구    |
| ADMIN  | dashboard | 관리자 카테고리 출력     | 김영환    |
| ADMIN  | seller    | 셀러 회원가입           | 김영환    |
| ADMIN  | seller    | 셀러 로그인            | 김영환    |
| ADMIN  | seller    | 셀러 계정 리스트        | 김영환    |
| ADMIN  | seller    | 셀러 계정 상세 정보     | 이영주    |
| ADMIN  | seller    | 셀러 계정 상세 정보 변경 | 이영주    |
| ADMIN  | seller    | 셀러 검색              | 김영환    |
| ADMIN  | seller    | 셀러 상태 변경          | 이영주    |
| ADMIN  | seller    | 셀러 비밀번호 변경       | 이영주    |
| ADMIN  | seller    | 셀러 상세 히스토리 조회   | 이영주    |
| ADMIN  | seller | 엑셀 다운로드           | 장재원    |
| ADMIN  | product | 상품 등록 초기화면     | 심원두   |
| ADMIN  | product | 상품 등록            | 심원두    |
| ADMIN  | product | 상품 상세 정보 조회    | 심원두    |
| ADMIN  | product | 상품 상세 정보 수정    | 심원두    |
| ADMIN  | product | 상품 정보 리스트(검색) | 심원두    |
| ADMIN  | product | 일괄 수정 | 장재원    |
| ADMIN  | product | 엑셀 다운로드 | 장재원    |
| ADMIN  | order | 주문 리스트 조회  | 김민서    |
| ADMIN  | order | 주문 관리 상태 변경  | 김민서    |
| ADMIN  | order | 주문 정보 상세 조회  | 김민서    |
| ADMIN  | order | 주문 상세 정보 변경  | 김민서    |
| ADMIN  | order | 엑셀 다운로드       | 김민서    |
| ADMIN  | event | 기획전 등록           | 강두연    |
| ADMIN  | event | 기획전 리스트 조회     | 강두연    |
| ADMIN  | event | 기획전 상세 조회       | 강두연    |
| ADMIN  | event | 기획전 수정           | 강두연    |
| ADMIN  | event | 기획전 삭제           | 이성보    |
| ADMIN  | order | 주문 리스트 조회      | 이성보    |
| ADMIN  | order | 주문 관리 상태 변경   | 이성보    |
| ADMIN  | order | 엑셀 다운로드        | 이성보    |
| ADMIN  | dashboard | 홈             | 이성보    |

<br>

# Refactoring Plan (~ 2021.01.31)

### 기능 리펙토링 
- **[상품 관리 / 회원 관리] 리펙토링**
    - ~~상품 등록 초기화면~~
    - 상품 등록
    - 상품 상세 정보 조회
    - 상품 상세 정보 수정
    - 상품 정보 리스트(검색)
    - 상품 일괄 수정
    - 셀러 회원가입
    - 셀러 로그인
    - 셀러 계정 리스트
    - 셀러 계정 상세 정보
    - 셀러 계정 상세 정보 변경
    - 셀러 검색
    - 셀러 상태 변경
    - 셀러 비밀번호 변경
    - 셀러 상세 히스토리 조회
    - 엑셀 다운로드

### 공통 모듈 및 컨벤션
- const.py 작성 (상수 관리 / 매직 넘버 포함 하드 코딩 제거)
- Request Validate 에 사용되는 Rule 클래스 정리
- 서비스단 유효성 체크 모듈 정리
- 에러 메세지 컨벤션 통일
- 코드 컨벤션 맞추기
- 로그 수집 도입 (like log4j)  
 
<br>

# License
* 저작권이 없는 사진을 사용하였습니다.
* 기술 증진의 목적으로 만들어진 프로젝트입니다.
* 무단으로 카피하여 사용하는 것을 금지합니다.
