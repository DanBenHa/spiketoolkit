from pathlib import Path

from spiketoolkit.sorters.basesorter import BaseSorter
from spiketoolkit.sorters.tools import _run_command_and_print_output, _spikeSortByProperty, _call_command
import spikeextractors as se

try:
    import klusta
    import klustakwik2
    HAVE_KLUSTA = True
except ModuleNotFoundError:
    HAVE_KLUSTA = False


class KlustaSorter(BaseSorter):
    """
    Parameters
    ----------
    
    
    probe_file
    file_name
    threshold_strong_std_factor
    threshold_weak_std_factor
    detect_sign
    extract_s_before
    extract_s_after
    n_features_per_channel
    pca_n_waveforms_max
    num_starting_clusters
    """
    
    sorter_name = 'klusta'
    installed = HAVE_KLUSTA
    SortingExtractor_Class = se.KlustaSortingExtractor
    
    _default_params = {
        'file_name': None,
        'probe_file': None,
    
        'adjacency_radius': None,
        'threshold_strong_std_factor': 5,
        'threshold_weak_std_factor': 2,
        'detect_sign': -1,
        'extract_s_before': 16,
        'extract_s_after': 32,
        'n_features_per_channel': 3,
        'pca_n_waveforms_max': 10000,
        'num_starting_clusters': 50,
        'parallel': True,
    }
    
    installation_mesg = """
       >>> pip install klusta klustakwik2
    
    More information on klusta at:
      * https://github.com/kwikteam/phy"
      * https://github.com/kwikteam/klusta
    """
    
    
    def __init__(self, **kargs):
        BaseSorter.__init__(self, **kargs)

    def set_params(self, **params):
        self.params = params
        
    
    def _setup_recording(self):
        source_dir = Path(__file__).parent
        
        # alias to params
        p = self.params
        
        # save prb file:
        if p['probe_file'] is None:
            p['probe_file'] = self.output_folder / 'probe.prb'
            se.saveProbeFile(self.recording, p['probe_file'], format='klusta', radius=p['adjacency_radius'])

        # save binary file
        if p['file_name'] is None:
            self.file_name = Path('recording')
        elif file_name.suffix == '.dat':
            self.file_name = p['file_name'].stem
        p['file_name'] = self.file_name
        se.writeBinaryDatFormat(self.recording, self.output_folder / self.file_name)

        if p['detect_sign'] < 0:
            detect_sign = 'negative'
        elif p['detect_sign'] > 0:
            detect_sign = 'positive'
        else:
            detect_sign = 'both'

        # set up klusta config file
        with (source_dir / 'config_default.prm').open('r') as f:
            klusta_config = f.readlines()
        
        
        # Note: should use format with dict approach here
        klusta_config = ''.join(klusta_config).format(
            self.output_folder / self.file_name, p['probe_file'], float(self.recording.getSamplingFrequency()),
            self.recording.getNumChannels(), "'float32'",
            p['threshold_strong_std_factor'], p['threshold_weak_std_factor'], "'" + detect_sign + "'", 
            p['extract_s_before'], p['extract_s_after'], p['n_features_per_channel'], 
            p['pca_n_waveforms_max'], p['num_starting_clusters']
        )

        with (self.output_folder /'config.prm').open('w') as f:
            f.writelines(klusta_config)

    def _run(self):
        
        cmd = 'klusta {} --overwrite'.format(self.output_folder /'config.prm')
        if self.debug:
            print('Running Klusta')
            print(cmd)
        
        _call_command(cmd)
        if not (self.output_folder / (self.file_name.name + '.kwik')).is_file():
            raise Exception('Klusta did not run successfully')

    def get_result(self):
        # overwrite the SorterBase.get_result
        sorting = se.KlustaSortingExtractor(self.output_folder / (self.file_name.name + '.kwik'))
        return sorting


# this behave like the old klusta(...)
def run_klusta(
        recording,
        output_folder=None,
        by_property=None,
        parallel=False,
        debug=False,
        **params):
    
    sorter = KlustaSorter(recording=recording, output_folder=output_folder,
                                    by_property=by_property, parallel=parallel, debug=debug)
    sorter.set_params(**params)
    sorter.run()
    sortingextractor = sorter.get_result()
    
    return sortingextractor
    
