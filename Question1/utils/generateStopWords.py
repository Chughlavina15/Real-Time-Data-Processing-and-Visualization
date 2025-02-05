import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

stop_words = stopwords.words('english')

formatted_stop_words = ', '.join([f'"{word}"' for word in stop_words])

with open("./utils/stopwords_list.conf", "w") as f:
    f.write(f'if [entity] in [{formatted_stop_words}] {{ drop {{}} }}')
