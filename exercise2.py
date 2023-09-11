import sqlite3


def main():
    global cursor, conn
    with open("stephen_king_adaptations.txt", "r") as file:
        stephen_king_adaptations_list = file.readlines()

    print(stephen_king_adaptations_list)

    try:
        conn = sqlite3.connect("stephen_king_adaptations.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE if not exists stephen_kind_adaptations_table (  
                movieID TEXT NOT NULL,  
                movieName TEXT NOT NULL,  
                movieYear INTEGER NOT NULL,  
                imdbRating REAL NOT NULL  
                )  
            """)

        for list in stephen_king_adaptations_list:
            data = list.strip().split(",")
            cursor.execute("""  
                INSERT INTO stephen_kind_adaptations_table (movieID, movieName, movieYear, imdbRating)  
                VALUES (?, ?, ?, ?)  
            """, (data[0], data[1], int(data[2]), float(data[3])))
        conn.commit()
    except sqlite3.Error as error:
        print("Something doesn't do well", error)

    while True:
        option = input("Please enter a number between 1 and 4\n")
        if option == "1":
            search_movie(cursor)
        elif option == "2":
            search_by_year(cursor)
        elif option == "3":
            search_by_rating(cursor)
        elif option == "4":
            print("Good bye")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 4.")
    cursor.close()
    conn.close()


def search_movie(cursor):
    movie_name = input("Enter the name of the movie to search: ")
    query = f"SELECT * FROM stephen_kind_adaptations_table WHERE movieName = ?"
    cursor.execute(query, (movie_name,))
    result = cursor.fetchall()
    if result:
        print("Movie details:")
        for row in result:
            print(f"ID: {row[0]}, Name: {row[1]}, Year: {row[2]}, IMDB Rating: {row[3]}")
    else:
        print("No such movie exists in our database.")


def search_by_year(cursor):
    year = input("Enter the year to search: ")
    query = f"SELECT * FROM stephen_kind_adaptations_table WHERE movieYear = ?"
    cursor.execute(query, (year,))
    result = cursor.fetchall()
    if result:
        print("Movies released in the year:", year)
        for row in result:
            print(f"ID: {row[0]}, Name: {row[1]}, Year: {row[2]}, IMDB Rating: {row[3]}")
    else:
        print("No movies were found for that year in our database.")


def search_by_rating(cursor):
    rating = input("Enter the minimum IMDB rating: ")
    query = f"SELECT * FROM stephen_kind_adaptations_table WHERE imdbRating >= ?"
    cursor.execute(query, (rating,))
    result = cursor.fetchall()
    if result:
        print("Movies with IMDB rating or above:", rating)
        for row in result:
            print(f"ID: {row[0]}, Name: {row[1]}, Year: {row[2]}, IMDB Rating: {row[3]}")
    else:
        print("No movies at or above that rating were found in the database.")


if __name__ == "__main__":
    main()
