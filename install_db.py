from database import *

# SQLite prend en charge plusieurs types de données pour stocker différentes valeurs dans une base de données. Voici quelques-uns des types de données couramment utilisés dans SQLite :
# 
# 'TEXT' : Ce type de données est utilisé pour stocker des chaînes de caractères. Par exemple, vous pouvez utiliser le type TEXT pour stocker des noms d'utilisateurs, des descriptions ou des adresses e-mail.
# 
# 'INTEGER' : Ce type de données est utilisé pour stocker des nombres entiers. Il peut être utilisé pour stocker des identifiants, des âges, des quantités, etc.
# 
# 'REAL' : Ce type de données est utilisé pour stocker des nombres à virgule flottante. Il peut être utilisé pour stocker des valeurs décimales, telles que des prix, des coordonnées géographiques, etc.
# 
# 'BLOB' : Ce type de données est utilisé pour stocker des données binaires, telles que des images, des fichiers audio ou vidéo, des documents, etc. Les données binaires sont stockées sous forme de séquence d'octets.
# 
# 'NULL' : Ce type de données est utilisé pour représenter une valeur nulle ou absente. Il peut être utilisé lorsque vous ne souhaitez pas attribuer de valeur à une colonne spécifique.
# 
# Lors de la création d'une table dans SQLite, vous pouvez spécifier le type de données approprié pour chaque colonne. Par exemple vous pouvez utilisez le type TEXT pour les colonnes 'username', 'password' et 'email'.

create_table(FOLDER+'database.sqlite3',
'user',
{
    'username': 'TEXT',
    'password': 'TEXT'
})

add_column_to_table(FOLDER+'database.sqlite3',
    'user',
    'email',
    'TEXT')

create_table(FOLDER+'database.sqlite3',
'article',
{
    'user_id': 'INTEGER',
    'article': 'TEXT'
})

create_class(FOLDER+'database.sqlite3')