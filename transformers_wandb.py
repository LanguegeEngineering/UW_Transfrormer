# -*- coding: utf-8 -*-
"""Transformers_wandb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U9PifkkKBfXsRkBooRoRoZAgIvS-xQpp
"""

!pip install simpletransformers

!pip install wandb -qqq
import wandb
import pandas as pd
wandb.login()

!wget https://s3.amazonaws.com/fast-ai-nlp/ag_news_csv.tgz

!tar -xf ag_news_csv.tgz
!mv ag_news_csv data

!head -15000 data/train.csv > data/small_train.csv
!tail -1500 data/train.csv >  data/small_test.csv 
!head -1500 data/test.csv > data/small_eval.csv

def preprocess_file(filename):
  df = pd.read_csv(filename, header=None)
  df['text'] = df.iloc[:, 1] + " " + df.iloc[:, 2]
  df = df.drop(df.columns[[1, 2]], axis=1)
  df.columns = ['labels', 'text']
  df = df[['text', 'labels']]
  df['text'] = df['text'].apply(lambda x: x.replace('\\', ' '))
  df['labels'] = df['labels'].apply(lambda x:x-1)
  return df

train_df = preprocess_file("data/small_train.csv")
eval_df = preprocess_file("data/small_eval.csv")
test_df = preprocess_file("data/small_test.csv")

train_df.head()

from simpletransformers.classification import ClassificationModel


# Training arguments
train_args = {
    'evaluate_during_training': True,
    'num_train_epochs': 5,
    'save_eval_checkpoints': False,
    'train_batch_size': 32,
    'eval_batch_size': 32,
    'overwrite_output_dir': True,
    'wandb_project': "distilbert_training",
}

# Create a ClassificationModel
model = ClassificationModel('distilbert', 'distilbert-base-uncased', num_labels=4, use_cuda=True, cuda_device=0, args=train_args)

# Train model
model.train_model(train_df, eval_df=eval_df)
result, model_outputs, wrong_predictions = model.eval_model(test_df)

"""### Zadania

1. Sprawdzić jaki jest czas, kiedy nie korzystamy z CUDY
2. Sprobować rożnych parametrow i poprawić wyniki
3. Sprawdzić inne modele do multi-class classification ze strony: https://simpletransformers.ai/docs/classification-specifics/
"""

