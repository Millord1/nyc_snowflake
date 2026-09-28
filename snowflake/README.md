# Snowflake

Cette partie du projet contient la configuration et la préparation de Snowflake pour recevoir les données NYC TLC Yellow Taxi.

L'architecture retenue est volontairement simple :

```text
Parquet
   ↓
Snowflake Stage
   ↓
RAW
   ↓
STAGING
   ↓
FINAL
```

Les fichiers suivant ont été utilisés directement dans Snowflake, je les ai copié ici pour la documentation...

## Création de l'environnement

Le fichier create_env.sql prépare l'env Snowflake

On crée :
- la base NYC_TAXI
- le schéma RAW
- le warehouse NYC_TAXI_WH

On utilise ensuite la base, le schéma et le warehouse :

```sql
USE DATABASE NYC_TAXI;
USE SCHEMA RAW;
USE WAREHOUSE NYC_TAXI_WH;
```

## Stage et table RAW

Les fichiers Parquet provenant de NYC TLC sont envoyés dans un stage interne Snowflake **NYC_TAXI.RAW.TLC_STAGE**

Définition du format de fichiers comme parquet:

```sql
CREATE FILE FORMAT NYC_TAXI.RAW.PARQUET_FORMAT
    TYPE = PARQUET;
```

Table principale: **NYC_TAXI.RAW.YELLOW_TAXI**

Les fichiers sont chargés:

```sql
COPY INTO NYC_TAXI.RAW.YELLOW_TAXI
FROM @NYC_TAXI.RAW.TLC_STAGE
FILE_FORMAT = (
    FORMAT_NAME = 'NYC_TAXI.RAW.PARQUET_FORMAT'
)
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;
```

MATCH_BY_COLUMN_NAME permet de faire correspondre les colonnes du Parquet avec celles de la table


## Contrôle de qualité des données

Le fichier quantify.sql sert à explorer les anomalies présentes dans les données
On vérifie :

- les distances nulles
- les distances négatives
- les distances supérieures à 1000 miles
- les valeurs minimale et maximale

Certaines valeurs aberrantes ont été trouvées. Elles ne sont pas supprimées en RAW afin de conserver les données sources originales

Même principe pour les montants :

- montants négatifs
- valeurs minimales et maximales
- répartition des montants négatifs selon payment_type

Les valeurs nulles ont également été étudiées.

Notamment, passenger_count et RatecodeID sont souvent tous les deux NULL pour les lignes avec *payment_type = 0*

etc...

## Organisation finale

```text
NYC_TAXI
│
├── RAW
│   ├── TLC_STAGE
│   ├── PARQUET_FORMAT
│   └── YELLOW_TAXI
│
├── STAGING
│   └── STG_YELLOW_TAXI
│
└── FINAL
    └── MART_YELLOW_TAXI_DAILY
```

RAW est geré par le script Python d'ingestion
STAGING et FINAL sont ensuite gérés avec dbt

Le modèle final contient des agrégations journalières :

- nombre de trajets
- chiffre d'affaires total
- tarif moyen
- distance moyenne
- durée moyenne
- pourboires
- péages

Il est bien sûr possible d'ajouter de nombreux marts puisqu'on finit avec 30M de rows en RAW