"""
Here a proposal for the futur Sorter with class approach.

The main idea is to decompose all intermediate steps to get more 
flexibility:
  * setup the recording (traces, output folder, and so...)
  * set parameters
  * run the sorter (with futur possibility to make it in separate env/container)
  * get the result (SortingExtractor)

One benfit shoudl to compare the "run" time between sorter without
the setup and getting result.

One new idea usefull for tridesclous and maybe other sorter would
a way to adapt params with datasets.


"""

import time
import copy
from pathlib import Path

class BaseSorter:
    
    sortername = '' # convinience for reporting
    installed = False # check at class level if isntalled or not
    SortingExtractor_Class = None # convinience to get the extractor
    _default_params = {}
    installation_mesg = "" # error message when not installed
    
    def __init__(self, recording=None, output_folder=None, debug=False,
                                    by_property=None, parallel=False):
        
        if output_folder is None:
            output_folder = sorter_name
        
        self.output_folder = Path(sorter_name)
        self.recording = recording
        self.debug = debug
        self.by_property = by_property
        self.parallel = parallel

        if not self.output_folder.is_dir():
            output_folder.mkdir()
    
    
    def default_params(self):
        return copy.deepcopy(self._default_params)
    
    def set_params(self):
        # need subclass
        raise(NotImplemenetdError)
    
    def run(self):
        
        
        
        if by_property is None:
            run_by_property = False
        else:
            if by_property in recording.getChannelPropertyNames():
                run_by_property = True
            else:
                run_by_property = False
        
        if run_by_property:
            # I will do this soon but need help
            raise(NotImplementedError('I need help here for by_property'))
        else:
            self._setup_recording()
            t0 = time.perf_counter()
            self._run()
            t1 = time.perf_counter()
        
        if debug:
            print('run time {:.0.2f}s'.frmat(t1-t0))
        
        return t1 - t0
        
    def _setup_recording(self):
        # need subclass
        raise(NotImplemenetdError)

    def _run(self):
        # need subclass
        raise(NotImplemenetdError)
    
    def get_result(self):
        sorting = self.SortingExtractor_Class(self.output_folder)
        return
    
    
    # new idea
    def get_params_for_particular_recording(self, rec_name):
       """
       this is speculative an nee to be discussed
       """
       return {}


# generic laucnher via function approach
def run_sorter_engine(SorterClass, recording, output_folder=None,
        by_property=None, parallel=False, **params):
    
    sorter = SorterClass(recording=recording, output_folder=output_folder, 
                                    by_property=by_property, parallel=parallel)
    sorter.set_params(**params)
    sorter.run()
    sortingextractor = sorter.get_result()
    return sortingextractor
    
