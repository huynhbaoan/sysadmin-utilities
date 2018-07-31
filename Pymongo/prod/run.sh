#!/bin/bash
## declare an array variable

sudo chown -R bkuser: /data2/log_archived/

declare -a COLL_ARRAY=(\
    "GuildMissionLog:createdAt"\
    "UserDataChange:_modified"\
    "BattleResultLog:createdAt"\
    "BattleResultStartLog:createdAt"
    "UserMonster:_modified"\
    "BattleRewardLog:createdAt"\
    "GameReportActionLog:createdAt"\
    "BattleTraceInfoLog:createdAt"\
    "StrengthenLog:createdAt"\
    "GameRewardLog:createdAt"\
    "GiftBoxLog:createdAt"\
    "MonsterSoldLog:createdAt"\
    "DiamondChangeLog:time"\
    "MedalExchangeLog:createdAt"\
    "UserGift:_created"\
    "LoginActionLog:createdAt"\
    "MissionStatusTraceLog:createdAt"\
    "FriendLog:createdAt"\
    "MissionRewardLog:createdAt"\
    "TutorialLog:createdAt"\
    "BuyGachaCoinLog:createdAt"\
    "LearnSkillLog:createdAt"\
    "PvPBattleResultStartLog:createdAt"\
    "ArenaBattleResultLog:createdAt"\
    "QuestTicketHistoryLog:createdAt"\
    "ArenaBattleResultStartLog:createdAt"\
    "LoginBonusStampActionLog:createdAt"\
    "LoginBonusActionLog:createdAt"\
    "PvPBattleResultLog:createdAt"\
    "LastActionLog:createdAt"\
    "CountUserClickLog:createdAt"\
    "FriendGachaLog:createdAt"\
    "HeroChallengeScoreResultActionLog:createdAt"\
    "PassBonusLog:createdAt"\
    "FreeGachaLog:createdAt"\
    "ArenaTrainingBattleResultLog:createdAt"\
    "EvolutionMonsterLog:createdAt"\
    "TicketConsumeLog:createdAt"\
    "ArenaTrainingBattleResultStartLog:createdAt"\
    "RegisterActionLog:createdAt"\
    "HeroChallengeBattleResultLog:createdAt"\
    "OneTimeShopLog:createdAt"\
    "HeroChallengeBattleResultStartLog:createdAt"\
    "ChallengeMissionActionLog:createdAt"\
    "ArenaMatchingActionLog:createdAt"\
    "RestoreStaminaLog:createdAt"\
    "SpecialRewardLog:createdAt"\
    "UserPreference:_modified"\
    "SkillJewelUsedLog:createdAt"\
    "SkillJewelSoldLog:createdAt"\
    )

declare -a COLL_ARRAY2=(\
    "LoginDetailLog:createdAt"\
    "DeviceTutorialLog:_created"\
    "LoginLog:createdAt"\
    "RealTimeBattleLog:update_time"\
    "DeviceFirstMeetMultiLog:_modified"\
    "GuildActionLog:createdAt"\
)
DIR="/data2/log_archived/"
cd $DIR

# get length of an array
arraylength=${#COLL_ARRAY[@]}

# use for loop to read all values and indexes
for (( i=1; i<${arraylength}+1; i++ ));
do
    # Extract PATTERN and call python to do optimize log
    # Cut log with custom ObjectId
    BACKUP_PATTERN=$(echo ${COLL_ARRAY[$i-1]} | cut -d : -f 1)
    INDEX_PATTERN=$(echo ${COLL_ARRAY[$i-1]} | cut -d : -f 2)
    echo "Deleting old log " $i " / " ${arraylength} " : " ${COLL_ARRAY[$i-1]}
    python args-find-delete-document-customid.py $BACKUP_PATTERN $INDEX_PATTERN
    echo "Compressing old log " $i " / " ${arraylength} " : " $BACKUP_PATTERN
    python args-compress-document.py $BACKUP_PATTERN $DIR
done


# get length of an array
arraylength=${#COLL_ARRAY2[@]}

# use for loop to read all values and indexes
for (( i=1; i<${arraylength}+1; i++ ));
do
    # Extract PATTERN and call python to do optimize log
    # Cut log with standard ObjectId
    BACKUP_PATTERN=$(echo ${COLL_ARRAY2[$i-1]} | cut -d : -f 1)
    INDEX_PATTERN=$(echo ${COLL_ARRAY2[$i-1]} | cut -d : -f 2)
    echo "Deleting old log " $i " / " ${arraylength} " : " ${COLL_ARRAY2[$i-1]}
    python args-find-delete-document-stdid.py $BACKUP_PATTERN $INDEX_PATTERN
    echo "Compressing old log " $i " / " ${arraylength} " : " $BACKUP_PATTERN
    python args-compress-document.py $BACKUP_PATTERN $DIR
done

# upload to S3
# find /data2/log_archived/ -name "*.tar*" -mtime -14 -print0 | xargs -0 -t -I % bash -c '/home/gsysadmin/.local/bin/aws s3 cp % s3://bucketname.path --storage-class ONEZONE_IA'