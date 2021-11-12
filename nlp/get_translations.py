### The following script can be executed to perform the full translation job
### However, I would be safer to run in parts as laid out before
### as multiple files are used so (drastically) fewer API calls are made


## Part 1 - add id to review data set
import pandas as pd

df = pd.read_csv("./olist_order_reviews_dataset.csv")
# add id to merge after translation are obtained
df['id'] = range(1, len(df) + 1)
# replace new line chars with space
df = df.replace(r'\n',' ', regex=True) 
df.to_csv('olist_order_reviews_dataset_with_id.csv', index=False)


## Part 2 - get translations and throw them into a new file
from google_trans_new import google_translator
import pandas as pd

df = pd.read_csv("./olist_order_reviews_dataset_with_id.csv")
print(df.head(20))
df.dropna(thresh=7, inplace=True)
df = df.replace(r'\n',' ', regex=True) 
print(df.head(20))
translator = google_translator()
for _, row in df.iterrows():
    print(row['id'], row['review_comment_title'], row['review_comment_message'])
    if type(row['review_comment_title']).__name__ != 'float':
        review_comment_title_english = translator.translate(row['review_comment_title'],lang_tgt='en')
    else:
        review_comment_title_english = ''
    if type(row['review_comment_message']).__name__ != 'float':
        review_comment_message_english = translator.translate(row['review_comment_message'],lang_tgt='en') 
    else:
        review_comment_message_english = ''
    file = open("translated.csv", "a")
    file.write(f'{row["id"]},"{review_comment_title_english}","{review_comment_message_english}"\n')


## Part 3 - merge the data set of original reviews with the translated results

import pandas as pd

reviews = pd.read_csv("./olist_order_reviews_dataset_with_id.csv")
translations = pd.read_csv("./translated.csv")
df = pd.merge(reviews, translations, on='id', how='left')
df.drop('id', axis=1, inplace=True)
df.to_csv('olist_order_reviews_dataset_with_translation.csv', index=False)