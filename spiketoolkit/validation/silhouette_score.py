import numpy as np

import spikemetrics.metrics as metrics
from spiketoolkit.curation.thresholdcurator import ThresholdCurator

from .quality_metric import QualityMetric

"""
Cole overall comments:
1. Make sure that all data is referenced as --> self._metric_data.
2. Once you are done with this class, you can implement the function so that you can test it in the notebook I gave you. See amplitude cutoffs for reference.
Change
"""
class SilhouetteScore(QualityMetric):
    def __init__(self, metric_data):
        QualityMetric.__init__(self, metric_data)
        #Cole: Change this to has_pca_scores()
        if not metric_data.has_amplitudes():
            #Cole: Change this to must have pca scores
            raise ValueError("MetricData object must have amplitudes")

    def compute_metric(self, max_spikes_for_silhouette=10000, seed=0):
        
        #Cole: Can delete this. Computing data not be done in this class, but in the function (see amplitude cutoff).
        if self._metric_data._pc_features is None:
            assert self._recording is not None, \
                "No recording stored. Add a recording first with set_recording"
            #Cole: Can delete this. Computing data not be done in this class, but in the function (see amplitude cutoff).
            self.compute_pca_scores(self._metric_data._recording)

        silhouette_scores_epochs = []
        for epoch in self._metric_data._epochs:
            in_epoch = np.logical_and(
                self._metric_data._spike_times_pca > epoch[1],
                self._metric_data._spike_times_pca < epoch[2],
            )
            spikes_in_epoch = np.sum(in_epoch)
            spikes_for_silhouette = np.min([spikes_in_epoch, max_spikes_for_silhouette])

            silhouette_scores_all = metrics.calculate_silhouette_score(
                self._metric_data._spike_clusters_pca[in_epoch],
                self._metric_data._total_units,
                self._metric_data._pc_features[in_epoch, :, :],
                self._metric_data._pc_feature_ind,
                spikes_for_silhouette,
                seed=seed,
                #self._metric_data.verbose
                verbose=self.verbose,
            )
            silhouette_scores_list = []
            for i in self._metric_data._unit_indices:
                silhouette_scores_list.append(silhouette_scores_all[i])
            silhouette_scores = np.asarray(silhouette_scores_list)
            silhouette_scores_epochs.append(silhouette_scores)

        #Cole: can remove this. No more caching is done in this class.
        self.metrics["silhouette_score"] = []
        for i, epoch in enumerate(self._epochs):
            self.metrics["silhouette_score"].append(silhouette_scores_epochs[i])
        return silhouette_scores_epochs

    # This looks good
    def threshold_metric(self, threshold, threshold_sign, epoch=0):

        assert epoch < len(self._metric_data.get_epochs()), "Invalid epoch specified"

        silhouette_score_epochs = self.compute_metric()[epoch]
        tc = ThresholdCurator(
            sorting=self._metric_data._sorting, metrics_epoch=silhouette_score_epochs
        )
        tc.threshold_sorting(threshold=threshold, threshold_sign=threshold_sign)
        return tc
