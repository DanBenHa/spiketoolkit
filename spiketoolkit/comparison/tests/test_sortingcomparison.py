import pytest
import numpy as np
from numpy.testing import assert_array_equal

import spikeextractors as se

from spiketoolkit.comparison import SortingComparison, compute_performance




def make_sorting(times1, labels1, times2, labels2):
    sorting1 = se.NumpySortingExtractor()
    sorting2 = se.NumpySortingExtractor()
    sorting1.setTimesLabels(np.array(times1), np.array(labels1))
    sorting2.setTimesLabels(np.array(times2), np.array(labels2))
    return sorting1, sorting2
    


def test_SortingComparison():
    # simple match
    sorting1, sorting2 = make_sorting([100, 200, 300, 400], [0, 0, 1, 0], 
                                                            [101, 201, 301, ], [0, 0, 5])
    sc = SortingComparison(sorting1, sorting2, count=True)
    print(sc)
    
    
    compute_performance(sc)
    
    sc._do_confusion()
    print(sc._confusion_matrix)
    
    
    
    
    
    
    
if __name__ == '__main__':
    test_SortingComparison()