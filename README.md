# Application de Raccourcissement d'URL avec FastAPI

Cette application web permet de raccourcir des URLs longues en URLs plus courtes, similaires à des services comme Bitly ou TinyURL. L'application est développée en utilisant FastAPI et utilise une base de données SQLite pour stocker les mappings URL raccourcies.

## Fonctionnalités

- **Raccourcissement d'URLs :** Permet aux utilisateurs de soumettre une URL longue et de recevoir en retour une URL raccourcie unique.
- **Redirection :** Les URLs raccourcies redirigent les utilisateurs vers l'URL d'origine.
- **Personnalisation :** L'utilisateur peut définir un slug personalisés pour ses URLs 

## Installation

1. **Clonage du dépôt :**

   ```bash
   git clone https://github.com/GuillaumeQ11/url_shortener_project.git
   cd url_shortener_project
   ```

2. **Installation des dépendances :**

   Assurez-vous que Python 3.7+ est installé. Créez un environnement virtuel et activez-le :

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows, utilisez .venv\Scripts\activate
   ```

   Installez les dépendances avec pip :

   ```bash
   pip install -r requirements.txt
   ```

3. **Lancement de l'application :**

   Démarrez l'application FastAPI :

   ```bash
   uvicorn main:app --reload
   ```

   L'application sera accessible à l'adresse par défaut : [http://localhost:8000](http://localhost:8000).

## Utilisation

1. Accédez à l'interface web à [http://localhost:8000](http://localhost:8000).

2. Entrez une URL longue dans le champ dédié et soumettez le formulaire.

3. (Optionnel) Vous pouvez entrer un slug personnalisé dans le champ dédié.

4. Vous recevrez une URL raccourcie qui redirige vers l'URL d'origine.


## Auteur

GuillaumeQ11 - [GitHub](https://github.com/GuillaumeQ11)
