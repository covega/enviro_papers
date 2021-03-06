# enviro_papers
Take datasets on the environment and slot them into candidate specific research papers

## Setup

We're using Python 3.6 and Jupyter Notebook.

1. Install [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html)

2. Install Virtualenv

    ```bash
    pip install virtualenv
    ```

## Development

```bash
# Enter virtual environment and install dependencies
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Create SQL database
python run.py

# Open Notebook
jupyter notebook
```

## Directory Structure

```bash
├── papers.ipynb        # Python Notebook for generating Word docs
├── README.md           # This README
├── app/ 
│   ├── __init__.py     # Runs all app functions
│   ├── config.py       # Configuration values
│   ├── create_tables/  # Scripts that import data from 
│   ├── models/         # SQL table definitions
│   ├── queries/        # Queries that create district-level data
│   ├── templates/      # Word templates
│   └── util.py         # Useful functions
├── data 
│   ├── cleaned         # Data intended for import into SQL
│   └── raw             # Raw data
├── papers.db           # Database file
├── requirements.txt    # Python packages
├── run.py              # Python script that runs the app
├── scripts             # Scripts run to clean data
└── venv                # Virtual environment files
```

## Data
Instructions on how to find and reproduce our data inputs

### ALA asthma data
We are capturing the number of children and adults that have asthma in each county. The ALA has [data on their website](https://www.lung.org/our-initiatives/healthy-air/sota/city-rankings/states/virginia/), and we're pulling it using the [underlying API](https://aws.stateoftheair.org/state/Alaska). 

### Polling data
We're using Yale's [Climate Opionion map](https://climatecommunication.yale.edu/visualizations-data/ycom-us/) data from 2019 to see what people think about the environment and climate change.

### Voting data
We're transforming state level [scorecard PDFs](https://github.com/covega/enviro_papers/tree/master/data/raw/voting) that list every legislator's votes for and against climate issues into [Excel files](https://github.com/covega/enviro_papers/tree/master/data/cleaned/voting) that are machine readable.

### Clean energy jobs data
_In development..._

### Daily Kos data
Right now we are only using the [Counties ↔ congressional district correspondences](https://docs.google.com/spreadsheets/d/18adZpIghSQQTZLrUNzEdn78ng7mnk2l4-h6IYPsv34I/edit?ts=5ca11736#gid=1870139254) data set and the [Counties ↔ legislative district correspondences](https://docs.google.com/spreadsheets/d/1Sk0iDv22KZsVoVDxh8e-f5Oi0Yj-mfK84cTEMbgSYi8/edit#gid=1450132261) from those [provided by Daily Kos](https://www.dailykos.com/stories/2019/7/30/1848730/-How-do-counties-House-districts-and-legislative-districts-all-overlap-These-new-tools-show-you?link_id=6&can_id=6a8a47a87a5af57ad72c93def75c1bf9&source=email-morning-digest-our-new-tools-show-how-counties-house-districts-and-legislative-districts-overlap&email_referrer=email_588758&email_subject=morning-digest-our-new-tools-show-how-counties-house-districts-and-legislative-districts-overlap). The script assumes that you take the Google Sheet and choose `File` > `Download` > `Microsoft Excel (.xlsx)`. Then, after placing in `data/daily-kos/`, run the following script:

```bash
# Enter virtual environment and install dependencies
virtualenv .
source bin/activate
pip install -r requirements.txt

# Run the Script
python scripts/clean_daily_kos.py
```

