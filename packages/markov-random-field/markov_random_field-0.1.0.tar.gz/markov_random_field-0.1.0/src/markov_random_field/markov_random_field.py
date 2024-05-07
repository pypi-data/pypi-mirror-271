"""Main module."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.signal import convolve2d


class HiddenMarkovRandomField:
    """Markov Random Field"""

    def __init__(self, n_classes: int, n_em_iterations: int = 10, n_map_iterations: int = 10):
        self.n_classes = n_classes
        self.n_em_iterations = n_em_iterations
        self.n_map_iterations = n_map_iterations
            
    
    
    @staticmethod
    def neighbor_difference(image: np.array, label: int):
        """Calculates the Discrepancy of Labels with Neighbors.

        Args:
            image (np.array): grayscale image
            label (int): integer label

        Returns:
            np.array: numpy array of the same shape as the image, where each
                pixel value is the number of neighbors with a different label
                divided by 2.
        """
        # masking of the image for a label
        mask = (image != label).astype(np.uint8)

        # Define a kernel to check left, right, up, down neighbors
        kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=np.uint8)

        # Convolve the mask with the kernel to count different neighbors
        neighbors_diff = convolve2d(mask, kernel, mode='same')
        neighbor_sum = neighbors_diff / 2

        # Return the neighbor sum with uint8 type
        return neighbor_sum.astype(np.uint8)



    @staticmethod
    def image_to_dataset(image):
        """Convert Grayscale Image to CSR type dataset.

        Args:
            image (np.array): grayscale image

        Returns:
            pd.DataFrame: dataframe with [c1, c2, value] columns
        """
        x = np.arange(image.shape[0], dtype=int)
        y = np.arange(image.shape[1], dtype=int)
        yy, xx = np.meshgrid(y, x)
        data = pd.DataFrame({
            'c1': xx.reshape(-1),
            'c2': yy.reshape(-1),
            'value': X.reshape(-1)
        })
        return data


    @staticmethod
    def dataset_to_image(data, shape):
        """Dataset to Grayscale Image Conversion.

        Args:
            data (pd.DataFrame): dataframe with [c1, c2, value] columns
            shape (shape): shape of the array

        Returns:
            np.array: grayscale image array
        """
        image = np.zeros(shape)
        image[data.c1.values, data.c2.values] = data.value.values
        return image



    def kmeans_clustering(self, data):
        """KMeans Clustering of pixel values.

        Args:
            data (Sequence[int]): pixel values.

        Returns:
            np.array: int labels of kmeans clustering of pixel values.
        """
        k_means = KMeans(n_clusters=self.n_clusters)
        k_means.fit(data)
        return k_means.labels_



    def estimate_initial_parameters(self, normalized_image):
        """Estimate the initial distribution parameters for the different classes.

        Args:
            normalized_image (np.array): normalized grayscale image.

        Returns:
            np.array: array of the same shape as the image, where each pixel corresponds to a label.
            dict[int, float]: means of the pixel values of the clusters.
            dict[int, float]: standard deviations of the pixel values of the clusters.
        """
        data = self.image_to_dataset(normalized_image)
        prediction = data.assign(value=self.kmeans_clustering(data[['value']].values))
        X = self.dataset_to_image(prediction, normalized_image.shape)

        means = np.zeros(self.n_classes)
        stds = np.zeros(self.n_classes)

        for s in range(self.n_classes):
            data_s = data[prediction.value == s]
            s_mean = data_s.value.mean()
            s_std = data_s.value.std()
            means[s] = s_mean
            stds[s] = s_std
        return X, means, stds



    def fit(self, image):
        """Fit the HMRF model to the image.

        Args:
            image (np.array): image (with 255 pixel values)
        
        Returns:
            np.array: array of the same shape as the image, where each pixel corresponds to a label determined by the HMRF.
        """
        #TODO: Make this normalize automagically
        Y = image/255#[20:-20, 20:300]/255

        plt.imshow(Y)
        plt.title("Input image (Y) with noise")
        plt.show()

        print("Initializing parameters")
        X, means, stds = self.estimate_initial_parameters(Y, self.n_classes)

        plt.imshow(X)
        plt.title("KMeans estimated states (X)")
        plt.show()


        print("Learning parameters")
        X_current = X.copy()
        means_current = means.copy()
        stds_current = stds.copy()
        sum_U = np.zeros(self.n_em_iterations)
        for em_it in range(self.n_em_iterations):
            print("EM iteration {}".format(em_it))

            print("\tMAP estimation")
            sum_U_MAP = np.zeros(self.n_map_iterations)
            for map_it in range(self.n_map_iterations):
                print("\t\tMAP iteration {}".format(map_it))
                U_prior = np.zeros((self.n_classes, *X.shape))
                U_conditional = np.zeros((self.n_classes, *X.shape))

                for s in range(self.n_classes):
                    # updating the conditional energy function
                    U_conditional[s, :, :] = ((Y - means[s])**2)/(2*stds[s]**2) + np.log2(stds[s])

                    # updating the prior energy function
                    U_prior[s, :, :] = self.neighbor_difference(X, s)

                # aggregate energies
                U = U_prior + U_conditional
                # compute the new states
                X_current = np.argmin(U, axis=0)
                # compute the minimum energy of the new state
                min_U = np.min(U, axis=0)
                sum_U_MAP[map_it] = min_U.sum()

                if (map_it >= 3) and (sum_U_MAP[map_it - 2:map_it].std())/sum_U_MAP[map_it] < 0.0001:
                    break
            # X_MAP = X_current.copy()
            sum_U[em_it] = min_U.sum()

            print("\tParameter estimation")
            P_s_y = np.zeros((self.n_classes, *X_current.shape))
            for s in range(self.n_classes):
                y_prob = 1/np.sqrt(2*np.pi*(stds_current[s]**2))*np.exp(-((Y - means_current[s])**2)/(2*stds_current[s]**2))
                U_s = np.zeros_like(X_current, dtype=float)
                U_s = self.neighbor_difference(X_current, s)
                P_s_y[s, :, :] = np.multiply(y_prob, np.exp(-U_s))

            P_y = P_s_y.sum(0)
            P_l_y = P_s_y/P_y

            for s in range(self.n_classes):
                means_current[s] = np.multiply(P_l_y[s, :, :], Y).sum()/P_l_y[s, :, :].sum()
                stds_current[s] = np.sqrt(np.multiply(P_l_y[s, :, :], (Y - means_current[s])**2).sum()/P_l_y[s, :, :].sum())

            if (em_it >= 3) and (sum_U[em_it - 2:em_it].std()/sum_U[em_it] < 0.0001):
                break

        plt.imshow(X_current)
        plt.title("HMRF estimated states (X)")
        plt.show()

        return X_current