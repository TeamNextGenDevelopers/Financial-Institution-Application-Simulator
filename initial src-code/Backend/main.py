from cloud_database import Database

class Bank:
    def __init__(self):
        connection_string = "mongodb+srv://tahshinshahriar:i2NK6Sc0jmCnhjWO@cluster0.nafiayb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        db_name = "financial-data"
        collection_name = "user-info-collection"
        db = Database(connection_string, db_name, collection_name)

    def login(self, email, passwd): 
        if self.db.get_password(email) == passwd:
            return True
        return False

    
        


        
