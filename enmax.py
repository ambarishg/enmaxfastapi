import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import re
import string
from sentence_transformers import SentenceTransformer

#key = st.secrets["OPENAI_KEY"]
key = "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"
filename_pickle ="ENMAX_ESG_FULL.pkl"

import os
import openai
openai.api_key = key

def create_prompt(context,query):
    header = "Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text and requires some latest information to be updated, print 'Sorry Not Sufficient context to answer query' \n"
    return header + context + "\n\n" + query + "\n"

def generate_answer(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=0,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop = [' END']
    )
    return (response.choices[0].text).strip()

def clean_text(text):
    '''Make text lowercase,remove punctuation
    .'''
    text = str(text).lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    return text

if (filename_pickle != ""):
    with open(filename_pickle, 'rb') as f:
        df_embeddings = pickle.load(f)

def get_model():
    model = SentenceTransformer('paraphrase-mpnet-base-v2')
    return model

def get_encodings():
    pole_data = df_embeddings["embeddings"].tolist()
    Lines = df_embeddings["text"].tolist()
    return pole_data,Lines

def get_answer(user_input):
    pole_data ,Lines = get_encodings()
    q_new = user_input
    q_new = [get_model().encode(q_new)]
    result = cosine_similarity(q_new,pole_data)
    result_df = pd.DataFrame(result[0], columns = ['sim'])
    df = pd.DataFrame(Lines,columns = ["text"])
    q = pd.concat([df,result_df],axis = 1)
    q = q.sort_values(by="sim",ascending = False)

    q_n = q[:5]
    q_n = q_n[["text"]]
    context= "\n\n".join(q_n["text"])
    
    prompt = create_prompt(context,user_input)
    reply = generate_answer(prompt)
    return(reply)
    

