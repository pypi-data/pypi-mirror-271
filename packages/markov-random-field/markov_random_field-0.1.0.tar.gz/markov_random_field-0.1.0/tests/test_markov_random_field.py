#!/usr/bin/env python

import numpy as np
import pandas as pd

"""Tests for `markov_random_field` package."""


import unittest

from markov_random_field import markov_random_field


class TestMarkov_random_field(unittest.TestCase):
    """Tests for `markov_random_field` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.n_classes = 3
        self.model = markov_random_field.MarkovRandomField(n_classes=self.n_classes)

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_neighbor_difference(self):
        """Test something."""
        image = np.array([
            [0, 0, 1], 
            [1, 0, 1], 
            [1, 1, 1]
        ])
        # [.5, .5, .5]
        # [.5, 1.5, 1]
        # [1, 1, 1]

        label = 1
        expected_result = np.array([
            [.5, .5, .5], 
            [.5, 1.5, 1], 
            [1, 1, 1]
        ], dtype=np.uint8)

        result = self.model.neighbor_difference(image, label)
        np.testing.assert_array_equal(result, expected_result)
    
    def test_001_image_to_dataset(self):
        image = np.array([[0, 1], [2, 3]])
        expected_result = pd.DataFrame({'c1': [0, 0, 1, 1], 'c2': [0, 1, 0, 1], 'value': [0, 2, 1, 3]})
        result = self.model.image_to_dataset(image)
        pd.testing.assert_frame_equal(result, expected_result)


    def test_002_dataset_to_image(self):
        data = pd.DataFrame({'c1': [0, 0, 1, 1], 'c2': [0, 1, 0, 1], 'value': [0, 2, 1, 3]})
        shape = (2, 2)
        expected_result = np.array([[0, 1], [2, 3]])
        result = self.model.dataset_to_image(data, shape)
        np.testing.assert_array_equal(result, expected_result)
    
    #TODO: write test for this
    def test_003_kmeans_clustering(self):
        pass

    #TODO: write test for this
    def test_004_estimate_inital_parameters(self):
        pass

    #TODO: write test for this
    def test_005_fit(self):
        pass



if __name__ == '__main__':
    unittest.main()
