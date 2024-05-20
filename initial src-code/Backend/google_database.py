from google.oauth2.service_account import Credentials
import gspread

class Database:
    def __init__(self, creds_path, book_name):
        self.creds_path = creds_path
        self.book_name = book_name
        self.client = None
        self.book = None
        self.sheet = None
        self.authenticate()
        self.open_workbook()
    


    def authenticate(self):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = Credentials.from_service_account_file(self.creds_path, scopes=scopes)
        self.client = gspread.authorize(creds)


    def open_workbook(self):
        self.book = self.client.open(self.book_name)
    
    def open_worksheet(self, sheet_name):
        book = self.book
        self.sheet = self.client.open(book).sheet_name

    def get_password(self, username):
        cell = self.sheet.find(username)
        row = cell.row
        column = 3
        passwd = cell(row,column).value
        return passwd
    
    def get_userinfo(self, username):
        cell = self.sheet.find(username)
        row = cell.row
        user_info = {}
        col_heads = ['Black', 'Account No', 'Username', 'Password', 'Name', 'Email', 'Phone No', 'Address']
        
        for col in range(1,8):
            user_info[col_heads[col]] = cell(row,col).value
        
        return user_info

    





    

    