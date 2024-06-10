# OOP_Course_Work
## made by student of the groupr EDIfu-23 Dmytro Rossokha
### Introduction
There was  implemented the application which keeps all key cards of the specific user, similar to Google Pay with bank cards. Currently, I have made on web implementation which works only on PC because there is no enough time to finish mobile application till the deadline. I decided to name it KeyWallet.
Main used technologies: Flask, MySQL
To run the program we need to launch next scripts:

.venv\Scripts\activate

$env:FLASK_APP = "main.py"

$env:FLASK_DEBUG = "1"

flask run

Then, we need to open XAMPP and run MySQL

![image](https://github.com/rossokhaadim/OOP_Course_Work/assets/162993195/553d81f0-a68f-4bba-8e1a-7cfd148f183d)
2.	Functions
### OOP principles used:
- Inheritance: <br />
Inheritance is a key concept in object-oriented programming (OOP) that allows a new class, called a subclass or derived class, to inherit properties and behaviors (methods) from an existing class, known as the superclass or base class. This mechanism promotes code reuse and establishes a hierarchical relationship between classes. The subclass can extend or override functionalities of the superclass, enabling more specific behavior. Inheritance supports the principle of "is-a" relationships, where the subclass is a specialized form of the superclass
```python
class Manager(metaclass = SingletonMeta):
class DatabaseHandler(Manager):
class PasswordManager(Manager):
class SessionManager(Manager):
```
- Abstraction: <br />
Abstraction is a fundamental concept in object-oriented programming (OOP) that focuses on simplifying complex systems by modeling classes appropriate to the problem. It involves highlighting the essential features of an object while hiding the unnecessary details. This helps in managing complexity by reducing and controlling the impact of changes
```python
class Manager(metaclass = SingletonMeta):
    def __init__(self, mysql):
        self.mysql = mysql

    @abstractmethod
    def get_user_by_username_and_password(self):
        pass
    @abstractmethod
    def get_card_by_account_id(self):
        pass

    @abstractmethod
    def get_account_data_by_username(self, username):
        pass

    @abstractmethod
    def get_account_data_by_id(self):
        pass

    @abstractmethod
    def insert_data_in_account(self):
        pass

    @abstractmethod
    def get_card_by_id(self):
        pass

    @abstractmethod
    def add_new_card(self):
        pass

    @abstractmethod
    def check_password(self):
        pass

    @abstractmethod
    def update_password(self):
        pass
```

- Encapsulation: <br />
Encapsulation is a fundamental principle of object-oriented programming (OOP) that focuses on bundling data (attributes) and methods (functions) that operate on that data into a single unit, known as a class. It also involves restricting direct access to some of the object's components, which is a means of preventing unintended interference and misuse of data. This is typically achieved through the use of access modifiers, such as private, protected, and public
```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class User(metaclass=SingletonMeta):
    def __init__(self):
        self.username = ""
        self.__password = ""
        self.__hashed_password = ""
        self.email = ""
        self.cards = []

    def get_password(self):
        return self.__password

    def get_hashed_password(self):
        return self.__hashed_password

    def input_password(self, password):
        self.__password = password

    def input_hashed_password(self, password):
        self.__hashed_password = password

class Card:
    def __init__(self):
        self.id = int()
        self.company_name = ""
        self.__key = ""
        self.img_path = ""

    def get_key(self):
        return self.__key

    def input_key(self, key):
        self.__key = key
```

- Polymorphism: <br />
Polymorphism is a core concept in object-oriented programming (OOP) that allows objects of different classes to be treated as objects of a common superclass. It enables a single interface to be used for a general class of actions. The specific action is determined by the exact nature of the situation, allowing for more flexible and reusable code.
 - Abstract Base Class (Manager) and its Subclasses
  ```python
   class Manager(metaclass = SingletonMeta):
    def __init__(self, mysql):
        self.mysql = mysql

    @abstractmethod
    def get_user_by_username_and_password(self):
        pass

    @abstractmethod
    def get_card_by_account_id(self):
        pass

    @abstractmethod
    def get_account_data_by_username(self, username):
        pass

    @abstractmethod
    def get_account_data_by_id(self):
        pass

    @abstractmethod
    def insert_data_in_account(self):
        pass

    @abstractmethod
    def get_card_by_id(self):
        pass

    @abstractmethod
    def add_new_card(self):
        pass

    @abstractmethod
    def check_password(self):
        pass

    @abstractmethod
    def update_password(self):
        pass


class DatabaseHandler(Manager):
   
class PasswordManager(Manager):
    @staticmethod
    def hash_password(password, secret_key):

class SessionManager(Manager):
    @staticmethod
    def is_logged_in():

    @staticmethod
    def logout():
  ```

 - Factory Method Pattern
 ```python
class Factory:
    @staticmethod
    def create_database_handler(mysql):
        dh = DatabaseHandler(mysql)
        return dh

    @staticmethod
    def use_session_manager():
        return SessionManager(None)

    @staticmethod
    def use_password_manager():
        return PasswordManager(None)
 ```

### Used design patterns
- Signleton
```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
```
- Factory Method <br />
Maybe the implementation is not enough detailed(no additional conditions) but it makes the code more readable
```python
class Factory:
    @staticmethod
    def create_database_handler(mysql):
        dh = DatabaseHandler(mysql)
        return dh

    @staticmethod
    def use_session_manager():
        return SessionManager(None)

    @staticmethod
    def use_password_manager():
        return PasswordManager(None)
```
### Additional things
- The script for QR-scanning was written on Java Script
  - This JavaScript code sets up a QR code scanner on a webpage that becomes active once the DOM is fully loaded. When a QR code is successfully scanned, the decoded text is sent via an AJAX POST request to a Flask backend endpoint (/process_qr_code). Depending on the server's response, the browser may redirect to a new URL or display an error message. The QR code scanner is initialized with specific parameters for frame rate and QR box size, and the scanning results are processed using the onScanSuccess callback function.
```js
function domReady(fn) {
    if (
        document.readyState === "complete" ||
        document.readyState === "interactive"
    ) {
        setTimeout(fn, 1000);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
}

domReady(function () {
    // If found your QR code
    function onScanSuccess(decodeText, decodeResult) {
        // Send the decoded text to Flask backend
        sendDataToBackend(decodeText);
    }

    // Function to send data to Flask backend
    function sendDataToBackend(data) {
        // Make an AJAX request
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/process_qr_code", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Parse the response JSON
                    var response = JSON.parse(xhr.responseText);
                    if (response.redirect_url) {
                        // Redirect to the provided URL
                        window.location.href = response.redirect_url;
                    } else if (response.error) {
                        // Handle error
                        alert(response.error);
                    }
                } else {
                    // Handle non-200 responses
                    alert("An error occurred: " + xhr.statusText);
                }
            }
        };
        xhr.send(JSON.stringify({ qr_data: data }));
    }

    let htmlscanner = new Html5QrcodeScanner(
        "my-qr-reader",
        { fps: 10, qrbos: 250 }
    );
    htmlscanner.render(onScanSuccess);
});

```
### Summary
To sum up, uring this coursewrok I have created a website based on Flask and MySQL. There were used all 4 OOP principles and Design Patterns such as Singleton and Factory Method. I am going to develop this project and made it as mobile app. Also, pay attention that it is just a model for representation and there extremely many things to develop





### Functionality

- Login Page
![image](https://github.com/rossokhaadim/OOP_Course_Work/assets/162993195/d70eb2f3-5383-4c3d-92d6-64a4983f7bc6)

- Register Page
![image](https://github.com/rossokhaadim/OOP_Course_Work/assets/162993195/3532c521-4647-40f5-9051-a508c91f9d70)

- Home Page
![image](https://github.com/rossokhaadim/OOP_Course_Work/assets/162993195/266c1fca-597b-414b-896e-52fe822734be)

- Card Page
![image](https://github.com/rossokhaadim/OOP_Course_Work/assets/162993195/b7c00bdd-9a4a-40b0-bbea-372f87cfac96)


- Profile Page
![image](https://github.com/rossokhaadim/OOP_Course_Work/assets/162993195/ac9e64ab-c817-4882-b7f9-ce19834b6b8b)

- Scan Page
![image](https://github.com/rossokhaadim/OOP_Course_Work/assets/162993195/e08ba46a-1d1b-4392-8f64-fe99e7105f59)

- QR-Generator
![image](https://github.com/rossokhaadim/OOP_Course_Work/assets/162993195/2ed8802a-369d-4cd5-a27e-405efc901909)


