# Issue History #
---
## Relative directory in python ##
It is hard for me to understand the change of directory in runtime util these days I try to read the config file.
- The project file tree
```
	.
	│  readme.md
	│  stmsvc.py
	│  test.py
	│
	├─conf
	│  │  global.config
	│  │  urls.py
	│  │  __init__.py
	│  │
	│  └─__pycache__
	│          urls.cpython-36.pyc
	│          __init__.cpython-36.pyc
	│
	├─input
	│  └─stm
	│          read_json_test.json
	│          table_source_ulrs.csv
	│
	├─output
	│  └─stm
	│          test_json_write.json
	│
	├─stm
	│  │  TemplateOperation.py
	│  │  test.py
	│  │  WebCrawl.py
	│  │  __init__.py
	│  │
	│  └─__pycache__
	│          TemplateOperation.cpython-36.pyc
	│          test.cpython-36.pyc
	│          urls.cpython-36.pyc
	│          __init__.cpython-36.pyc
	│
	├─templates
	│  └─stm
	│          STM_Template.xlsx
	│          stm_template.xltx
	│
	├─utils
	│  │  ReadConfig.py
	│  │  __init__.py
	│  │
	│  └─__pycache__
	│          ReadConfig.cpython-36.pyc
	│          __init__.cpython-36.pyc
	│
	└─__pycache__
	        requests.cpython-36.pyc
```

- The relative directory effect between modules
 - Modules are in the same folder
 	```
 	stm
	 │  TemplateOperation.py
	 │  test.py
	 │  WebCrawl.py
 	```
 Under this situation, the module can be called from each other with simply '.'
 e.g., in the test.py, you can call TemplateOperation module like this:
 	from .TemplateOperation import TemplateOperations

 - Modules are in different folder
 	```
 	stm
	 │  TemplateOperation.py
	```
	```
	utils
	 │  ReadConfig.py
 	```
 In this condition, the if TemplateOperation needs to call ReadConfig, additional codes needed:
 ```
 	if '../' not in sys.path:
 		sys.path.insert(0,'../')
 	from utils.ReadConfig import DecodeConfig
 ```
- The relative directory effect during runtime
 - Reference a file location is totally an independent process from Module dependency
 - The relative folder level totally rely on the entance file of the runtime
 To introduce a configure file `global.config`, consider the following situations:
 	```
 	1. ├─stm
	   │  TemplateOperation.py
	   │  test.py               <- the runtime entrance
	   │  WebCrawl.py
	   ├─conf
	   │  global.config
	```
	   Here the code in test will call a method in TemplateOperation module, and the file path defined in this module.
	   While the relative path was decided by the location of the entrance, so here the relative path should be `../conf/global.config`.
   ```
	2. .
	   │  stmsvc.py             <- the runtime entrance
	   │
	   ├─conf
	   │  │  global.config
	   │
	   ├─stm
	   │  │  TemplateOperation.py
	   │  │  test.py
	   │  │  WebCrawl.py
   ```   
       In this situation, I packed the code to call the TemplateOperation in `stm/test.py` as a class's `foo` method,
       then call this method via the utmost code in `stmsvc.py` in `root` directory.
       This time the relative path still was decided by the location of the entrance, so here the relative path is `./conf/global.config`.
   ```	
	3. .
	   │  stmsvc.py             
	   │
	   ├─conf
	   │  │  global.config
	   │
	   ├─stm
	   │  │  TemplateOperation.py
	   │  │  WebCrawl.py
	   │  │	   	   
	   │  ├─substm
	   │  │  │  test.py         <- the runtime entrance
   ```  
	   For this time, following the rule, the relative path should be `../../conf/global.config`

 Seems there is no better route reference solution under this vary route change situation.
 Alternative way is to set a GLOBAL variable class to introduce the absolute folder location.
