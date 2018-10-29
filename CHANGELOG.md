# Pyaerocom changelog

Changes below were applied after the release version 0.6.3. 

## After release 0.6.3.

-  Reviewed Config class and initialisation of paths for different database settings
   - Configuration can now easily be changed using method `pyaerocom.const.change_database()`
   - Removed check of individual obsdirs and model dirs in `Config` class as it slows down import of pyaerocom
   - Reading of OBSCONFIG from ini files is more flexible now
