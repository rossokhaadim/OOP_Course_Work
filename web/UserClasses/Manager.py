from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
class Manager:
    def __init__(self, mysql):
        self.mysql = mysql


class DatabaseHandler(Manager):
    # @staticmethod
    def get_cursor(self):
        mysql = self.mysql
        return mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # @staticmethod
    def get_user_by_username_and_password(self, username, password):
        cursor = self.get_cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        return cursor.fetchone()

    # @staticmethod
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

    def get_account_data_by_id(self, username):
        mysql = self.mysql
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
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


class SessionManager(Manager):
    @staticmethod
    def is_logged_in():
        return 'loggedin' in session

    @staticmethod
    def logout():
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)


class TemplateRenderer(Manager):
    @staticmethod
    def render(template, **kwargs):
        return render_template(template, **kwargs)