# RapidSQL

RapidSQL est une bibliothèque Python conçue pour simplifier les interactions avec les bases de données SQLite. Elle offre une interface orientée objet pour effectuer des opérations de création, de lecture, de mise à jour et de suppression de données. Le projet intègre également des fonctionnalités avancées telles que la gestion des barres de progression lors d'insertions massives de données et la génération automatique de classes modèles Python adaptées à la structure de la base de données.

## Fonctionnalités Clés

- **Interface Pythonique pour SQLite** : Facilite les opérations CRUD avec une approche orientée objet.
- **Génération Automatique de Modèles** : Produit des classes Python correspondant aux tables de la base de données, simplifiant l'accès et la manipulation des données.
- **Support des Relations entre Tables** : Génère automatiquement des méthodes et des attributs pour gérer les relations entre tables, telles que les relations un-à-plusieurs.

## Gestion Automatique des Identifiants

Dans RapidSQL, chaque table que vous créez bénéficie automatiquement d'une colonne d'identifiant (`id`) en auto-incrémentation. Cela signifie que vous n'avez pas besoin de spécifier explicitement une colonne `id` lors de la création de vos tables : RapidSQL s'en charge pour vous, garantissant ainsi que chaque enregistrement est unique et facilement identifiable.

### Exemple de Création de Table

```python
create_table('database.sqlite3', 'user', {
    'username': 'TEXT',
    'password': 'TEXT'
})
create_table('database.sqlite3', 'article', {
    'titre': 'TEXT',
    'contenu': 'TEXT',
    'user_id': 'INTEGER'
})
```

Dans cet exemple, la table 'user' contiendra les colonnes 'username' et 'password', toutes deux de type 'TEXT'. Un identifiant unique (id) en auto-incrémentation est automatiquement ajouté à cette table, bien que cela ne soit pas explicitement spécifié dans l'appel de fonction.
La table 'article' inclura les colonnes 'titre' et 'contenu', de type 'TEXT',ainsi qu'une colonne 'user_id' de type 'INTEGER'. Cette dernière colonne est destinée à stocker des clés étrangères référençant la table 'user', permettant ainsi de lier chaque article à un utilisateur spécifique. Comme pour la table 'user', un identifiant unique (id) en auto-incrémentation est automatiquement ajouté.

## Exemples d'utilisation

### Créer un nouvel utilisateur

```python
from models import User

new_user = User(username="exemple", password="123456", email="exemple@mail.com")
new_user.insert()
```

### Obtenir des informations sur un utilisateur

```python
user = get_user(condition="username='exemple'", first=True)
if user:
    print(user.username, user.email)
```

### Mettre à jour un utilisateur

```python
user = get_user(condition="username='exemple'", first=True)
user.password = "nouveauMotDePasse"
user.update()
```

### Supprimer un utilisateur

```pyhton
user = get_user(condition="username='exemple'", first=True)
user.delete()
```

## Relations entre Tables et Chargement Dynamique

RapidSQL facilite la gestion des relations entre vos tables. Lorsqu'une table comporte une colonne clé étrangère, par exemple user_id dans une table article, des méthodes et des attributs sont automatiquement générés pour accéder facilement aux données relationnelles.

Accéder aux Relations : Pour un utilisateur, accéder à ses articles se fait via la méthode `get_article()` qui charge la liste des articles dans l'attribut article de l'instance User.

Chargement Inverse : De la même manière, un objet Article aura accès à son utilisateur via un attribut user et une méthode `get_user()` correspondante.

### Exemples de Relations

Accès aux Articles d'un Utilisateur : Si une table article contient une colonne user_id, la classe générée `User()` aura un attribut article et une méthode `get_article()`. Cette méthode renvoie une liste de tous les objets Article liés à l'utilisateur, accessibles via self.article.

```python
user = get_user(condition="username='exemple'", first=True)
if user:
    user.get_article()  # Charge tous les articles liés à cet utilisateur dans user.article
    for article in user.article:
        print(article.title)  # Hypothétique attribut 'title' de l'objet Article
```        

Association d'un Article à un Utilisateur : Inversement, un objet `Article()` inclura un attribut user et une méthode `get_user()`, qui charge l'objet User associé dans self.user.

```python
article = get_article(condition="title='Mon Premier Article'", first=True)
if article:
    article.get_user()  # Charge l'utilisateur lié à cet article dans article.user
    print(article.user.username)
```