import pytest
import numpy as np
from numpy.testing import assert_array_equal

import spikeextractors as se

from spiketoolkit.comparison import compare_two_sorters



def make_sorting(times1, labels1, times2, labels2):
    sorting1 = se.NumpySortingExtractor()
    sorting2 = se.NumpySortingExtractor()
    sorting1.set_times_labels(np.array(times1), np.array(labels1))
    sorting2.set_times_labels(np.array(times2), np.array(labels2))
    return sorting1, sorting2
    


def test_compare_two_sorters():
    # simple match
    sorting1, sorting2 = make_sorting([100, 200, 300, 400], [0, 0, 1, 0], 
                                                            [101, 201, 301, ], [0, 0, 5])
    sc = compare_two_sorters(sorting1, sorting2)
    
    sc._do_confusion_matrix()
    print(sc._confusion_matrix)
    
        
        
    
    
    
if __name__ == '__main__':
    test_compare_two_sorters()