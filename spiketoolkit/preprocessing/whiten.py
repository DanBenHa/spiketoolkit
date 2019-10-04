from .filterrecording import FilterRecording
import numpy as np


class WhitenRecording(FilterRecording):

    preprocessor_name = 'Whiten'
    installed = True  # check at class level if installed or not
    preprocessor_gui_params = [
        {'name': 'chunksize', 'type': 'int', 'value': 30000, 'default': 30000, 'title':
            "Chunk size for the filter."},
        {'name': 'cache_chunks', 'type': 'bool', 'value': False, 'default': False, 'title':
            "If True filtered traces are computed and cached"},
    ]
    installation_mesg = ""  # err

    def __init__(self, recording, chunksize=30000, cache_chunks=False):
        self._recording = recording
        self._whitening_matrix = self._compute_whitening_matrix()
        FilterRecording.__init__(self, recording=recording, chunksize=chunksize)

    def _get_random_data_for_whitening(self, num_chunks=50, chunksize=500):
        N = self._recording.get_num_frames()
        list = []
        for i in range(num_chunks):
            ff = np.random.randint(0, N - chunksize)
            chunk = self._recording.get_traces(start_frame=ff, end_frame=ff + chunksize)
            list.append(chunk)
        return np.concatenate(list, axis=1)

    def _compute_whitening_matrix(self):
        data = self._get_random_data_for_whitening()
        AAt = data @ np.transpose(data)
        AAt = AAt / data.shape[1]
        U, S, Ut = np.linalg.svd(AAt, full_matrices=True)
        W = (U @ np.diag(1 / np.sqrt(S))) @ Ut
        return W

    def filter_chunk(self, *, start_frame, end_frame):
        chunk = self._recording.get_traces(start_frame=start_frame, end_frame=end_frame)
        chunk2 = self._whitening_matrix @ chunk
        return chunk2


def whiten(recording, chunksize=30000, cache_chunks=False):
    '''
    Whitens the recording extractor traces.

    Parameters
    ----------
    recording: RecordingExtractor
        The recording extractor to be whitened.
    chunksize: int
        The chunk size to be used for the filtering.
    cache_chunks: bool
        If True, filtered traces are computed and cached all at once (default False).
    Returns
    -------
    whitened_recording: WhitenRecording
        The whitened recording extractor

    '''
    return WhitenRecording(
        recording=recording,
        chunksize=chunksize,
        cache_chunks=cache_chunks
    )
