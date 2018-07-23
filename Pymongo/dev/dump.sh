#!/bin/bash
MONGODUMP_PATH="/opt/mongodb/bin/mongodump"
MONGO_HOST="10.0.0.60"
MONGO_PORT="27019"
BACKUP_DIR="/data/db_archive/"
MONGO_DATABASE="mondra_log"
#COLLECTION_PATTERN="MatchReport"

declare -a COLLECTION_PATTERN_ARRAY=(\
    "BattleUserReport"\
    "BattleReport"\
    "DeckReport"\
    "GachaReport"\
    "GachaUserUnique"\
    "MatchReport"\
    )
arraylength=${#COLLECTION_PATTERN_ARRAY[@]}


for (( i=1; i<${arraylength}+1; i++ ));
do
COLLECTION_PATTERN=${COLLECTION_PATTERN_ARRAY[$i-1]}

for DAY in {11..31}; do
MONGO_COLLECTION=$COLLECTION_PATTERN"_"$DAY"_12_2015"
$MONGODUMP_PATH --host $MONGO_HOST --port $MONGO_PORT --out=$BACKUP_DIR --db $MONGO_DATABASE --collection $MONGO_COLLECTION
done


for MONTH in 0{1..9} {10..12}; do 
for DAY in 0{1..9} {10..31}; do
MONGO_COLLECTION=$COLLECTION_PATTERN"_"$DAY"_"$MONTH"_2016"
$MONGODUMP_PATH --host $MONGO_HOST --port $MONGO_PORT --out=$BACKUP_DIR --db $MONGO_DATABASE --collection $MONGO_COLLECTION
done
done

for MONTH in 0{1..9} {10..12}; do
for DAY in 0{1..9} {10..31}; do
MONGO_COLLECTION=$COLLECTION_PATTERN"_"$DAY"_"$MONTH"_2017"
$MONGODUMP_PATH --host $MONGO_HOST --port $MONGO_PORT --out=$BACKUP_DIR --db $MONGO_DATABASE --collection $MONGO_COLLECTION
done
done

for MONTH in 0{1..3}; do
for DAY in 0{1..9} {10..31}; do
MONGO_COLLECTION=$COLLECTION_PATTERN"_"$DAY"_"$MONTH"_2018"
$MONGODUMP_PATH --host $MONGO_HOST --port $MONGO_PORT --out=$BACKUP_DIR --db $MONGO_DATABASE --collection $MONGO_COLLECTION
done
done



cd /data/db_archive/mondra_log/
mkdir $COLLECTION_PATTERN
mv $COLLECTION_PATTERN"_"* $COLLECTION_PATTERN



cd "/data/db_archive/mondra_log/"$COLLECTION_PATTERN
find . -name "*.bson" -size 0 -print0 | xargs -0 rm
find . -name "*.metadata.json" -size 0 -print0 | xargs -0 rm

for YEAR in 2015; do
for MONTH in 12; do
tar -cvzf $COLLECTION_PATTERN"_xx_"$MONTH"_"$YEAR".tar.gz" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
rm -f "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
done
done

for YEAR in {2016..2017}; do
for MONTH in 0{1..9} {10..12}; do
tar -cvzf $COLLECTION_PATTERN"_xx_"$MONTH"_"$YEAR".tar.gz" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
rm -f "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
done
done

for YEAR in 2018; do
for MONTH in 0{1..3}; do
tar -cvzf $COLLECTION_PATTERN"_xx_"$MONTH"_"$YEAR".tar.gz" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
rm -f "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
done
done


done


cd /data/db_archive/mondra_log/
mkdir $COLLECTION_PATTERN
mv $COLLECTION_PATTERN"_"* $COLLECTION_PATTERN



cd "/data/db_archive/mondra_log/"$COLLECTION_PATTERN
find . -name "*.bson" -size 0 -print0 | xargs -0 rm
find . -name "*.metadata.json" -size 0 -print0 | xargs -0 rm

for YEAR in 2015; do
for MONTH in 12; do
tar -cvzf $COLLECTION_PATTERN"_xx_"$MONTH"_"$YEAR".tar.gz" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
rm -f "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
done
done

for YEAR in 2016; do
for MONTH in 0{1..9} {10..12}; do
tar -cvzf $COLLECTION_PATTERN"_xx_"$MONTH"_"$YEAR".tar.gz" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
rm -f "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
done
done

for YEAR in 2017; do
for MONTH in 0{1..9}; do
tar -cvzf $COLLECTION_PATTERN"_xx_"$MONTH"_"$YEAR".tar.gz" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
rm -f "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".bson" "./"$COLLECTION_PATTERN"_"*"_"$MONTH"_"$YEAR".metadata.json"
done
done
