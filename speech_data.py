# TODO! see https://github.com/pannous/caffe-speech-recognition for some data sources

import os
import re
import sys
import wave

import numpy
import numpy as np
import librosa
import matplotlib
import scipy.io as sio

from random import shuffle

path = "data/spoken_numbers_mat/" # 8 bit

def dense_to_one_hot(labels_dense, num_classes=10):
  """Convert class labels from scalars to one-hot vectors."""
  return numpy.eye(num_classes)[labels_dense]

def mfcc_batch_generator(batch_size=10, height=120):
  batch_features = []
  labels = []
  files = os.listdir(path)
  while True:
    print("loaded batch of %d files" % len(files))
    shuffle(files)
    for wav in files:
      if not wav.endswith(".mat"): continue
      #wave, sr = librosa.load(path+wav, sr=8000,mono=True)
      label=dense_to_one_hot(int(wav[0]),10)
      labels.append(label)
      
      mfcc_old = sio.loadmat(path+wav)
      mfcc_old = mfcc_old['MFCC_pro']      

      #mfcc_old = librosa.feature.mfcc(wave, sr, n_mfcc=13)
      #delta_mfcc = librosa.feature.delta(mfcc_old, order=1)
      #delta_delta_mfcc = librosa.feature.delta(mfcc_old, order=2)

      #mfcc = numpy.hstack((mfcc_old, delta_mfcc, delta_delta_mfcc))
      #mfcc = numpy.concatenate((mfcc_old, delta_mfcc),axis=0)
      mfcc = mfcc_old      

      #mfcc = mfcc.astype(int)
      #print(np.array(mfcc).shape)

      mfcc=np.pad(mfcc,((0,0),(0,height-len(mfcc[0]))), mode='constant', constant_values=0)
      batch_features.append(np.array(mfcc))

      if len(batch_features) >= batch_size:
        # print(np.array(batch_features).shape)
        # yield np.array(batch_features), labels
        #print(str(mfcc_old)+'\r'+str(delta_mfcc)+'\r'+str(delta_delta_mfcc)+'\r'+str(len(mfcc)))
        yield batch_features, labels  # basic_rnn_seq2seq inputs must be a sequence
        batch_features = []  # Reset for next batch
        labels = []

