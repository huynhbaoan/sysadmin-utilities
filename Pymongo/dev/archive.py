import tarfile, gzip
import sys, os, glob, shutil


DIR = '/home/huynhbaoan/PythonProject/Pymongo/dev/'
BACKUP_PATTERN = 'GameRewardLog'



for file in glob.glob(DIR + BACKUP_PATTERN):

FULLPATH = os.path.join(DIR + BACKUP_PATTERN, BACKUP_PATTERN + "_" + str(DAY) + \
                   "_" + str(MONTH) + "_" + str(YEAR))
print('creating archive')
try:
    with tarfile.TarFile.gzopen(os.path.join(DIR, 'sampledir'+'.tar.gz'), mode='w', compresslevel=9) as targz:
        for file in glob.glob(FULLPATH + "*.bson"):
            print('Adding file: ', file)
            try:
                targz.add(file)
            except:
                print("Error adding file ", file, "Error: ", sys.exc_info())
except:
    print("Unexpected error:", sys.exc_info())
    raise


print
print('Contents:')
t = tarfile.open('sampledir.tar.gz', 'r')
for member_info in t.getmembers():
    print(member_info.name)



# def restore_docs(DIR, BACKUP_PATTERN, DAY, MONTH, YEAR, collection, BEGIN_PART_NUM):
    
#     FULLPATH = os.path.join(DIR + BACKUP_PATTERN, BACKUP_PATTERN + "_" + str(DAY) + \
#                 "_" + str(MONTH) + "_" + str(YEAR))
#     print ("Restoring ",BACKUP_PATTERN,DAY,MONTH,YEAR)
#     for file in glob.glob(FULLPATH + "*.bson"):
#         print ("Restoring from ",file)    
#         with open(file, 'rb') as f:
            