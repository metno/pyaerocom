from pyaerocom.aeroval._processing_base import ProcessingEngine, DataImporter

class SuperObsEngine(ProcessingEngine, DataImporter):
    """
    Class to handle the processing of combined obs datasets
    """
    raise NotImplementedError('coming soon')

if __name__=='__main__':
    engine = SuperObsEngine()
