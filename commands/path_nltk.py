import nltk
import os
print(next(p for p in nltk.data.path if os.path.exists(p)))