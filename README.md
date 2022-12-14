# clean_mss_template π‘π½

Template for microservices repositories based in Clean Arch

## The Project π½

### Introduction and Objectives β

The main objective is to provide a template for repositories that can be used as a starting point for new projects. This
architecture is based on the Clean Architecture, and it was based in many other projects and books, articles that were
mixed by the students of MauΓ‘ Institute of Technology, from the academic group Dev. Community MauΓ‘.

### Reasons 1οΈβ£3οΈβ£

The project aims to help developers to start new projects with a good architecture, and with a good structure, so that anybody can create good applications.

### Clean Architecture π§Όπ°

The purpose of the project is to learn and create a Clean Architecture for microservices stateless with AWS Lambda which is a way of structuring
the code in layers, each of which has a
specific responsibility. This architecture is based on the principles of SOLID and books like "Clean Architecture: A
Craftsman's Guide to Software Structure and Design" by Robert C. Martin.

We also tried to explain for new programmers in the mos intuitive way and you can see the explanation here: [Clean Architecture Figma](https://www.figma.com/file/CmfQcH2xbZyIszPX0iOxPp/Clean-Arch---HackaBeckas?node-id=0%3A1&t=B38vNfX3VSv6qtU7-1)


### Folder Structure ππ΄π²π³

Our folder structure was developed specially for our projects. 


```bash
.
βββ iac
βββ src
βΒ Β  βββ modules
βΒ Β  βΒ Β  βββ create_user
βΒ Β  βΒ Β  βΒ Β  βββ app
βΒ Β  βΒ Β  βββ delete_user
βΒ Β  βΒ Β  βΒ Β  βββ app
βΒ Β  βΒ Β  βββ get_user
βΒ Β  βΒ Β  βΒ Β  βββ app
βΒ Β  βΒ Β  βββ update_user
βΒ Β  βΒ Β      βββ app
βΒ Β  βββ shared
βΒ Β      βββ domain
βΒ Β      βΒ Β  βββ entities
βΒ Β      βΒ Β  βββ enums
βΒ Β      βΒ Β  βββ repositories
βΒ Β      βββ helpers
βΒ Β      βΒ Β  βββ enum
βΒ Β      βΒ Β  βββ errors
βΒ Β      βΒ Β  βββ functions
βΒ Β      βΒ Β  βββ http
βΒ Β      βββ infra
βΒ Β          βββ dto
βΒ Β          βββ external
βΒ Β          βββ repositories
βββ tests
    βββ modules
    βΒ Β  βββ create_user
    βΒ Β  βΒ Β  βββ app
    βΒ Β  βββ delete_user
    βΒ Β  βΒ Β  βββ app
    βΒ Β  βββ get_user
    βΒ Β  βΒ Β  βββ app
    βΒ Β  βββ update_user
    βΒ Β      βββ app
    βββ shared
        βββ domain
        βΒ Β  βββ entities
        βββ helpers
        βββ infra

```


## Name Format π
### Files and Directories π

- Files have the same name as the classes
- snake_case π (ex: `./app/create_user_controller.py`)

### Classes π΄
- #### Pattern π

    - CamelCase π«πͺ

- #### Types π§­

    - **Interface** starts with "I" --> `IUserRepository`, `ISelfieRepository` π
    - **Repository** have the same name as interface, without the "I" and the type in final (ex: `UserRepositoryMock`, `SelfieRepositoryDynamo`) π₯¬
    - **Controller** ends with "Controller" --> `CreateUserController`, `GetSelfieController` π?
    - **Usecase** ends with "Usecase" --> `CreateUserUsecase`, `GetSelfieUsecase` π 
    - **Viewmodel** ends with "Viewmodel" --> `CreateUserViewmodel`, `GetSelfieViewmodel` π
    - **Presenter** ends with "Presenter" --> `CreateUserPresenter`, `GetSelfiePresenter`π

### Methods π¨βπ«

- snake_case π
- Try associate with a verb (ex: `create_user`, `get_user`, `update_selfie`)

### Variables π°

- snake_case π
- Avoid verbs

### Enums

- SNAKE_CASE π
- File name ends with "ENUM" (ex: "STATE_ENUM")

### Tests π

- snake_case π
- "test" follow by class name (ex: `test_cadastrar_usuario_valido`, `test_cadastrar_usuario_sem_email`)
    - The files must start with "test" to pytest recognition

### Commit π’

- Start with verb
- Ends with emoji π

## Installation π©βπ»

Clone the repository using template

### Create virtual ambient in python (only first time)

###### Windows

    python -m venv venv

###### Linux

    virtualenv -p python3.9 venv

### Activate the venv

###### Windows:

    venv\Scripts\activate

###### Linux:

    source venv/bin/activate

### Install the requirements

    pip install -r requirements-dev.txt

### Run the tests

    pytest

### To run local set .env file

    STAGE = TEST


## Contributors π°π€π°

- Bruno Vilardi - [Brvilardi](https://github.com/Brvilardi) π·ββοΈ
- Hector Guerrini - [hectorguerrini](https://github.com/hectorguerrini) π§ββοΈ
- JoΓ£o Branco - [JoaoVitorBranco](https://github.com/JoaoVitorBranco) π
- Vitor Soller - [VgsStudio](https://github.com/VgsStudio) π±βπ»

## Especial Thanks π

- [Dev. Community MauΓ‘](https://www.instagram.com/devcommunitymaua/)
- [Clean Architecture: A Craftsman's Guide to Software Structure and Design](https://www.amazon.com.br/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
- [Institute MauΓ‘ of Technology](https://www.maua.br/)



