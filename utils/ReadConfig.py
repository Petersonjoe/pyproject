# -*- coding: utf-8 -*-
#############################################
# @Author: jlei1
# @Date:   2018-07-04
# @Last Modified By:   jlei1
# @Last Modified Time: 2018-07-04
#############################################

from distutils.log import warn as printf

class DecodeConfig(object):
    """
    DecodeConfig class is to read the config files,
       Configuration file type: .config, e.g., db.config; .csv; .json etc.
    """

    __filepath__ = None
    __filename__ = None

    def __init__(self) -> None:
        super(DecodeConfig, self).__init__()

    def __fileCheck__(self) -> bool:
        if (not self.__filename__) or (not self.__filepath__):
            printf("*** Error: file path or file name is not provided! ***\n")
            return False
        else:
            return True

    def __fileClean__(self) -> None:
        self.__filepath__ = None
        self.__filename__ = None

    def getConfig(self, filepath: str = None, filename: str = None) -> dict:
        '''
        Read file type: .config
        :param1: filepath
        :param2: filename without file extension

        Return a dict structured like `{'section':{'option':'option_value'}}`
        '''
        from configparser import ConfigParser
        self.__filepath__ = filepath
        self.__filename__ = filename
        if not self.__fileCheck__(): 
            self.__fileClean__()
            return

        fileLocation = self.__filepath__ + self.__filename__ + ".config"
        _settings = {}
        try:
            config = ConfigParser()
            config.read(fileLocation)
            section_list = config.sections()
            if len(section_list) == 0:
                printf("*** Warn: No Configuration Info Found! ***\n")
                return
            for section in section_list:
                if not (section in _settings.keys()):
                    _settings[section] = {}
                    _settings[section] = {k: v for k, v in config.items(section)}
                else:
                    printf("*** Error: config section cannot read twice! ***\n")
        except Exception as ex:
            self.__fileClean__()
            printf("*** Error: config data read failed! ***\n")
            printf("*** Error Message ***\n %s\n" % ex.message)
            return None

        if len(_settings.keys()) > 0:
            self.__fileClean__()
            return _settings

        self.__fileClean__()    
        return None

    def getCSV(self, filepath: str = None, filename: str = None, separator: str = ",") -> list:
        '''
        Read file type: .csv

        :param1: filepath
        :param2: filename
        :param3: data separator, default is comma `,`
        
        This method only return the raw list parsed from csv file, 
        every row is a list nested in an outer list regarding to the whole file,
        must override this method when customized result format needed.
        '''
        import csv
        self.__filepath__ = filepath
        self.__filename__ = filename
        if not self.__fileCheck__():
            self.__fileClean__()
            return

        fileLocation = self.__filepath__ + self.__filename__ + ".csv"
        with open(fileLocation, 'r') as csvfile:
            try:
                reader = csv.reader(csvfile, delimiter = separator)
                rows = [row for row in reader]
            except Exception as ex:
                self.__fileClean__()
                printf("*** Error: CSV data read failed! ***\n")
                printf("*** Error Message ***\n %s\n" % ex.message)
                return None

        self.__fileClean__()            
        return rows

    def getJSON(self, filepath: str = None, filename: str = None) -> dict:
        '''
        getJson will read a json file into a python dict with the same data structure
        
        :param1: filepath, input file path where json file is
        :param2: filename, the filename without extension (default `.json`)
        
        This method will read a json file, return a python dict variable with that json structure
        '''
        import json
        self.__filepath__ = filepath
        self.__filename__ = filename
        if not self.__fileCheck__():
            self.__fileClean__()
            return

        fileLocation = self.__filepath__ + self.__filename__ + ".json"
        try:
            with open(fileLocation, "r") as lf:
                data = json.load(lf)
            self.__fileClean__()
            return data
        except Exception as ex:
            self.__fileClean__()
            printf("*** Error: json data read failed! ***\n")
            printf("*** Error Message ***\n %s\n" % ex.message)
            return None
            
    def jsonWrite(self, filepath: str = None, filename: str = None, data: dict = {}) -> None:
        '''
        jsonWrite will write data into a file named `filename`
        
        :param1: filepath, default output path where json result is
        :param2: filename, the filename without extension (default `.json`)
        :param3: data, a dict that packs data as corresponding json format which will be written
        
        This method will directly write result to the file path, no sepecific return value,
        must override this method when customized result format needed.
        '''  
        import json
        self.__filepath__ = filepath
        self.__filename__ = filename
        if not self.__fileCheck__():
            self.__fileClean__()
            return

        fileLocation = self.__filepath__ + self.__filename__ + ".json"  
        try:
            with open(fileLocation, "w") as wf:
                json.dump(data, wf)
            self.__fileClean__()
        except Exception as ex:
            self.__fileClean__()
            printf("*** Error: json data write failed! ***\n")
            printf("*** Error Message ***\n %s\n" % ex.message)
            return None
            
