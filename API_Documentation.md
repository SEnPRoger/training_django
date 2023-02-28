<div id="main"></div>

# 👋 Ласкаво просимо до документації API v1.0

(Версiя вiд 27 лют. 2023 р.)
У цій документації будуть наведені приклади запитів до сервера та відповіді від нього, а також опис прикладів помилок валідації при обробці вхідного запиту. Документацiя буде оновлюватися.

### Перелiк доступних запитiв:

Акаунт користувача
* [Реєстрація](#register)
* [Авторизація](#login)
* [Загальна інформація про користувача](#detail_public)
* [Детальна особиста інформація про користувача](#detail_private)
* [Зміна нікнейму](#change_username)
* [Зміна паролю](#change_password)
* [Завантаження фотографії профілю](#upload_photo)
* [Перевiрка на унiкальнiсть нiкнейму](#available_username)
* [Перевiрка на унiкальнiсть email](#available_email)
* [Вихiд з акаунту](#logout_account)
* [Видалення акаунту](#delete_account)

<div id="register"></div>

# 🚪 Реєстрація

### 📬 *Адреса для запиту:* **`/api/account/register/`**
*Тип запиту:* **POST**

💬*Приклад запиту до сервера: (JSON)*

> ```json 
> {
>     "email": "senproger@gmail.com", 
>     "username": "SEnPRoger",
>     "password": "1234", 
>     "password2": "1234"
> }
> ```

✔️*Приклад вiдповiдi вiд сервера: (JSON)*

> ```json 
> {
>     "status": "successfully registered",
>     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
> }
> ```

❌*Приклад вiдповiдi вiд сервера у випадку невдачi : (JSON)*
> ```json 
> {
>     "username":  [
>         "account with this Username already exists."
>     ],
>     "email":  [
>         "account with this Email already exists."
>     ]
> }
> ```

❌ або якщо email не валiдний:

> ```json
> {
>     "email":  [
>         "Enter a valid email address."
>     ]
> }
>  ```

### 📢 ВАЖЛИВО: Refresh-token буде записаний до cookies зi значенням `refresh_cookie`, а Access-token у виглядi вiдповiдi для подальшого використання запитiв, що потребують авторизованого пiдключення.
[До початку документації👆](#main)

<div id="login"></div>

# 🔑 Авторизація

### 📬 *Адреса для запиту:* **`/api/account/login/`**
*Тип запиту:* **POST**

💬*Приклад запиту до сервера: (JSON)*

> ```json
>  {
>     "username_or_email": "senproger@gmail.com" // або SEnPRoger
>     "password": "1234"
>  }
>  ```

✔️*Приклад вiдповiдi вiд сервера: (JSON)*

> ```json
> {
>     "status": "successfully logged",
>     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
> }
>  ```

❌*Приклад вiдповiдi вiд сервера у випадку невдачi : (JSON)*
>  ```json
>  {
>      "status": "account not found!"
>  }
>  ```

### 📢 ВАЖЛИВО: Refresh-token буде записаний до cookies зi значенням `refresh_cookie`, а Access-token у виглядi вiдповiдi для подальшого використання запитiв, що потребують авторизованого пiдключення.

[До початку документації👆](#main)

<div id="detail_public"></div>

# 👦🏼 Загальна інформація про користувача

### 📬 *Адреса для запиту:* **`/api/account/`{username}`/`**
*Тип запиту:* **GET**

✔️*Приклад вiдповiдi вiд сервера: (JSON)*

> ```json
>  {
>    "status": "successfully got account",
>    "account": {
>        "username": "SEnPRoger",
>        "photo": "/media/accounts/2/SEnPRoger_nX76Jvt.gif",
>        "is_moderator": true,
>        "created_at": "26 February 2023 17:41"
>    }
>  }
>  ```

[До початку документації👆](#main)

<div id="detail_private"></div>

# 👦🏼 Детальна інформація про користувача

### 📬 *Адреса для запиту:* **`/api/account/detail/`**
*Тип запиту:* **GET**

*Cookie:* `refesh_cookie`
> ❗️ Cookie повинен мiстити ключ `refesh_cookie` та мати значення
> у виглядi Refresh-token (httpOnly)

*Header:* `Authorization:  Bearer  <access-token>`
> ❗️ Header (заголовок запиту) повинен мiстити ключ Authorization та мати
> значення у виглядi Access-token

✔️*Приклад вiдповiдi вiд сервера: (JSON)*

> ```json
>  {
>     "status":  "success",
>     "account":  {
>     	"username":  "SEnPRoger",
>     	"email":  "senproger@gmail.com",
>     	"photo":  "/media/accounts/2/SEnPRoger.jpg", //or null
> 	"is_moderator":  false,
>     	"created_at":  "26 February 2023 17:41", //2023-02-18T07:42:32.695287+02:00 (raw version as option)
>     	"changed_username":  "26 February 2023 17:41"
>     }
>   }
>  ```

❌[Приклад вiдповiдi вiд сервера у випадку невалiдного **Access-token**](#invalid_token)
 
### 📢 ВАЖЛИВО: Refresh-token буде записаний до cookies зi значенням `refresh_cookie`, а Access-token у виглядi вiдповiдi для подальшого використання запитiв, що потребують авторизованого пiдключення.

[До початку документації👆](#main)

<div id="change_username"></div>

# ✍️ Зміна нікнейму

### 📬 *Адреса для запиту:* **`/api/account/change_username/`**
*Тип запиту:* **POST**

*Cookie:* `refesh_cookie`
> ❗️ Cookie повинен мiстити ключ `refesh_cookie` та мати значення
> у виглядi Refresh-token (httpOnly)

*Header:* `Authorization:  Bearer  <access-token>`
> ❗️ Header (заголовок запиту) повинен мiстити ключ Authorization та мати
> значення у виглядi Access-token

💬*Приклад запиту до сервера: (JSON)*

> ```json
> {
>     "username": "SEnPRoger2"
> }
> ``` 

✔️*Приклад вiдповiдi вiд сервера: (JSON)*

> ```json
> {
>     "status": "successfully changed nickname"
> }
> ``` 

❌*Приклад вiдповiдi вiд сервера у випадку невдачi : (JSON)*

>    ```json
>    {
>     	"status": "username change available once at day"
>    }
>    ``` 
❌ або якщо користувач з таким username вже є у системi:
>    ```json
>    {
>     	"username":  [
>     		"account with this Username already exists."
>     	]
>    }
>    ``` 

❌[Приклад вiдповiдi вiд сервера у випадку невалiдного **Access-token**](#invalid_token)

[До початку документації👆](#main)

<div id="change_password"></div>

# 🔒 Зміна паролю

### 📬 *Адреса для запиту:* **`/api/account/change_password/`**
*Тип запиту:* **POST**

*Cookie:* `refesh_cookie`
> ❗️ Cookie повинен мiстити ключ `refesh_cookie` та мати значення
> у виглядi Refresh-token (httpOnly)

*Header:* `Authorization:  Bearer  <access-token>`
> ❗️ Header (заголовок запиту) повинен мiстити ключ Authorization та мати
> значення у виглядi Access-token

💬*Приклад запиту до сервера: (JSON)*

> ```json
>  {
>     "password": "1234",
>     "password2": "1234"
>  }
>  ``` 

✔️*Приклад вiдповiдi вiд сервера: (JSON)*

> ```json
> {
>     "status": "successfully changed passsword"
> }
> ``` 

❌*Приклад вiдповiдi вiд сервера у випадку невдачi : (JSON)*
> ```json
> {
>     "non_field_errors":  [
>     		"Both passwords should be equal"
>     ]
> }
>    ```

❌[Приклад вiдповiдi вiд сервера у випадку невалiдного **Access-token**](#invalid_token)

[До початку документації👆](#main)

<div id="upload_photo"></div>

# 📷 Завантаження фотографії профілю

### 📬 *Адреса для запиту:* **`/api/account/upload_photo/`**
*Тип запиту:* **POST**

*Cookie:* `refesh_cookie`
> ❗️ Cookie повинен мiстити ключ `refesh_cookie` та мати значення
> у виглядi Refresh-token (httpOnly)

*Header:* `Authorization:  Bearer  <access-token>`
> ❗️ Header (заголовок запиту) повинен мiстити ключ Authorization та мати
> значення у виглядi Access-token

💬*Приклад запиту до сервера: (JSON)*

>    ```json
>    {
>     	"file": "SEnPRoger.jpg"
>    }
>    ```

✔️*Приклад вiдповiдi вiд сервера: (JSON)*

>    ```json
>    {
>     	"status": "successfully uploaded photo"
>    }
>    ```

**📢 ВАЖЛИВО: користувачi, що не мають статус Moredator, не можуть завантажувати у якостi фотографії профiлю файли з розширенням (.gif).
Загалом дозволенi такi формати файлiв: .jpg, .png та .gif для модераторiв.**

❌*Приклад вiдповiдi вiд сервера у випадку невдачi : (JSON)*
>    ```json
>    {
>     	"status": "you cannot upload gif as account photo"
>    }
>    ```
❌[Приклад вiдповiдi вiд сервера у випадку невалiдного **Access-token**](#invalid_token)

[До початку документації👆](#main)

<div id="available_username"></div>

# ✒️ Перевiрка на унiкальнiсть нiкнейму

### 📬 *Адреса для запиту:* **`/api/account/available_username/`**
*Тип запиту:* **GET**

💬*Приклад запиту до сервера: (JSON)*

>    ```json
>    {
>     	"username": "SEnPRoger2"
>    }
>    ```

✔️*Приклад вiдповiдi вiд сервера: (JSON)*
>    ```json
>    {
>     	"status": "username available"
>    }
>    ```

❌*Приклад вiдповiдi вiд сервера у випадку невдачi : (JSON)*
>    ```json
>    {
>     	"username":  [
>     		"account with this Username already exists."
>     	]
>    }
>    ```

❌ або якщо username не бiльше за 3 символи:

>    ```json
>    {
>     	"status": "username should be have more then 3 characters"
>    }
>    ```

[До початку документації👆](#main)

<div id="available_email"></div>

# ✉️ Перевiрка на унiкальнiсть email

### 📬 *Адреса для запиту:* **`/api/account/available_email/`**
*Тип запиту:* **GET**

💬*Приклад запиту до сервера: (JSON)*

>    ```json
>    {
>     	"email": "senproger2@gmail.com"
>    }
>    ```

✔️*Приклад вiдповiдi вiд сервера: (JSON)*
>    ```json
>    {
>     	"status": "email available"
>    }
>    ```

❌*Приклад вiдповiдi вiд сервера у випадку невдачi : (JSON)*
>    ```json
>    {
>     	"username":  [
>     		"account with this Email already exists."
>     	]
>    }
>    ```
[До початку документації👆](#main)

<div id="logout_account"></div>

# 🐾 Вихiд з акаунту

### 📬 *Адреса для запиту:* **`/api/account/logout/`**
*Тип запиту:* **POST**
*Cookie:* `refesh_cookie`
> ❗️ Cookie повинен мiстити ключ `refesh_cookie` та мати значення
> у виглядi Refresh-token (httpOnly)

*Header:* `Authorization:  Bearer  <access-token>`
> ❗️ Header (заголовок запиту) повинен мiстити ключ Authorization та мати
> значення у виглядi Access-token

✔️*Приклад вiдповiдi вiд сервера: (JSON)*
>    ```json
>    {
>     	"status": "successfully logout from account!"
>    }
>    ```

❌[Приклад вiдповiдi вiд сервера у випадку невалiдного **Access-token**](#invalid_token)

[До початку документації👆](#main)

 <div id="delete_account"></div>
 
# 🧹 Видалення акаунту

### 📬 *Адреса для запиту:* **`/api/account/delete/`**
*Тип запиту:* **POST**

*Cookie:* `refesh_cookie`
> ❗️ Cookie повинен мiстити ключ `refesh_cookie` та мати значення
> у виглядi Refresh-token (httpOnly)

*Header:* `Authorization:  Bearer  <access-token>`
> ❗️ Header (заголовок запиту) повинен мiстити ключ Authorization та мати
> значення у виглядi Access-token

✔️*Приклад вiдповiдi вiд сервера: (JSON)*
>    ```json
>    {
>     	"status": "successfully deleted account"
>    }
>    ```

❌[Приклад вiдповiдi вiд сервера у випадку невалiдного **Access-token**](#invalid_token)

[До початку документації👆](#main)

<div id="invalid_token"></div>

# 🔖 Невалiдний Access-token

  **Access-token** необхiдний для пiдтвердження особи, що увiйшла до системи.
> Час життя Access-token: **5 хвилин (у тестовому режимi 1 хвилину)**

У випадку невалiдностi Access-token потрiбно за допомогою основного (**Refresh-token**) оновити його. Iнакше система не надасть доступ до iнформацiї за запитом до url з правом доступу **IsAuthenticated**.
> Час життя Refresh-token: **21 день (у тестовому режимi 3 хвилини)**

❌*Приклад вiдповiдi вiд сервера у випадку невалiдного **Access-token** : (JSON)*

*Якщо Refresh-token дiйсний:*
>    ```json
>    {
>     	"status": "Access token is not valid",
>     	"detail": "Token has expired or incorrect",
>     	"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
>    }
>    ```

*Якщо Refresh-token НЕ дiйсний:*
>    ```json
>    {
>     	"status": "Refresh token is not valid",
>     	"detail": "Token has expired or incorrect"
>    }
>    ```

*Або:*
>    ```json
>    {
>     	"detail": "Authentication credentials were not provided."
>    }
>    ```

[До початку документації👆](#main)


