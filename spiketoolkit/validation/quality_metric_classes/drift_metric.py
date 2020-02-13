import numpy as np

import spikemetrics.metrics as metrics
from spiketoolkit.curation.thresholdcurator import ThresholdCurator

from .quality_metric import QualityMetric

class DriftMetric(QualityMetric):
    def __init__(self, metric_data):
        QualityMetric.__init__(self, metric_data, metric_name="drift_metric")

        if not metric_data.has_pca_scores():
            raise ValueError("MetricData object must have pca scores")

    def compute_metric(self, drift_metrics_interval_s, drift_metrics_min_spikes_per_interval, save_as_property):

        max_drifts_epochs = []
        cumulative_drifts_epochs = []
        for epoch in self._metric_data._epochs:
            in_epoch = np.logical_and(
                self._metric_data._spike_times_pca > epoch[1], self._metric_data._spike_times_pca < epoch[2]
            )
            max_drifts_all, cumulative_drifts_all = metrics.calculate_drift_metrics(
                self._metric_data._spike_times_pca[in_epoch],
                self._metric_data._spike_clusters_pca[in_epoch],
                self._metric_data._total_units,
                self._metric_data._pc_features[in_epoch, :, :],
                self._metric_data._pc_feature_ind,
                drift_metrics_interval_s,
                drift_metrics_min_spikes_per_interval,
                verbose=self._metric_data.verbose,
            )
            max_drifts_list = []
            cumulative_drifts_list = []
            for i in self._metric_data._unit_indices:
                max_drifts_list.append(max_drifts_all[i])
                cumulative_drifts_list.append(cumulative_drifts_all[i])
            max_drifts = np.asarray(max_drifts_list)
            cumulative_drifts = np.asarray(cumulative_drifts_list)
            max_drifts_epochs.append(max_drifts)
            cumulative_drifts_epochs.append(cumulative_drifts)
        if save_as_property:
            self.save_as_property(self._metric_data._sorting, max_drifts_epochs, metric_name="max_drift")
            self.save_as_property(self._metric_data._sorting, cumulative_drifts_epochs, metric_name="cumulative_drift")
        return list(zip(max_drifts_epochs, cumulative_drifts_epochs))

    def threshold_metric(self, threshold, threshold_sign, epoch, metric_name, drift_metrics_interval_s, 
                         drift_metrics_min_spikes_per_interval, save_as_property):

        assert epoch < len(self._metric_data.get_epochs()), "Invalid epoch specified"

        max_drifts_epochs, cumulative_drifts_epochs = self.compute_metric(drift_metrics_interval_s, drift_metrics_min_spikes_per_interval, 
                                                                          save_as_property)[epoch]
        if metric_name == "max_drift":
            metrics_epoch = max_drifts_epochs
        elif metric_name == "cumulative_drift":
            metrics_epoch = cumulative_drifts_epochs
        else:
            raise ValueError("Invalid metric named entered")
                                                                    
        threshold_curator = ThresholdCurator(
            sorting=self._metric_data._sorting, metrics_epoch=metrics_epoch
        )
        threshold_curator.threshold_sorting(
            threshold=threshold, threshold_sign=threshold_sign
        )
        return threshold_curator