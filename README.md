# NYC Taxi Data Pipeline

Projet de data engineering autour des données **NYC TLC Yellow Taxi**.

* télécharger les données mensuelles en **Parquet**
* effectuer une première validation avec **DuckDB**
* charger les fichiers dans **Snowflake**
* conserver les données brutes dans une couche **RAW**
* nettoyer et typer les données avec **dbt**
* produire des données agrégées dans une couche **FINAL**
* automatiser les ingestions mensuelles avec **GitHub Actions**

## Architecture

```text
NYC TLC
   ↓
Python
   ↓
Parquet
   ↓
DuckDB
   ↓
Snowflake RAW
   ↓
dbt STAGING
   ↓
dbt FINAL
```

Le projet sert surtout à mettre en pratique un pipeline **data engineering complet**, de l'ingestion jusqu'à la transformation et l'automatisation.


## Ingestion

**src/ingestion**

Ce dossier contient trois fichiers:
- ingestion.py
- ingest_historical.py
- ingest_monthly.py

Le fichier **ingest_monthly.py** est *'fictif'* dans le sens où les data ne semblent pas être misent à jour en temps réel sur le site source.

**ingestion.py** Contient la logique de base de l'ingestion sous forme de Class Python en ctx manager. Cette Class permet de télécharger les fichiers, les ingérer en DuckDB puis supprimer l'historique dans *data/*.

**ingest_historical.py** Lance l'ingestion depuis 2026-01 jusqu'au dernier mois disponible (à ce jour, 2026-06). Il faut donc un certain temps pour que l'ingestion se termine puisqu'on parle de plus de 78M de rows.

## Lancer le projet:

Environnement virtuel:

```bash
~/.pyenv/versions/"$version"/bin/python -m venv env
source env/bin/activate
```

Lancer l'ingestion:
```bash
pip install -e .
python -m src.ingestion.ingest_historical
```

Lancer dbt:
```bash
cd dbt/nyc_taxi
dbt debug
dbt run
dbt test
```

## Github Actions

Le projet est entièrement orchestré avec Github Actions, on peut trouver les fichiers d'orchestration des jobs dans .**github/workflows**