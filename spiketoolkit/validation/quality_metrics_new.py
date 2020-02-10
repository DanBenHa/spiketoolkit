from .quality_metric_classes.metric_data import MetricData
from .quality_metric_classes.amplitude_cutoff import AmplitudeCutoff
from .quality_metric_classes.silhouette_score import SilhouetteScore
from .quality_metric_classes.num_spikes import NumSpikes
from .quality_metric_classes.firing_rate import FiringRate
from .quality_metric_classes.d_prime import DPrime
from .quality_metric_classes.l_ratio import LRatio
from .quality_metric_classes.presence_ratio import PresenceRatio
from .parameter_dictionaries import get_recording_params, get_amplitude_params, get_pca_scores_params, get_metric_scope_params, update_param_dicts

def compute_num_spikes(
    sorting,
    sampling_frequency=None,
    metric_scope_params=get_metric_scope_params(),
    save_as_property=True
):
    """
    Computes and returns the num spikes for the sorted dataset.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.
    sampling_frequency:
        The sampling frequency of the result. If None, will check to see if sampling frequency is in sorting extractor.
    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                List of unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.
    save_as_property: bool
        If True, the metric is saved as sorting property
    Returns
    ----------
    num_spikes_epochs: list of lists
        The num spikes of the sorted units in the given epochs.
    """
    ms_dict, = update_param_dicts(metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        sampling_frequency=sampling_frequency,
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    ns = NumSpikes(metric_data=md)
    num_spikes_epochs = ns.compute_metric(save_as_property)
    return num_spikes_epochs


def compute_firing_rates(
    sorting,
    sampling_frequency=None,
    metric_scope_params=get_metric_scope_params(),
    save_as_property=True
):
    """
    Computes and returns the firing rates for the sorted dataset.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.
    sampling_frequency:
        The sampling frequency of the result. If None, will check to see if sampling frequency is in sorting extractor.
    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                List of unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.
    save_as_property: bool
        If True, the metric is saved as sorting property
    Returns
    ----------
    firing_rate_epochs: list of lists
        The firing rates of the sorted units in the given epochs.
    """
    ms_dict, = update_param_dicts(metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        sampling_frequency=sampling_frequency,
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    fr = FiringRate(metric_data=md)
    firing_rate_epochs = fr.compute_metric(save_as_property)
    return firing_rate_epochs


def compute_presence_ratios(
    sorting,
    sampling_frequency=None,
    metric_scope_params=get_metric_scope_params(),
    save_as_property=True
):
    """
    Computes and returns the presence ratios for the sorted dataset.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.
    sampling_frequency:
        The sampling frequency of the result. If None, will check to see if sampling frequency is in sorting extractor.
    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                List of unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.
    save_as_property: bool
        If True, the metric is saved as sorting property
    Returns
    ----------
    presence_ratio_epochs: list of lists
        The presence ratios of the sorted units in the given epochs.
    """
    ms_dict, = update_param_dicts(metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        sampling_frequency=sampling_frequency,
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    pr = PresenceRatio(metric_data=md)
    presence_ratio_epochs = pr.compute_metric(save_as_property)
    return presence_ratio_epochs


def compute_amplitude_cutoffs(
    sorting,
    recording,
    recording_params=get_recording_params(),
    amplitude_params=get_amplitude_params(),
    metric_scope_params=get_metric_scope_params(),
    save_features_props=False,
    save_as_property=True,
    seed=None,
):
    """
    Computes and returns the amplitude cutoffs for the sorted dataset.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.
    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes
    amplitude_params: dict
        This dictionary should contain any subset of the following parameters:
            amp_method: str
                If 'absolute' (default), amplitudes are absolute amplitudes in uV are returned.
                If 'relative', amplitudes are returned as ratios between waveform amplitudes and template amplitudes.
            amp_peak: str
                If maximum channel has to be found among negative peaks ('neg'), positive ('pos') or both ('both' - default)
            amp_frames_before: int
                Frames before peak to compute amplitude.
            amp_frames_after: int
                Frames after peak to compute amplitude.
    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).
    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                List of unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.
    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.
    save_as_property: bool
        If True, the metric is saved as sorting property
    seed: int
        Random seed for reproducibility
    Returns
    ----------
    amplitude_cutoffs_epochs: list of lists
        The amplitude cutoffs of the sorted units in the given epochs.
    """

    rp_dict, ap_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                                   amplitude_params=amplitude_params, 
                                                   metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )
    md.compute_amplitudes(
        amp_method=ap_dict["amp_method"],
        amp_peak=ap_dict["amp_peak"],
        amp_frames_before=ap_dict["amp_frames_before"],
        amp_frames_after=ap_dict["amp_frames_after"],
        save_features_props=save_features_props,
        seed=seed,
    )
    ac = AmplitudeCutoff(metric_data=md)
    amplitude_cutoffs_epochs = ac.compute_metric(save_as_property)
    return amplitude_cutoffs_epochs


def compute_silhouette_scores(
    sorting,
    recording,
    pca_scores_params=get_pca_scores_params(),
    recording_params=get_recording_params(),
    metric_scope_params=get_metric_scope_params(),
    max_spikes_for_silhouette=10000,
    save_features_props=False,
    save_as_property=True,
    seed=None,
):
    """
    Computes and returns the silhouette scores in the sorted dataset.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.

    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes

    pca_scores_params: dict
        This dictionary should contain any subset of the following parameters:
            ms_before: float
                Time period in ms to cut waveforms before the spike events
            ms_after: float
                Time period in ms to cut waveforms after the spike events
            dtype: dtype
                The numpy dtype of the waveforms
            max_spikes_per_unit: int
                The maximum number of spikes to extract per unit.
            max_spikes_for_pca: int
                The maximum number of spikes to use to compute PCA.

    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).

    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.

    max_spikes_for_silhouette: int
        Max spikes to be used for silhouette metric.

    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.

    save_as_property: bool
        If True, the metric is saved as sorting property

    seed: int
        Random seed for reproducibility

    Returns
    ----------
    silhouette_score_epochs: list of lists
        The sihouette scores of the sorted units in the given epochs.
    """
    rp_dict, ps_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                                   pca_scores_params=pca_scores_params, 
                                                   metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    md.compute_pca_scores(
        n_comp=ps_dict["n_comp"],
        ms_before=ps_dict["ms_before"],
        ms_after=ps_dict["ms_after"],
        dtype=ps_dict["dtype"],
        max_spikes_per_unit=ps_dict["max_spikes_per_unit"],
        max_spikes_for_pca=ps_dict["max_spikes_for_pca"],
        save_features_props=save_features_props,
        seed=seed,
    )

    silhouette_score = SilhouetteScore(metric_data=md)
    silhouette_score_epochs = silhouette_score.compute_metric(max_spikes_for_silhouette, seed, save_as_property)
    return silhouette_score_epochs


def compute_d_primes(
    sorting,
    recording,
    pca_scores_params=get_pca_scores_params(),
    recording_params=get_recording_params(),
    metric_scope_params=get_metric_scope_params(),
    num_channels_to_compare=13,
    max_spikes_per_cluster=500,
    save_features_props=False,
    save_as_property=True,
    seed=None,
):
    """
    Computes and returns the d primes in the sorted dataset.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.

    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes

    pca_scores_params: dict
        This dictionary should contain any subset of the following parameters:
            ms_before: float
                Time period in ms to cut waveforms before the spike events
            ms_after: float
                Time period in ms to cut waveforms after the spike events
            dtype: dtype
                The numpy dtype of the waveforms
            max_spikes_per_unit: int
                The maximum number of spikes to extract per unit.
            max_spikes_for_pca: int
                The maximum number of spikes to use to compute PCA.

    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).

    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.

    num_channels_to_compare: int
        The number of channels to be used for the PC extraction and comparison
        
    max_spikes_per_cluster: int
        Max spikes to be used from each unit

    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.

    save_as_property: bool
        If True, the metric is saved as sorting property

    seed: int
        Random seed for reproducibility

    Returns
    ----------
    d_prime_epochs: list of lists
        The d primes of the sorted units in the given epochs.
    """
    rp_dict, ps_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                                   pca_scores_params=pca_scores_params, 
                                                   metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    md.compute_pca_scores(
        n_comp=ps_dict["n_comp"],
        ms_before=ps_dict["ms_before"],
        ms_after=ps_dict["ms_after"],
        dtype=ps_dict["dtype"],
        max_spikes_per_unit=ps_dict["max_spikes_per_unit"],
        max_spikes_for_pca=ps_dict["max_spikes_for_pca"],
        save_features_props=save_features_props,
        seed=seed,
    )

    d_prime = DPrime(metric_data=md)
    d_prime_epochs = d_prime.compute_metric(num_channels_to_compare, max_spikes_per_cluster, seed, save_as_property)
    return d_prime_epochs

def compute_l_ratios(
    sorting,
    recording,
    pca_scores_params=get_pca_scores_params(),
    recording_params=get_recording_params(),
    metric_scope_params=get_metric_scope_params(),
    num_channels_to_compare=13,
    max_spikes_per_cluster=500,
    save_features_props=False,
    save_as_property=True,
    seed=None,
):
    """
    Computes and returns the l ratios in the sorted dataset.

    Parameters
    ----------
    sorting: SortingExtractor
        The sorting result to be evaluated.

    recording: RecordingExtractor
        The given recording extractor from which to extract amplitudes

    pca_scores_params: dict
        This dictionary should contain any subset of the following parameters:
            ms_before: float
                Time period in ms to cut waveforms before the spike events
            ms_after: float
                Time period in ms to cut waveforms after the spike events
            dtype: dtype
                The numpy dtype of the waveforms
            max_spikes_per_unit: int
                The maximum number of spikes to extract per unit.
            max_spikes_for_pca: int
                The maximum number of spikes to use to compute PCA.

    recording_params: dict
        This dictionary should contain any subset of the following parameters:
            apply_filter: bool
                If True, recording is bandpass-filtered.
            freq_min: float
                High-pass frequency for optional filter (default 300 Hz).
            freq_max: float
                Low-pass frequency for optional filter (default 6000 Hz).

    metric_scope_params: dict
        This dictionary should contain any subset of the following parameters:
            unit_ids: list
                unit ids to compute metric for. If not specified, all units are used
            epoch_tuples: list
                A list of tuples with a start and end time for each epoch
            epoch_names: list
                A list of strings for the names of the given epochs.

    num_channels_to_compare: int
        The number of channels to be used for the PC extraction and comparison
        
    max_spikes_per_cluster: int
        Max spikes to be used from each unit

    save_features_props: bool
        If true, it will save amplitudes in the sorting extractor.

    save_as_property: bool
        If True, the metric is saved as sorting property

    seed: int
        Random seed for reproducibility

    Returns
    ----------
    l_ratio_epochs: list of lists
        The l ratios of the sorted units in the given epochs.
    """
    rp_dict, ps_dict, ms_dict = update_param_dicts(recording_params=recording_params, 
                                                   pca_scores_params=pca_scores_params, 
                                                   metric_scope_params=metric_scope_params)

    if ms_dict["unit_ids"] is None:
        ms_dict["unit_ids"] = sorting.get_unit_ids()

    md = MetricData(
        sorting=sorting,
        recording=recording,
        apply_filter=rp_dict["apply_filter"],
        freq_min=rp_dict["freq_min"],
        freq_max=rp_dict["freq_max"],
        unit_ids=ms_dict["unit_ids"],
        epoch_tuples=ms_dict["epoch_tuples"],
        epoch_names=ms_dict["epoch_names"],
    )

    md.compute_pca_scores(
        n_comp=ps_dict["n_comp"],
        ms_before=ps_dict["ms_before"],
        ms_after=ps_dict["ms_after"],
        dtype=ps_dict["dtype"],
        max_spikes_per_unit=ps_dict["max_spikes_per_unit"],
        max_spikes_for_pca=ps_dict["max_spikes_for_pca"],
        save_features_props=save_features_props,
        seed=seed,
    )

    l_ratio = LRatio(metric_data=md)
    l_ratio_epochs = l_ratio.compute_metric(num_channels_to_compare, max_spikes_per_cluster, seed, save_as_property)
    return l_ratio_epochs