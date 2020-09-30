#!/usr/bin/env bash
python src/scripts/run.py -dataset "synthetic" -dataset_model 1 -data_path "data/synthetic_model_1" -algo "bayesian_lstm" -rnn_units 32 -bs 32 -ep 400 -output_path "output/exp_synthetic_model_1" -mc_samples 1000 -particles 3
python src/scripts/run.py -dataset "synthetic" -dataset_model 1 -data_path "data/synthetic_model_1" -algo "bayesian_lstm" -rnn_units 32 -bs 32 -ep 400 -output_path "output/exp_synthetic_model_1" -mc_samples 1000 -particles 3 -prior_sigma_1 0.5
python src/scripts/run.py -dataset "synthetic" -dataset_model 1 -data_path "data/synthetic_model_1" -algo "bayesian_lstm" -rnn_units 32 -bs 32 -ep 400 -output_path "output/exp_synthetic_model_1" -mc_samples 1000 -particles 3 -prior_sigma_1 0.75
python src/scripts/run.py -dataset "synthetic" -dataset_model 1 -data_path "data/synthetic_model_1" -algo "bayesian_lstm" -rnn_units 32 -bs 32 -ep 400 -output_path "output/exp_synthetic_model_1" -mc_samples 1000 -particles 3 -prior_sigma_1 1.0
python src/scripts/run.py -dataset "synthetic" -dataset_model 1 -data_path "data/synthetic_model_1" -algo "bayesian_lstm" -rnn_units 32 -bs 32 -ep 400 -output_path "output/exp_synthetic_model_1" -mc_samples 1000 -particles 3 -prior_sigma_1 1.5

