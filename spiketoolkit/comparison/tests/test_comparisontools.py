import pytest
import numpy as np
from numpy.testing import assert_array_equal

import spikeextractors as se

from spiketoolkit.comparison import do_matching, do_score_labels, do_counting, do_confusion_matrix




def make_sorting(times1, labels1, times2, labels2):
    sorting1 = se.NumpySortingExtractor()
    sorting2 = se.NumpySortingExtractor()
    sorting1.set_times_labels(np.array(times1), np.array(labels1))
    sorting2.set_times_labels(np.array(times2), np.array(labels2))
    return sorting1, sorting2
    
    


def test_do_matching():
    delta_tp=10
    min_accuracy=0.5
    
    # simple match
    sorting1, sorting2 = make_sorting([100, 200, 300, 400], [0, 0, 1, 0], 
                                                            [101, 201, 301, ], [0, 0, 5])
    event_counts_1,  event_counts_2, matching_event_counts_12, best_match_units_12,\
            matching_event_counts_21, best_match_units_21, \
            unit_map12,  unit_map21 = do_matching(sorting1, sorting2, delta_tp, min_accuracy)
    assert event_counts_1[0] == 3
    assert matching_event_counts_12[0][0] == 2
    assert best_match_units_12[0] == 0
    assert best_match_units_12[1] == 5
    assert unit_map12[0] == 0
    
    # match when 2 units fire at same time
    sorting1, sorting2 = make_sorting([100, 100, 200, 200, 300], [0, 1, 0, 1, 0], 
                                                            [100, 100, 200, 200, 300], [0, 1, 0, 1, 0],)
    event_counts_1,  event_counts_2, matching_event_counts_12, best_match_units_12,\
            matching_event_counts_21, best_match_units_21, \
            unit_map12,  unit_map21 = do_matching(sorting1, sorting2, delta_tp, min_accuracy)
    assert best_match_units_12[0] == 0
    assert best_match_units_12[1] == 1
    assert unit_map12[0] == 0
    assert unit_map12[1] == 1


def test_do_score_labels():
    delta_tp=10
    
    # simple match
    sorting1, sorting2 = make_sorting([100, 200, 300, 400], [0, 0, 1, 0], 
                                                            [101, 201, 301, ], [0, 0, 5])
    unit_map12 = {0: 0, 1: 5}
    labels_st1, labels_st2 = do_score_labels(sorting1, sorting2, delta_tp, unit_map12)
    assert_array_equal(labels_st1[0], ['TP', 'TP', 'FN'])
    assert_array_equal(labels_st1[1], ['TP',])
    assert_array_equal(labels_st2[0], ['TP', 'TP'])
    assert_array_equal(labels_st2[5], ['TP',])

    # match when 2 units fire at same time
    sorting1, sorting2 = make_sorting([100, 100, 200, 200, 300], [0, 1, 0, 1, 0], 
                                                            [100, 100, 200, 200, 300], [0, 1, 0, 1, 0],)
    unit_map12 = {0: 0, 1: 1}
    labels_st1, labels_st2 = do_score_labels(sorting1, sorting2, delta_tp, unit_map12)
    assert_array_equal(labels_st1[0], ['TP', 'TP', 'TP'])
    assert_array_equal(labels_st1[1], ['TP', 'TP', ])
    assert_array_equal(labels_st2[0], ['TP', 'TP', 'TP'])
    assert_array_equal(labels_st2[1], ['TP', 'TP', ])
    
    

def test_do_counting():
    delta_tp=10
    
    ######
    # simple match
    sorting1, sorting2 = make_sorting([100, 200, 300, 400], [0, 0, 1, 0], 
                                                            [101, 201, 301, ], [0, 0, 5])
    unit_map12 = {0: 0, 1: 5}
    labels_st1, labels_st2 = do_score_labels(sorting1, sorting2, delta_tp, unit_map12)
    mixed_counts = do_counting(sorting1, sorting2, unit_map12, labels_st1, labels_st2)

    assert mixed_counts['pooled_with_sum']['TP'] == 3
    assert mixed_counts['pooled_with_sum']['FN'] == 1
    
    assert mixed_counts['by_spiketrains'][0]['TP'] == 2
    assert mixed_counts['by_spiketrains'][0]['CL'] == 0
    assert mixed_counts['by_spiketrains'][0]['FN'] == 1
    assert mixed_counts['by_spiketrains'][0]['FP'] == 0
    assert mixed_counts['by_spiketrains'][0]['NB1'] == 3
    assert mixed_counts['by_spiketrains'][0]['NB2'] == 2
    
    ######
    # match when 2 units fire at same time
    sorting1, sorting2 = make_sorting([100, 100, 200, 200, 300], [0, 1, 0, 1, 0], 
                                                            [100, 100, 200, 200, 300], [0, 1, 0, 1, 0],)
    unit_map12 = {0: 0, 1: 1}
    labels_st1, labels_st2 = do_score_labels(sorting1, sorting2, delta_tp, unit_map12)
    mixed_counts = do_counting(sorting1, sorting2, unit_map12, labels_st1, labels_st2)

    assert mixed_counts['pooled_with_sum']['TP'] == 5
    assert mixed_counts['pooled_with_sum']['FN'] == 0
    
    assert mixed_counts['by_spiketrains'][0]['TP'] == 3
    assert mixed_counts['by_spiketrains'][0]['CL'] == 0
    assert mixed_counts['by_spiketrains'][0]['FN'] == 0
    assert mixed_counts['by_spiketrains'][0]['FP'] == 0
    assert mixed_counts['by_spiketrains'][0]['NB1'] == 3
    assert mixed_counts['by_spiketrains'][0]['NB2'] == 3
    

def test_do_confusion_matrix():
    
    # simple match
    sorting1, sorting2 = make_sorting([100, 200, 300, 400], [0, 0, 1, 0], 
                                                            [101, 201, 301, ], [0, 0, 5])
    unit_map12 = {0: 0, 1: 5}
    labels_st1 = {0: np.array(['TP', 'TP', 'FN']), 1: np.array(['TP'])}
    labels_st2 = {0: np.array(['TP', 'TP']), 5: np.array(['TP'])}
    
    conf_matrix,  st1_idxs, st2_idxs = do_confusion_matrix(sorting1, sorting2, unit_map12, labels_st1, labels_st2)
    cm = np.array([[2, 0, 1], [0, 1, 0], [0, 0, 0]], dtype='int64')
    assert_array_equal(conf_matrix, cm)
    assert_array_equal(st1_idxs, [0, 1])
    assert_array_equal(st2_idxs, [0, 5])

    # match when 2 units fire at same time
    sorting1, sorting2 = make_sorting([100, 100, 200, 200, 300], [0, 1, 0, 1, 0], 
                                                            [100, 100, 200, 200, 300], [0, 1, 0, 1, 0],)
    unit_map12 = {0: 0, 1: 1}
    labels_st1 = {0: np.array(['TP', 'TP', 'TP']), 1: np.array(['TP', 'TP'])}
    labels_st2 = {0: np.array(['TP', 'TP', 'TP']), 1: np.array(['TP', 'TP'])}
    conf_matrix,  st1_idxs, st2_idxs = do_confusion_matrix(sorting1, sorting2, unit_map12, labels_st1, labels_st2)
    cm =  np.array([[3, 0, 0], [0, 2, 0], [0, 0, 0]], dtype='int64')
    assert_array_equal(conf_matrix, cm)
    
    



if __name__ == '__main__':
    #~ test_do_matching()
    #~ test_do_score_labels()
    test_do_counting()
    #~ test_do_confusion_matrix()


