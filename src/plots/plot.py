import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import argparse
from src.data_provider.datasets import Dataset, CovidDataset
import numpy as np
import os


class Plot:
    def __init__(self, dataset, alpha=0.8, variance=0.5, shift_x=0.1, output_path=None, colors=['firebrick', 'limegreen','seagreen', 'blueviolet'], marker='o', markersize=4, alpha_plot=0.8, linewidth=0):
        self.output_path = output_path
        self.dataset = dataset
        self.alpha = alpha
        self.variance = variance
        _, _, test_data = self.dataset.get_datasets()
        self.test_data = test_data[:, :-1, :]  # 24 first timesteps.
        self.shift_x = shift_x
        self.get_empirical_distribs()
        # plot params:
        self.color_smc = colors[0]
        self.color_lstm = colors[1]
        self.color_transf = colors[2]
        self.color_bayes = colors[3]
        self.shift_x = shift_x
        self.marker = marker
        self.markersize = markersize
        self.alpha_plot = alpha_plot
        self.linewidth = linewidth

    def get_empirical_distribs(self):
        smc_t_path = os.path.join(self.output_path, "smc_t")
        lstm_path = os.path.join(self.output_path, "lstm")
        transf_path = os.path.join(self.output_path, "baseline_t")
        bayes_path = os.path.join(self.output_path, "bayesian_lstm")
        self.smc_distrib = self.dataset.get_data_from_folder(smc_t_path)
        self.lstm_distrib = self.dataset.get_data_from_folder(lstm_path)
        self.transf_distrib = self.dataset.get_data_from_folder(transf_path)
        self.bayes_distrib = self.dataset.get_data_from_folder(bayes_path)

    def get_true_CI(self, index, tsp):
        mean = np.squeeze(self.test_data[index, tsp])
        lower_bound = mean - 1.96 * np.sqrt(self.variance)
        upper_bound = mean + 1.96 * np.sqrt(self.variance)
        yy = np.linspace(lower_bound, upper_bound, 10)
        return yy

    def get_pred_CI(self, distrib, index, tsp):
        mean = np.squeeze(np.mean(distrib[index, :, tsp], axis=0))
        std = np.squeeze(np.std(distrib[index, :, tsp], axis=0))
        lower_b = mean - 1.96 * std
        upper_b = mean + 1.96 * std
        zz = np.linspace(lower_b, upper_b, 10)
        return zz

    def plot_true_mean(self, idx_test):
        plt.plot(self.test_data[idx_test, :, 0], color='darkcyan', label='True mean', linewidth=3)

    def _plot(self):
        plt.figure(figsize=(15, 10))
        for j in range(1):
            plt.subplot(1, 1, j + 1)
            idx_test = np.random.randint(0, self.test_data.shape[0])
            self.plot_true_mean(idx_test)
            for tsp in range(self.test_data.shape[1]):
                yy = self.get_true_CI(index=idx_test, tsp=tsp)
                smc = self.get_pred_CI(distrib=self.smc_distrib, index=idx_test, tsp=tsp)
                lstm = self.get_pred_CI(distrib=self.lstm_distrib, index=idx_test, tsp=tsp)
                transf = self.get_pred_CI(distrib=self.transf_distrib, index=idx_test, tsp=tsp)
                bayes = self.get_pred_CI(distrib=self.bayes_distrib, index=idx_test, tsp=tsp)
                xx = tsp * np.ones(10)
                if tsp == 0:
                    plt.plot(xx, yy, color='darkcyan', label='True 95% confidence interval', linewidth=3)
                    plt.plot(xx - self.shift_x, smc, color=self.color_smc, label='SMC-Transformer', marker=self.marker, markersize=self.markersize, alpha=self.alpha_plot, linewidth=self.linewidth)
                    plt.plot(xx + 1 * self.shift_x, lstm, color=self.color_lstm, label='MC-Dropout LSTM', marker=self.marker,
                            markersize=self.markersize, alpha=self.alpha_plot, linewidth=self.linewidth)
                    plt.plot(xx + 2 * self.shift_x, transf, color=self.color_transf, label='MC-Dropout Transformer', marker=self.marker,
                             markersize=self.markersize, alpha=self.alpha_plot, linewidth=self.linewidth)
                    plt.plot(xx + 3 * self.shift_x, bayes, color=self.color_bayes, label='Bayesian LSTM',
                             marker=self.marker,
                             markersize=self.markersize, alpha=self.alpha_plot, linewidth=self.linewidth)
                else:
                    plt.plot(xx, yy, color='darkcyan', linewidth=3)
                    plt.plot(xx - self.shift_x, smc, color=self.color_smc, marker=self.marker,
                             markersize=self.markersize, alpha=self.alpha_plot, linewidth=self.linewidth)
                    plt.plot(xx + 1 * self.shift_x, lstm, color=self.color_lstm,
                             markersize=4, alpha=self.alpha_plot, linewidth=self.linewidth)
                    plt.plot(xx + 2 * self.shift_x, transf, color=self.color_transf,
                             marker=self.marker,
                             markersize=self.markersize, alpha=self.alpha_plot, linewidth=self.linewidth)
                    plt.plot(xx + 3 * self.shift_x, bayes, color=self.color_bayes,
                             marker=self.marker,
                             markersize=self.markersize, alpha=self.alpha_plot, linewidth=self.linewidth)
            plt.ylabel('Signal values', fontsize=16)
            plt.xlabel('Time steps', fontsize=16)
            plt.grid('on')
            plt.legend(markerscale=3, fontsize=14, frameon=False)
            plt.savefig(os.path.join(self.output_path, "ci_plot_idx_test_{}".format(idx_test)))

    def plot(self, num_plots=5):
        for _ in range(num_plots):
            self._plot()

if __name__ == '__main__':
    # load dataset
    parser = argparse.ArgumentParser()
    # data parameters:
    parser.add_argument("-dataset", type=str, default='synthetic', help='dataset selection')
    parser.add_argument("-dataset_model", type=int, default=1, help="model 1 or 2 for the synthetic dataset.")
    parser.add_argument("-data_path", type=str, default="../../data/synthetic_model_1", help="path for uploading the dataset")
    parser.add_argument("-output_path", type=str, default="../../output/plots/ci_plots/synthetic_model_1",
                        help="path for the saved predicted disrib.")
    parser.add_argument("-alpha", type=float, default=0.8, help="alpha value in synthetic models 1 & 2.")
    parser.add_argument("-beta", type=float, default=0.54, help="beta value for synthetic model 2")
    parser.add_argument('-p', type=float, default=0.7, help="p value for synthetic model 2.")
    parser.add_argument('-variance', type=float, default=0.5, help="variance value for synthetic model.")

    args = parser.parse_args()

    dataset = Dataset(data_path=args.data_path, model=args.dataset_model, name=args.dataset)

    ci_plot = Plot(dataset=dataset, alpha=args.alpha, variance=args.variance, output_path=args.output_path)

    ci_plot.plot()

