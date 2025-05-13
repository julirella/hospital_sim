# hospital_sim



## Dependencies
### Language requirement
* Python 3.12.3 (may work with older versions but untested)
### Create virtual environment (optional):
* `python3 -m venv venv`
* `source venv/bin/activate`
### Install dependencies
* `pip install -r requirements.txt`

## Run simulation
### Navigate to hospital_sim directory
* `cd [path/to/hospital_sim]`
### Run default example simulation
* `python3 -m src.main --visualise`
### Run custom simulation
* `python3 -m src.main [-h] [--graph GRAPH] [--people PEOPLE] [--events EVENTS] [--event_output EVENT_OUTPUT] [--nurse_output NURSE_OUTPUT] [--visualise]`

<!-- #### Argument description: -->
  
| Argument                      | Description                           | Default                         |
|-------------------------------|---------------------------------------|---------------------------------|
| `--graph GRAPH`               | Path to the graph layout JSON file    | `input/layouts/horizontal.json` |
| `--people PEOPLE`             | Path to the people JSON file          | `input/people/example1.json`    |
| `--events EVENTS`             | Path to the events JSON file          | `input/events/random.json`      |
| `--event_output EVENT_OUTPUT` | Path to the event log output CSV file | `output/eventLog.csv`           |
| `--nurse_output NURSE_OUTPUT` | Path to the nurse log output CSV file | `output/nurseLog.csv`           |
| `--visualise`                 | Run with visualisation                | Off by default                  |
| `-h, --help`                  | Display help message                  |                                 |

### Run other examples
* `python3 -m src.main --visualise --graph input/layouts/horizontal.json --people input/people/example1.json --events input/events/example1.json`
* `python3 -m src.main --visualise --graph input/layouts/expLayout.json --people input/people/example2.json --events input/events/example2.json`
### Run tests
* `python3 -m unittest discover`


## Visualisation controls
  
| Key          | Function                    |
|--------------|-----------------------------|
| `space`      | pause/resume                |
| `->`         | jump forwards one step      |
| `<-`         | jump backwards one step     |
| `d`          | increase step size by 0.1 s |
| `s`          | decrease step size by 0.1 s |
| `r`          | restart                     |