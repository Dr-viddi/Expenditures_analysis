## About this project
A small script to visualize monthly and annual expenses.

## Preparation
1. Import Data from one year (e.g. from 1.1.2021 - 31.12.2021) from bank account in csv format and place it in the *data* folder.

2. Prepare config. An example config is stored in the *configs* folder

## Install
1. Create new environment with
```
conda create --name myenv python=3.9
```

2. Activate the environment with 
```
conda activate myenv
```

3. Navigate to root folder *Expenditures_visualization/* and enter:
```
pip install .
```

## Run
In the activated environment, just enter the command 
```
visualize
```
The script starts using the example.config.yml in the configs folder. Another config file can be provided via
```
visualize --config <path_to_config>
```


## ToDo
* add tests