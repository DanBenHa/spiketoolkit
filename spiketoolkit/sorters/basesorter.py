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
import threading

import spikeextractors as se

class BaseSorter:
    
    sorter_name = '' # convinience for reporting
    installed = False # check at class level if isntalled or not
    SortingExtractor_Class = None # convinience to get the extractor
    _default_params = {}
    installation_mesg = "" # error message when not installed
    
    def __init__(self, recording=None, output_folder=None, debug=False,
                                    grouping_property=None, parallel=False):
        
        
        assert self.installed, """This sorter {} is not installed.
        Please install it with:  \n{} """.format(self.sorter_name, self.installation_mesg)

        self.debug = debug
        self.grouping_property = grouping_property
        self.parallel = parallel
        
        if output_folder is None:
            output_folder = 'test_' + self.sorter_name
        output_folder = Path(output_folder).absolute()
        
        if grouping_property is None:
            # only one groups
            self.recording_list = [recording]
            self.output_folders = [output_folder]
        else:
            # several groups
            self.recording_list = se.getSubExtractorsByProperty(recording, grouping_property)
            n_group = len(self.recording_list)
            self.output_folders = [Path(str(output_folder) + '_'+str(i)) for i in range(n_group) ]
        
        # make folders
        for output_folder in self.output_folders:
            if not output_folder.is_dir():
                output_folder.mkdir()
    
    @classmethod
    def default_params(self):
        return copy.deepcopy(self._default_params)
    
    def set_params(self):
        # need subclass
        raise(NotImplementedError)
    
    def run(self):
        for i, recording in enumerate(self.recording_list):
            self._setup_recording(recording, self.output_folders[i])
        
        t0 = time.perf_counter()
        
        if not self.parallel:
            for i, recording in enumerate(self.recording_list):
                self._run(recording, self.output_folders[i])
        else:
            # run in threads
            threads = []
            for i, recording in enumerate(self.recording_list):
                thread = threading.Thread(target=self._run, args=(recording, self.output_folders[i]))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
            
        t1 = time.perf_counter()
        
        
        if self.debug:
            print('{} run time {:0.2f}s'.format(self.sorter_name, t1-t0))
        
        return t1 - t0
        
    def _setup_recording(self, recording, output_folder):
        # need be iplemented in subclass
        # this setup ONE recording (or SubExtractor)
        raise(NotImplementedError)

    def _run(self, recording, output_folder):
        # need be iplemented in subclass
        # this run the sorter on ONE recording (or SubExtractor)
        raise(NotImplementedError)
    
    def _get_one_result(self, recording, output_folder):
        # general case that do not work always
        # sometime (klusta, ironclust) need to be over written
        sorting = self.SortingExtractor_Class(output_folder)
        return sorting
    
    def get_result_list(self):
        sorting_list = []
        for i, recording in enumerate(self.recording_list):
            sorting = self._get_one_result(recording, self.output_folders[i])
            sorting_list.append(sorting)
        return sorting_list
    
    def get_result(self):
        sorting_list = self.get_result_list()
        if len(sorting_list) == 1:
            return sorting_list[0]
        else:
            for i, sorting in enumerate(sorting_list):
                group = self.recording_list[i].getChannelProperty(self.recording_list[i].getChannelIds()[0], 'group')
                if sorting is not None:
                    for unit in sorting.getUnitIds():
                        sorting.setUnitProperty(unit, 'group', group)
            
            # reassemble the sorting outputs
            sorting_list = [sort for sort in sorting_list if sort is not None]
            multi_sorting = se.MultiSortingExtractor(sortings=sorting_list)
            return multi_sorting
            
    
    
    
    # new idea
    def get_params_for_particular_recording(self, rec_name):
       """
       this is speculative an nee to be discussed
       """
       return {}


# generic laucnher via function approach
def run_sorter_engine(SorterClass, recording, output_folder=None,
        grouping_property=None, parallel=False, debug=False, **params):
    
    sorter = SorterClass(recording=recording, output_folder=output_folder, 
                                    grouping_property=grouping_property, parallel=parallel, debug=debug)
    sorter.set_params(**params)
    sorter.run()
    sortingextractor = sorter.get_result()
    return sortingextractor
    
