# enviro_papers
Take datasets on the environment and slot them into candidate specific research papers

## Setup

We're using Python 2.7 and Jupyter Notebook.

1. Install [Jupyter Notebook](https://jupyter.readthedocs.io/en/latest/install.html)

2. Install Virtualenv

    ```bash
    pip install virtualenv
    ```

## Development

```bash
# Enter virtual environment and install dependencies
virtualenv .
source bin/activate
pip3 install -r requirements.txt

# Open Notebook
jupyter notebook
```

## Data
Instructions on how to find and reproduce our data inputs

### Daily Kos Data
Right now we are only using the [Counties ↔ congressional district correspondences](https://docs.google.com/spreadsheets/d/18adZpIghSQQTZLrUNzEdn78ng7mnk2l4-h6IYPsv34I/edit?ts=5ca11736#gid=1870139254) data set from those [provided by Daily Kos](https://www.dailykos.com/stories/2019/7/30/1848730/-How-do-counties-House-districts-and-legislative-districts-all-overlap-These-new-tools-show-you?link_id=6&can_id=6a8a47a87a5af57ad72c93def75c1bf9&source=email-morning-digest-our-new-tools-show-how-counties-house-districts-and-legislative-districts-overlap&email_referrer=email_588758&email_subject=morning-digest-our-new-tools-show-how-counties-house-districts-and-legislative-districts-overlap). The script assumes that you take the Google Sheet and choose `File` > `Download` > `Microsoft Excel (.xlsx)`. Then, after placing in `data/daily-kos/`, run the following script:

```bash
# Enter virtual environment and install dependencies
virtualenv .
source bin/activate
pip3 install -r requirements.txt

# Run the Script
python3 scripts/process-xlsx.py
```

