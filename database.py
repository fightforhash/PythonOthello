# Import the mysql.connector module
import mysql.connector

# Define a class that represents the database connection and operations
class Database:

    # Define the constructor that takes the host, user, password, and database name as parameters
    def __init__(self, host, user, password, database):
        # Create a connection object with the required parameters
        self.connection = mysql.connector.connect(
            host=host, # The name of the host where the server is running
            user=user, # The user name of the account with access to the schema
            password=password, # The password of the account
            database=database # The name of the schema
            
        )
        # Create a cursor object to execute queries
        self.cursor = self.connection.cursor()
        self.logged_in_user_id = None

    # Define a method that fetches data from the users table
    def get_all_users(self):
        # Define the query string
        query = "select * from users"
        # Execute the query and fetch the results
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        # Return the results as a list of tuples
        return results

    def insert_new_user(self, user, password, email):
        #Define the query string
        query = "insert into users (Username, Pass, Email) VALUES (%s, %s, %s)"
        values = (user, password, email)
        self.cursor.execute(query, values)
        self.connection.commit()

    def get_all_stats(self):
        query = "select * from user_stats"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results
    
    def select_user_stats(self, user_id):
        if user_id is None:
            # Handle the case where no user is logged in
            print("No user is logged in.")
            return None
        #Define the query string
        query = f"select * from user_stats where Player_id = {user_id}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results
    
    def update_user_stats(self, user_id, wins, losses, total, outcome):
        query = "update user_stats "
      #  curr_row = select_user_stats(user_id)
        if (outcome == "win"):
            query = query + f"Set total_wins = {wins}"
        else:
            query = query + f"Set total_losses = {losses}"
        query = query + f", total_games_played = {total}, win_percentage = {round((wins / total), 4)} WHERE Player_id = {user_id}"
        self.cursor.execute(query)
        self.connection.commit()
        
    def validate_user(self, username, password):
        try:
            query = "SELECT User_id FROM users WHERE Username = %s AND Pass = %s"
            values = (username, password)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                self.logged_in_user_id = result[0]  # Store only the user ID
                return True  # Login successful
            else:
                return False  # Login failed
        except mysql.connector.Error as err:
            print("Error occurred: ", err)
            return False
        

    def get_logged_in_user_id(self):
        return self.logged_in_user_id

    # Define a method that closes the cursor and the connection
    def close(self):
        # Close the cursor object
        self.cursor.close()
        # Close the connection object
        self.connection.close()
    


# Define the parameters for connecting to the database
host = "localhost"
user = "root"
password = "selleryH@11"
database = "othellogame"

# Create an instance of the Database class with the parameters
db = Database(host, user, password, database)

# Call the select_user_stats method and print the results
users = db.select_user_stats("9")
print(users[0])
print(users[0][0])
print(users[0][1])
print(users[0][4])

i = 0
wins = 2
losses = 0
games = 3
db.update_user_stats("9", wins, losses, games, "win")



# Call the close method to close the cursor and the connection
db.close()
