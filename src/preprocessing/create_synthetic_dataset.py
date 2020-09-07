from preprocessing.time_series.df_to_dataset_synthetic import split_synthetic_dataset
from preprocessing.time_series.generate_ts_dataset import generate_synthetic_dataset
import argparse
import numpy as np
import os
import tensorflow as tf

if __name__ == "__main__":

  parser = argparse.ArgumentParser()
  parser.add_argument("-data_path", type=str, default="../../../data", help="data folder to save synthetic dataset.")
  parser.add_argument('-model', type=int, default=1, help='choice between model 1 and 2.')
  parser.add_argument('-seq_len', type=int, default=24, help="number of timesteps in the time-series dataset.")
  parser.add_argument('-num_samples', type=int, default=100, help="number of samples in the generated synthetic dataset.")
  parser.add_argument('-num_features', type=int, default=1,
                      help="number of features in the generated synthetic dataset.")
  parser.add_argument("-cv", type=int, default=0, help="split the dataset in Kfold subsets for cross-validation.Default to No.")
  parser.add_argument("-TRAIN_SPLIT", type=float, default=0.7, help="train split for splitting between train and validation sets.")
  parser.add_argument("-VAL_SPLIT", type=float, default=0.5, help="split between validation and test sets.")
  parser.add_argument("-VAL_SPLIT_cv", type=float, default=0.9, help="split between train/val sets and test set when doing cv.")
  args = parser.parse_args()

  std_matrix = tf.sqrt(tf.constant(0.5, shape=(1, 1), dtype=tf.float32))
  A = tf.constant([0.8], shape=(1, 1), dtype=tf.float32)
  X_data = generate_synthetic_dataset(A=A, std_matrix=std_matrix, num_samples=args.num_samples, num_features=args.num_features, model=args.model)

  out_path = os.path.join(args.data_path, "synthetic_model_{}".format(str(args.model)))
  if not os.path.isdir(out_path):
      os.makedirs(out_path)
  out_file = os.path.join(out_path, "synthetic_dataset_{}_feat.npy".format(args.num_features))
  print("saving synthetic dataset into a .npy file...")
  np.save(out_file, X_data)
  folder_path = os.path.dirname(out_file)
  train_data_synt, val_data_synt, test_data_synt = split_synthetic_dataset(x_data=X_data,
                                                                           save_path=folder_path,
                                                                           TRAIN_SPLIT=args.TRAIN_SPLIT,
                                                                           VAL_SPLIT=args.VAL_SPLIT,
                                                                           VAL_SPLIT_cv=args.VAL_SPLIT_cv,
                                                                           cv=args.cv)





