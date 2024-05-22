from abc import abstractmethod

from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib



class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


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
    def get_cursor(self):
        mysql = self.mysql
        return mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    def get_user_by_username_and_password(self, username, password):
        cursor = self.get_cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        return cursor.fetchone()

    def get_card_by_account_id(self, account_id):
        dh = DatabaseHandler(self.mysql)
        cursor = dh.get_cursor()
        cursor.execute('SELECT * FROM cards WHERE account_id = %s', (account_id,))
        cards = cursor.fetchall()
        return cards

    def get_account_data_by_username(self, username):
        mysql = self.mysql
        dh = DatabaseHandler(mysql)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        return account

    def get_account_data_by_id(self, id):
        mysql = self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (id,))
        account = cursor.fetchone()
        return account

    def insert_data_in_account(self, username, password, email):
        mysql = self.mysql
        dh = DatabaseHandler(mysql)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
        mysql.connection.commit()
        # msg = 'You have successfully registered!'
        # return msg

    def get_card_by_id(self, card_id):
        mysql = self.mysql
        dh = DatabaseHandler(mysql)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cards WHERE ID = %s', (card_id,))
        card = cursor.fetchone()
        return card

    def add_new_card(self, card_key, card_company, img_path, user_id):
        mysql = self.mysql
        dh = DatabaseHandler(mysql)
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO cards (`key`, company, imp_path, account_id) VALUES (%s, %s, %s, %s)",
            (card_key, card_company, img_path, user_id)
        )
        mysql.connection.commit()
        cur.close()

    def check_password(self, account_id, password):
        print(account_id, password)
        mysql = self.mysql
        dh = DatabaseHandler(mysql)
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE id = %s AND password = %s', (account_id, password))
        account = cur.fetchone()
        return account

    def update_password(self, new_password, id):
        mysql = self.mysql
        dh = DatabaseHandler(mysql)
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Update the password in the database
        cur.execute('UPDATE accounts SET password = %s WHERE id = %s', (new_password, session['id']))
        mysql.connection.commit()



class PasswordManager(Manager):
    @staticmethod
    def hash_password(password, secret_key):
        hash = password + secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest()
        return password


class SessionManager(Manager):
    @staticmethod
    def is_logged_in():
        return 'loggedin' in session

    @staticmethod
    def logout():
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)



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
