# -*- coding: utf-8 -*-

"""
Test Layer Factory: test cases for the LayerFactory class.
"""

import numpy as np
import pytest
import torch

from sparseypy.core.hpo_objectives.hpo_objective import HPOObjective


class TestHPOObjective:
    """
    TestHPOObjective: a class holding a collection
        of tests focused on the HPOObjective class.
    """
    def test_objective_combination(self) -> None:
        """
        Tests whether the HPOObjective correctly calculates 
        the objective value for some given test data.
        """
        # construct test metric data
        test_metric_data = [
            {
                'BasisSetSizeMetric': [[1,2,3,4], [5,6,7,8]],
                'MatchAccuracyMetric': [[1,1,1,1], [1,1,1,1]],
                'FeatureCoverageMetric': [[1.0, 0.1]],
                'BasisSetSizeIncreaseMetric': [np.array([1,1,1,1]), np.array([1,1,1,1])]
            },
            {
                'BasisSetSizeMetric': [[1,1,1,1], [1,1,1,1]],
                'MatchAccuracyMetric': [[1,1,1,1], [1,1,1,1]],
                'FeatureCoverageMetric': [1.0, 1.0],
                'BasisSetSizeIncreaseMetric': [np.array([1,1,1,1]), np.array([1,1,1,1])]
            },
            # Add more entries as needed
        ]

        # construct test HPO configuration
        hpo_config = {
            "optimization_objective": {
                "combination_method": "mean",
                "objective_terms": [
                    {'metric': {"name": "basis_set_size"}, "weight": 1.0},
                    {'metric': {"name": "match_accuracy"}, "weight": 1},
                    {'metric': {"name": "feature_coverage"}, "weight": 1.0},
                    {'metric': {"name": "basis_set_size_increase"}, "weight": 1}
                ]
            }
        }

        # Initialize HPOObjective with the configuration
        hpo_objective = HPOObjective(hpo_config)

        # Calculate combined metric
        combined_metric = hpo_objective.combine_metrics(test_metric_data)
        # assert metric values
        assert combined_metric['total'] == 1.38125
        test_metric_data = [
            {
                'MatchAccuracyMetric': 5,
                'BasisSetSizeIncreaseMetric': [np.array([3,5,5,7]), np.array([1,9,1,9])]
            },
            {
                'MatchAccuracyMetric': 3,
                'BasisSetSizeIncreaseMetric': [np.array([1,5,1,5]), np.array([2,4,2,4])]
            },
            # Add more entries as needed
        ]

        # construct test HPO configuration
        hpo_config = {
            "optimization_objective": {
                "combination_method": "mean",
                "objective_terms": [
                    {'metric': {"name": "match_accuracy"}, "weight": 1.0},
                    {'metric': {"name": "basis_set_size_increase"}, "weight": 0.5}
                ]
            }
        }

        # Initialize HPOObjective with the configuration
        hpo_objective = HPOObjective(hpo_config)

        # Calculate combined metric
        combined_metric = hpo_objective.combine_metrics(test_metric_data)
        assert combined_metric['total'] == 3
