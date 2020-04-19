
#https://stackoverflow.com/questions/40327859/pyspark-how-to-read-csv-into-dataframe-and-manipulate-it

# load in data
#political_ads = sc.textFile("/usr/data/facebook/fbpac-ads-en-US.csv")   

import pyspark
from csv import reader
import re 
import pandas as pd
import datetime
from datetime import date
sc = pyspark.SparkContext()
sql = SQLContext(sc)

my_df = spark.read.csv("/usr/data/facebook/fbpac-ads-en-US.csv", header = True, inferSchema = True, quote = "\"", escape = "\"")
df1 = my_df.drop('html')
df2 = df1.drop('targetings').drop('targeting').drop('targetedness')
df2.show(1)
                          
rdd = df2.rdd.map(tuple)
rdd.take(2)

def whatis(line):
  return line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19]

whatis = rdd.map(whatis)


#remove hyperfeed_story
#accounts for columns that don't have "hyperfeed" in them
def takeline(line):
    idnum = "hyperfeed_story_id_"
    id = line[0]
    if idnum in line[0]:
            id = line[0].strip(idnum)
    else:
            id = id
    return id, line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19]

takeline = rdd.map(takeline)
takeline.take(3)


#remove html tags and other weird emojis in "message" content
def remove_paragraph_tags(line):
    fixupcontent = line[4]
    clean = re.compile(r'<.*?>')
    fixupcontent1 = re.sub(clean, '', fixupcontent)
    emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F" # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "]+", flags=re.UNICODE)
    fixupcontent = (emoji_pattern.sub(r'', fixupcontent1))
    return line[0], line[1], line[2], line[3], fixupcontent, line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19]


remove_tags = takeline.map(remove_paragraph_tags)
remove_tags.take(1)



#make "created" and "updated" datetime objects
def fix_time(line):
    created_time = line[6]
    strip_create_time = created_time[:10]
    datetime_create = datetime.datetime.strptime(strip_create_time, '%Y-%m-%d')
    update_time = line[7]
    strip_update_time = update_time[:10]
    datetime_update = datetime.datetime.strptime(strip_update_time, '%Y-%m-%d')
    
    return line[0], line[1], line[2], line[3], line[4], line[5], datetime_create, datetime_update, line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19]

fix_time = remove_tags.map(fix_time)
fix_time.take(1)


#taking the brackets out of the image col
def images_column(line):
    image_url = line[9]
    cleanstart = "{"
    cleanend = "}"
    quote = '"'
    if cleanstart or cleanend or quote in image_url:
      image_url = image_url.replace(cleanstart, '')
      image_url = image_url.replace(cleanend, '')
      image_url = image_url.replace(quote, '')
      return line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], image_url, line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17], line[18], line[19]

image_col = fix_time.map(images_column)
image_col.take(1)  


#for target column, replace [] rows with "NA"
def target_col(line):
    target = line[13]
    brack = "[]"
    if target == brack:
            key = target
            key = "NA"
    else:
            key = target
    return line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], key, line[14], line[15], line[16], line[17], line[18], line[19]
          

target = image_col.map(target_col)
target.take(2)              

###########################

result = isinstance(dictline, dict)
 
def key_values(line):
    target = line[13]
    if isinstance(target,dict):
            for k,v in target.items():
                    return k,v
                    return line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], key, line[14, line[15], line[16], line[17], line[18], line[19]       



def key_values(line):
    target = line[13]
    if isinstance(target,dict):
            for k, v in target.items():
                return k, v
            key, values = target.items()
            return key, values
    else:
            return target
        
target = image_col.map(target_col)
target.take(2)    


#################################################################

