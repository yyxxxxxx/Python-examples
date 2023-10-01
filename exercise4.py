import sqlite3


class LibraryManagementSystem:
    def __init__(self):
        self.conn = sqlite3.connect('library.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                            BookID TEXT PRIMARY KEY,
                            Title TEXT,
                            Author TEXT,
                            ISBN TEXT,
                            Status TEXT
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                            UserID TEXT PRIMARY KEY,
                            Name TEXT,
                            Email TEXT
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                            ReservationID TEXT PRIMARY KEY,
                            BookID TEXT,
                            UserID TEXT,
                            ReservationDate TEXT,
                            FOREIGN KEY (BookID) REFERENCES Books (BookID),
                            FOREIGN KEY (UserID) REFERENCES Users (UserID)
                        )''')
        self.conn.commit()

    def add_book(self, book_id, title, author, isbn, status):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO Books (BookID, Title, Author, ISBN, Status)
                          VALUES (?, ?, ?, ?, ?)''', (book_id, title, author, isbn, status))
        self.conn.commit()
        print("Book added successfully.")

    def search_book(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT * FROM Books WHERE BookID = ?''', (book_id,))
        return cursor.fetchone()

    def find_book_detail(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT Books.*, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Books.BookID = ?''', (book_id,))
        result = cursor.fetchone()
        if result:
            book_details = {
                'BookID': result[0],
                'Title': result[1],
                'Author': result[2],
                'ISBN': result[3],
                'Status': result[4],
                'ReservedBy': {
                    'Name': result[5],
                    'Email': result[6]
                } if result[5] else None
            }
            print(book_details)
        else:
            print("No books were found.")

    def find_reservation_status(self, query):
        cursor = self.conn.cursor()
        if query.startswith('LB'):
            cursor.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                              FROM Books
                              LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                              LEFT JOIN Users ON Reservations.UserID = Users.UserID
                              WHERE Books.BookID = ?''', (query,))
        elif query.startswith('LU'):
            cursor.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                              FROM Books
                              LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                              LEFT JOIN Users ON Reservations.UserID = Users.UserID
                              WHERE Users.UserID = ?''', (query,))
        elif query.startswith('LR'):
            cursor.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                              FROM Books
                              LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                              LEFT JOIN Users ON Reservations.UserID = Users.UserID
                              WHERE Reservations.ReservationID = ?''', (query,))
        else:
            cursor.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
                              FROM Books
                              LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                              LEFT JOIN Users ON Reservations.UserID = Users.UserID
                              WHERE Books.Title LIKE ?''', ('%' + query + '%',))

        result = cursor.fetchall()
        if result:
            for row in result:
                if row[0]:
                    book_details = {
                        'BookID': row[0],
                        'Title': row[1],
                        'Status': row[2],
                        'ReservedBy': {
                            'Name': row[3],
                            'Email': row[4]
                        } if row[3] else None
                    }
                    print(book_details)
                else:
                    print("No reservation found.")
        else:
            print("This book doesn't exist in the database.")

    def find_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT Books.*, Users.Name, Users.Email
                          FROM Books
                          LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                          LEFT JOIN Users ON Reservations.UserID = Users.UserID''')
        result = cursor.fetchall()
        if result:
            for row in result:
                book_details = {
                    'BookID': row[0],
                    'Title': row[1],
                    'Author': row[2],
                    'ISBN': row[3],
                    'Status': row[4],
                    'ReservedBy': {
                        'Name': row[5],
                        'Email': row[6]
                    } if row[5] else None
                }
                print(book_details)
        else:
            print("No books found.")

    def update_book_details(self, book_id, **kwargs):
        cursor = self.conn.cursor()
        if 'status' in kwargs and (kwargs['status'] == 'Available'):
            cursor.execute('''UPDATE Books SET Status = ? WHERE BookID = ?''', (kwargs['status'], book_id))
            cursor.execute('''DELETE FROM Reservations WHERE BookID = ?''', (book_id,))
        elif 'title' in kwargs:
            new_title = kwargs['title']
            cursor.execute('''UPDATE Books SET Title = ? WHERE BookID = ?''', (new_title, book_id))
        elif 'author' in kwargs:
            new_author = kwargs['author']
            cursor.execute('''UPDATE Books SET Author = ? WHERE BookID = ?''', (new_author, book_id))
        else:
            new_isbn = kwargs['isbn']
            cursor.execute('''UPDATE Books SET ISBN = ? WHERE BookID = ?''', (new_isbn, book_id))
        self.conn.commit()
        print("Book details updated successfully.")

    def delete_book(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM Books WHERE BookID = ?''', (book_id,))
        cursor.execute('''DELETE FROM Reservations WHERE BookID = ?''', (book_id,))
        self.conn.commit()
        print("Book deleted successfully.")

    def close_connection(self):
        self.conn.close()


def main():
    library_system = LibraryManagementSystem()

    while True:
        print("\n### Library Management System ###")
        print("1. Add a new book to the database.")
        print("2. Find a book's detail based on BookID.")
        print("3. Find a book's reservation status.")
        print("4. Find all books in the database.")
        print("5. Modify/update book details based on BookID.")
        print("6. Delete a book based on BookID.")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            book_id = input("Enter BookID: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            isbn = input("Enter ISBN: ")
            status = input("Enter Status: ")
            library_system.add_book(book_id, title, author, isbn, status)
        elif choice == '2':
            book_id = input("Enter BookID: ")
            library_system.find_book_detail(book_id)
        elif choice == '3':
            query = input("Enter BookID, Title, UserID, or ReservationID: ")
            library_system.find_reservation_status(query)
        elif choice == '4':
            library_system.find_all_books()
        elif choice == '5':
            book_id = input("Enter BookID: ")
            if not library_system.search_book(book_id):
                print("Please enter a valid BookID.")
                continue
            print("What details would you like to modify?")
            print("1. Title")
            print("2. Author")
            print("3. ISBN")
            print("4. Status")
            sub_choice = input("Enter your choice: ")
            if sub_choice == '1':
                new_title = input("Enter new Title: ")
                library_system.update_book_details(book_id, title=new_title)
            elif sub_choice == '2':
                new_author = input("Enter new Author: ")
                library_system.update_book_details(book_id, author=new_author)
            elif sub_choice == '3':
                new_isbn = input("Enter new ISBN: ")
                library_system.update_book_details(book_id, isbn=new_isbn)
            elif sub_choice == '4':
                new_status = input("Enter new Status: ")
                library_system.update_book_details(book_id, status=new_status)
            else:
                print("Invalid choice.")
        elif choice == '6':
            book_id = input("Enter BookID: ")
            library_system.delete_book(book_id)
        elif choice == '7':
            library_system.close_connection()
            print("Good bye and have a nice day!")
            break
        else:
            print("PLEASE RE-ENTER A VALID VALUE!.")


if __name__ == '__main__':
    main()
