# NYC Taxi Data Pipeline

Projet de data engineering autour des données **NYC TLC Yellow Taxi**.

* télécharger les données mensuelles en **Parquet**
* effectuer une première validation avec **DuckDB**
* charger les fichiers dans **Snowflake**
* conserver les données brutes dans une couche **RAW**
* nettoyer et typer les données avec **dbt**
* produire des données agrégées dans une couche **FINAL**
* automatiser les ingestions mensuelles avec **GitHub Actions**

### Architecture

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
