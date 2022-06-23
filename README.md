# 백수 탈출

## 📢프로젝트 소개


개발 취준생들을 대상으로 하여 만든 사이트이다. 개발과 관련된 내용으로 된 퀴즈를 풀면서 지식을 증진시키고 배웠던 공부를 복습을 할 수 있다. 

![Untitled](https://user-images.githubusercontent.com/84106842/175197365-0944d186-29c2-4080-bf98-69a3f115903d.png)

  
## 🎬시연 영상


[백수 탈출](https://www.youtube.com/watch?v=FhEKosjdt3M&t=2s)

<br/>
  
## 📝와이어프레임


![Untitled (1)](https://user-images.githubusercontent.com/84106842/175197373-63f86c30-b1ee-45d4-8854-816ed7574936.png)

[와이어프레임 Canvas](https://app.tryeraser.com/workspace/gather:G8NVlGTiT7iRUF5ptable5?origin=share)

<br/>
  
## 📅프로젝트 기간


2022년 6월 20일 ~ 2021년 6월 23일 

<br/>

## ****🔨 개발툴****


- Server: AWS EC2 (Ubuntu 18.04 LTS)
- Framework: Flask (Python)
- Database: MongoDB
- View : HTML5, CSS3, Javascript, JQuery, bulma
- Design Tool (Canvas)
- Tool : Git, Notion

<br/>
  
## **👨🏻‍🤝‍👨🏻팀원**


- 김원영
- 신유근
- 임거정
- 백승한

<br/>
  
## 💡핵심 기능



### 회원가입 및 로그인

- 회원가입
    - 아이디 & 비밀번호 형식 확인
    - 아이디 중복 확인
    - DB에 아이디와 비밀번호 저장하여 회원가입 & 로그인 화면으로 전환
- 로그인
    - 아이디 & 비밀번호 입력 확인
    - 서버로 POST 요청을 보내 가입 정보가 존재하는지 확인
    - 회원일 경우 토큰 부여
- 로그아웃 시 토큰이 삭제되고 메인 페이지로 이동한다.

### 랭킹

- 데이터베이스에 저장된 User들을 불러와서 퀴즈 완료 시간으로 정렬하여 보여준다.
- 게임을 완료하면 랭킹 페이지로 이동한다.

### 취업공고

- 크롤링을 통하여 잡코리아 사이트의 취업공고를 보여준다.

### 퀴즈

- 퀴즈의 정답을 맞추면 캐릭터가 이동하고 다음 퀴즈로 넘어간다.
- 정답을 못 맞출시 재도전 및 메인페이지로 돌아갈 수 있다.

<br/>
  
## **💣 프로젝트 중 힘들었던 점**


- Git 협업 경험의 부재로 인한 프로젝트 관리의 어려움
- 잦은 컨플릭

<br/>
  
## 💫Trouble Shooting


- 새로고침을 하면 타이머가 리셋이 되는 문제
    - 새로고침 방지할 수 있는 KEYKODE를 작성
- 정답 란에 영어를 적으면 에러 발생
    - 변수 충돌로 인해 변수명을 다시 작성
- OG 타이틀 적용 문제
    - 로그인 페이지로 랜더링이 되는것을 메인페이지로 바꿈

<br/>
  
## **기타**


[백수탈출 노션](https://www.notion.so/2-52282b3eb11d4fecb6d21869b942bb92)
