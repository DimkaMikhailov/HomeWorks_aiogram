import asyncio
from sqlite3 import Error
import sqlite3
from typing import LiteralString

from config import db


class DataBase:
    def __init__(self):
        self.__con = sqlite3.connect(db, check_same_thread=False)
        self.__cur = self.__con.cursor()

        self.loop = asyncio.get_running_loop()

    def create_tables(self):
        tables = [
            '''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,
                                                telegram_id INTEGER UNIQUE,
                                                username VARCHAR(50),
                                                first_name VARCHAR(50),
                                                last_name VARCHAR(50)
                                                reference_link VARCHAR(50));''',
            '''CREATE TABLE IF NOT EXISTS reference_users(id INTEGER PRIMARY KEY, 
                                                          referral_telegram_id INTEGER,
                                                          referent_telegram_id INTEGER,
                                                          UNIQUE (referral_telegram_id, referent_telegram_id),
                                                          FOREIGN KEY (referral_telegram_id) REFERENCES users(telegram_id);'''

                  ]

        for table in tables:
            try:
                self.__cur.execute(table)
                self.__con.commit()
            except Error as e: print(e)

    async def async_create_tables(self):
        await self.loop.run_in_executor(None, self.create_tables)

    def insert_into_users(self, values):
        query = '''INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?);'''
        try:
            self.__cur.execute(query, values)
        except Error as e:
            print(e)

        self.__con.commit()

    async def async_insert_into_users(self, value):
        await self.loop.run_in_executor(None, self.insert_into_users, value)

    def select_user_for_username(self, username):
        result = []
        query = f"""SELECT * FROM users WHERE username='{username}';"""

        try:
            self.__cur.execute(query)
            result = self.__cur.fetchone()
        except Error as e: print(e)

        return result

    async def async_select_user_for_username(self, username):
        return await self.loop.run_in_executor(None, self.select_user_for_username, username)

    def select_user_for_first_name(self, first_name):
        result = []
        query = f"""SELECT * FROM users WHERE first_name='{first_name}';"""

        try:
            self.__cur.execute(query)
            result = self.__cur.fetchone()
        except Error as e:
            print(e)

        return result

    async def async_select_user_for_first_name(self, first_name):
        return await self.loop.run_in_executor(None, self.select_user_for_first_name, first_name)

    def select_user_for_id(self, user_id):
        result = []
        query = f"""SELECT * FROM users WHERE telegram_id='{user_id}';"""

        try:
            self.__cur.execute(query)
            result = self.__cur.fetchone()
        except Error as e:
            print(e)

        return result

    async def async_select_user_for_id(self, user_id):
        return await self.loop.run_in_executor(None, self.select_user_for_id, user_id)

    def update_user_ref_link(self, user_id, link):
        query = f"""UPDATE users SET link={link} WHERE telegram_id={user_id};"""
        try:
            self.__cur.execute(query)
        except Error as e:
            print(e)
        self.__con.commit()

    async def async_update_user_ref_link(self, user_id, link):
        await self.loop.run_in_executor(None, self.update_user_ref_link, user_id, link)

    def get_referral(self, by_link):
        result = []
        query = f'''SELECT * FROM reference_balance WHERE reference_link={by_link};'''
        if by_link:
            try:
                self.__cur.execute(query)
                result = self.__cur.fetchone()
            except Error as e: print(e)

        return result

    async def async_get_referral(self, by_link):
        return await self.loop.run_in_executor(None, self.get_referral, by_link)

    def references_in_pair(self, _from, to):
        result = []
        query = f'''SELECT * FROM reference_users WHERE referral_telegram_id={_from} AND referent_telegram_id={to};'''
        try:
            self.__cur.execute(query)
            result = self.__cur.fetchone()
        except Error as e: print(e)

        return result

    async def async_references_in_pair(self, _from, to):
        await self.loop.run_in_executor(None, self.references_in_pair, _from, to)

    def set_reference_pair(self, _from, to):
        query = f"""INSERT OR IGNORE INTO reference_users VALUES(NULL, {_from}, {to});"""
        try:
            self.__cur.execute(query)
        except Error as e: print(e)
        self.__con.commit()

    async def async_set_reference_pair(self, _from, to):
        await self.loop.run_in_executor(None, self.set_reference_pair, _from, to)

    def get_reference_list(self, user_id):
        headers = ['referable_id', 'username']
        result = []
        reference_list = []
        try:
            self.__cur.execute(f"""SELECT r.referent_telegram_id, u.username FROM reference_users AS r 
                                        LEFT JOIN users AS u ON r.referent_telegram_id = u.telegram_id
                                        WHERE r.referral_telegram_id={user_id};""")
            result = self.__cur.fetchall()
        except Error as e: print(e)

        if result:
            for row in result:
                reference_list.append(dict(zip(headers, row)))
        return reference_list

    async def async_get_reference_list(self, user_id):
        return await self.loop.run_in_executor(None, self.get_reference_list, user_id)

