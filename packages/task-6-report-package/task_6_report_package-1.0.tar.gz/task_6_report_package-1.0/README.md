# Task 6 Report Package



## Description

The package contains a program that displays results of racing Monaco.<br/>
To download data, you can specify the following parameters
when starting the program in the terminal: <br/>
  --driver "driver name"  
  --files <folder_path>  
  --desc

## Project structure

task_6_report_package  
│  
├── report_application  
│ ├── `__init.py__`  
│ └── repport_app.py  
│  
└── `__main__.py`  

## Installation

To install the package, input the following in your terminal:
```bash
python3 pip install task_6_reporh_package
```


## Usage

### Run package in CLI with Driver Name Argument:
```
task_6_report_package --files <folder_path> --driver "driver name"
```
Example:
```
task_6_report_package --files ../data_files --driver “Sebastian Vettel”
```


### Run package in CLI with Desc Argument:
```
task_6_report_package --files <folder_path> --desc
```
Example:
```
task_6_report_package --files ../data_files --desc
```


***

## Authors and acknowledgment
Anton Galkin

## License
MIT

## Project status
Study
