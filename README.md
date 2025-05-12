# hospital_sim



## Dependencies
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
* Argument description:
  
| Argument                      | Description                           | Default                                |
|-------------------------------|---------------------------------------|----------------------------------------|
| `--graph GRAPH`               | Path to the graph layout JSON file    | `input/layouts/toScaleLayout.json`     |
| `--people PEOPLE`             | Path to the people JSON file          | `input/people/manyPeople.json`         |
| `--events EVENTS`             | Path to the events JSON file          | `input/events/testEventsRequests.json` |
| `--event_output EVENT_OUTPUT` | Path to the event log output CSV file | `output/eventLog.csv`                  |
| `--nurse_output NURSE_OUTPUT` | Path to the nurse log output CSV file | `output/nurseLog.csv`                  |
| `--visualise`                 | Run with visualisation                | Off by default                         |
| `-h, --help`                  | Display help message                  |                                        |

### Run other examples
* `python3 -m src.main --visualise --graph input/layouts/horizontal.json --people input/people/example1.json --events input/eve
nts/example1.json`
### Run tests
* `python3 -m unittest discover`
