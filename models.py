'''File generated by RapidSQL v1.0. GitHub: https://github.com/OMT26/RapidSQL'''
from database import *

DATABASE = 'c:/Users/poiss/Desktop/Dev TEST/RapidSQL/database.sqlite3'

class User:
    """
    Class for accessing data from table "user".
    """
    def __init__(self, useranme:str, password:str, email:str, id:int = 0) -> None:
        """
        Initialize a new instance of the Model class.

        Args:
        useranme (str)
        password (str)
        email (str)
        id (int, optional): Defaults to 0.
        """
        self.id = id
        self.useranme = useranme
        self.password = password
        self.email = email
        
        self.article = []

    def insert(self, db:str = DATABASE) -> None:
        """
        Inserts the User object into the specified database.
        Only works if the self.id is not 0.

        Args:
            db (str): The name of the database to insert the participant into.

        Returns:
            None
        """
        if self.id == 0:
            withou_id = self.__dict__.copy()
            del withou_id['id'];del withou_id['article']
            self.id = insert_data(db, "user", withou_id)
    
    def update(self, db:str = DATABASE) -> None:
        """
        Updates the User object in the database.

        Args:
            db (str): The name of the database to update the object in.

        Returns:
            None
        """
        if self.id != 0:
            withou_id = self.__dict__.copy()
            del withou_id['id'];del withou_id['article']
            update_data(db, "user", withou_id, f"id = {self.id}")
    
    def delete(self, db:str = DATABASE) -> None:
        """
        Deletes the User object from the specified database.

        Args:
            db (str): The name of the database to delete the object from.

        Returns:
            None
        """
        delete_data(db, "user", f"id = {self.id}")
    
    def get_article(self, db:str = DATABASE) -> None:
        """
        Retrieves the Article associated with the current User from the database.

        Args:
            db (str): The name of the database to query. Defaults to the value of the DATABASE constant.

        Returns:
            None
        """
        self.article = get_article(db, f"user_id = {self.id}")
                
class Article:
    """
    Class for accessing data from table "article".
    """
    def __init__(self, user_id:int, article:str, id:int = 0) -> None:
        """
        Initialize a new instance of the Model class.

        Args:
        user_id (int)
        article (str)
        id (int, optional): Defaults to 0.
        """
        self.id = id
        self.user_id = user_id
        self.article = article
        
        self.user = None

    def insert(self, db:str = DATABASE) -> None:
        """
        Inserts the Article object into the specified database.
        Only works if the self.id is not 0.

        Args:
            db (str): The name of the database to insert the participant into.

        Returns:
            None
        """
        if self.id == 0:
            withou_id = self.__dict__.copy()
            del withou_id['id'];del withou_id['user']
            self.id = insert_data(db, "article", withou_id)
    
    def update(self, db:str = DATABASE) -> None:
        """
        Updates the Article object in the database.

        Args:
            db (str): The name of the database to update the object in.

        Returns:
            None
        """
        if self.id != 0:
            withou_id = self.__dict__.copy()
            del withou_id['id'];del withou_id['user']
            update_data(db, "article", withou_id, f"id = {self.id}")
    
    def delete(self, db:str = DATABASE) -> None:
        """
        Deletes the Article object from the specified database.

        Args:
            db (str): The name of the database to delete the object from.

        Returns:
            None
        """
        delete_data(db, "article", f"id = {self.id}")
    
    def get_user(self, db:str = DATABASE) -> None:
        """
        Retrieves the User from the database based on the user_id in the current Article object.

        Args:
            db (str): The name of the database to query. Defaults to DATABASE.

        Returns:
            None
        """
        self.user =  get_user(db, f"id = {self.user_id}", first=True)
                
def get_user(db:str = DATABASE, condition:str = "", first:bool = False, count:bool = False) -> Union[list, User, int, None]:
    """
    Args:
        db (string, optional): Database path. Defaults to DATABASE.
        condition (string, optional): Condition for query. Defaults to None.
        first (bool, optional): If true return only the first result. Defaults to False.
        count (bool, optional): If true return integer of result. Defaults to False.
    
    Return:
        Union[list, User, int, None]: 
            - If first is True, returns a single User object or None if no result is found.
            - If count is True, returns the integer count of results.
            - Otherwise, returns a list of User objects.
    """
    data_list = get_data(db, "user", condition)
    if first:
        return User(id = data_list[0][0],useranme = data_list[0][1],password = data_list[0][2],email = data_list[0][3]) if len(data_list) != 0 else None
    if count:
        return len(data_list)
    return [User(id = l[0],useranme = l[1],password = l[2],email = l[3]) for l in data_list]
        
def get_article(db:str = DATABASE, condition:str = "", first:bool = False, count:bool = False) -> Union[list, Article, int, None]:
    """
    Args:
        db (string, optional): Database path. Defaults to DATABASE.
        condition (string, optional): Condition for query. Defaults to None.
        first (bool, optional): If true return only the first result. Defaults to False.
        count (bool, optional): If true return integer of result. Defaults to False.
    
    Return:
        Union[list, Article, int, None]: 
            - If first is True, returns a single Article object or None if no result is found.
            - If count is True, returns the integer count of results.
            - Otherwise, returns a list of Article objects.
    """
    data_list = get_data(db, "article", condition)
    if first:
        return Article(id = data_list[0][0],user_id = data_list[0][1],article = data_list[0][2]) if len(data_list) != 0 else None
    if count:
        return len(data_list)
    return [Article(id = l[0],user_id = l[1],article = l[2]) for l in data_list]
        