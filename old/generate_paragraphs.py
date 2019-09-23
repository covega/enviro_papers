import pandas as pd
import sys
import os, os.path
from collections import defaultdict

data_dir = os.path.join(os.getcwd(), 'data/')

rep_and_district_info_filename = 'Names_Districts_Counties.csv'
county_asthma_info_filename = 'Asthma_Data_ALA_6.26.2019.csv'
county_polling_info_filename = 'Yale_Polling.csv'
voting_history_filename = 'vote_history.csv'
state_senate_folder = os.path.join(data_dir, 'daily-kos/state-senate-districts-to-counties/')
state_house_folder = os.path.join(data_dir, 'daily-kos/state-house-districts-to-counties/')

rep_and_district_info = pd.read_csv(data_dir + rep_and_district_info_filename, encoding = "ISO-8859-1")
county_asthma_info = pd.read_csv(data_dir + county_asthma_info_filename, encoding = "ISO-8859-1")
county_polling_info = pd.read_csv(data_dir + county_polling_info_filename, encoding = "ISO-8859-1")
voting_history = pd.read_csv(data_dir + voting_history_filename, encoding = "ISO-8859-1")

district_county_info = {}
for filename in os.listdir(state_senate_folder):
    state_abr = os.path.splitext(filename)[0]
    file_path = os.path.join(state_senate_folder, filename)
    district_county_info[state_abr] = {
        "SS": pd.read_csv(file_path, encoding = "ISO-8859-1")
    }

for filename in os.listdir(state_house_folder):
    state_abr = os.path.splitext(filename)[0]
    file_path = os.path.join(state_house_folder, filename)
    district_county_info[state_abr]["SH"] = pd.read_csv(file_path, encoding = "ISO-8859-1")

# Make sure the data was read correctly and is what we expect

print(rep_and_district_info.head(3))
print("-"*40)
print(county_asthma_info.head(3))
print("-"*40)
print(county_polling_info.head(3))
print("-"*40)
print(voting_history.head(3))
print("-"*40)
print(district_county_info["VA"]["SS"].head(3))
print("-"*40)
print(district_county_info["VA"]["SH"].head(3))



district_to_counties_by_state = {}
for state, state_info in district_county_info.items():
    district_to_counties = {}

    to_parse = [
        ("SS", "SD #.1", "County.1", "County Pop.\nin SD", "% of SD\nin County"),
        ("SH", "HD #.1", "County.3", "County Pop.\nin HD", "% of HD\nin County"),
    ]

    ss_info = state_info["SS"]

    for (chamber, district_num_key, county_num_key, county_pop_key, percent_key) in to_parse:
        for idx, row in state_info[chamber].iterrows():
            district_num = row.get(district_num_key)
            county = row.get(county_num_key)
            county_pop_in_district = row.get(county_pop_key)
            percent_of_district_in_county = row.get(percent_key)

            if not district_num or not county:
                continue

            district_num = district_num if type(district_num) == str else str(int(district_num))
            district_key = "%s-%s" % (chamber, district_num)

            if district_key not in district_to_counties:
                district_to_counties[district_key] = []

            district_to_counties[district_key].append((
                county.lower(),
                county,
                county_pop_in_district,
                percent_of_district_in_county))

    district_to_counties_by_state[state] = district_to_counties

# Sanity check the outputs

district_to_counties_by_state["VA"]

# Drop labels 133 to get rid of "total" column
asthma_info_counties = [name.lower() for name in county_asthma_info['County'].drop(labels=133)]
asthma_info_children = list(county_asthma_info['Pediatric Asthma'].drop(labels=133))
asthma_info_adults = list(county_asthma_info['Adult Asthma'].drop(labels=133))

asthma_info_children = [int(x.replace(',', '')) for x in asthma_info_children]
asthma_info_adults = [int(x.replace(',', '')) for x in asthma_info_adults]

county_to_asthma_children = dict(zip(asthma_info_counties, asthma_info_children))
county_to_asthma_adults = dict(zip(asthma_info_counties, asthma_info_adults))

# county_to_asthma_adults

# Make a mapping of istrict to asthma totals, # of counts of district.

district_to_asthma_text = {}
for district, county_info in district_to_counties_by_state["VA"].items():
    chamber_abbr = district[:2]
    chamber = "State Senate" if chamber_abbr == "SS" else "State House" if chamber_abbr == "SH" else ""
    district_num = district[3:]
    child_asthma_count = 0
    adult_asthma_count = 0
    for (county_key, county, population, percent_of_district) in county_info:
        child_asthma_count += county_to_asthma_children[county_key]
        adult_asthma_count += county_to_asthma_adults[county_key]

    if len(county_info) > 1:
        district_to_asthma_text[district] =  """In the %d counties that make up %s District %s, %d kids and %d adults live with asthma.""" % (len(county_info), chamber, district_num, child_asthma_count, adult_asthma_count)
    else:
        district_to_asthma_text[district] =  """In the %s District %s, %d kids and %d adults live with asthma.""" % (chamber, district_num, child_asthma_count, adult_asthma_count)



county_polling_info_counties = [name.lower() for name in county_polling_info['GeoName']]
# county_polling_info_pop = dict(zip(county_polling_info_counties,list(county_polling_info['TotalPop'])))
county_polling_info_happening = dict(zip(county_polling_info_counties,list(county_polling_info['happening'])))
county_polling_info_worried = dict(zip(county_polling_info_counties,list(county_polling_info['worried'])))
county_polling_info_regulate = dict(zip(county_polling_info_counties,list(county_polling_info['regulate'])))
county_polling_info_rebates = dict(zip(county_polling_info_counties,list(county_polling_info['rebates'])))


district_to_overview = {}
for district,county_info in district_to_counties_by_state["VA"].items():
    total_pop, know_num, worried_num, regulate_num, rebates_num = 0.0,0.0,0.0,0.0,0.0

    for (county_key, county, population, percent_of_district) in county_info:
        total_pop += population
        know_num += county_polling_info_happening[county_key] * population
        worried_num += county_polling_info_worried[county_key] * population
        regulate_num += county_polling_info_regulate[county_key] * population
        rebates_num += county_polling_info_rebates[county_key] * population

    district_to_overview[district] =  ("In the counties that make up"
                                       " this district, {0:.2f}% know that"
                                       " global warming is happening,"
                                       " and {1:.2f}% are somewhat or very"
                                       " worried about it. {2:.2f}% support"
                                       " regulating CO2 as a pollutant,"
                                       " and {3:.2f}% want to provide tax"
                                       " rebates for people who purchase"
                                       " energy-efficient vehicles or "
                                       "solar panels.").format(know_num/total_pop, worried_num/total_pop, regulate_num/total_pop, rebates_num/total_pop)

district_to_specific = {}
for district, county_info in district_to_counties_by_state["VA"].items():

    # Format: (county_key, county, population, percent_of_district)
    max_pop_county = max(county_info, key=lambda x:x[2]) # by population
    min_pop_county = min(county_info, key=lambda x:x[2]) # by population

    if not max_pop_county or not min_pop_county:
        continue
    min_pop_happening = county_polling_info_happening[min_pop_county[0]]
    min_pop_worried = county_polling_info_worried[min_pop_county[0]]
    min_pop_regulate = county_polling_info_regulate[min_pop_county[0]]
    min_pop_rebates = county_polling_info_rebates[min_pop_county[0]]
    max_pop_happening = county_polling_info_happening[max_pop_county[0]]
    max_pop_worried = county_polling_info_worried[max_pop_county[0]]
    max_pop_regulate = county_polling_info_regulate[max_pop_county[0]]
    max_pop_rebates = county_polling_info_rebates[max_pop_county[0]]

    district_to_specific[district] = ("- Number of people who know that global warming is happening:" +
        "\n\t- {0:.2f}% in {1}, and {2:.2f}% in {3}").format(min_pop_happening, min_pop_county[1], max_pop_happening, max_pop_county[1])
    district_to_specific[district] += (
    "\n- Percent who are somewhat or very worried about climate change: "
        "\n\t- {0:.2f}% in {1}, and {2:.2f}% in {3}").format(min_pop_worried, min_pop_county[1], max_pop_worried, max_pop_county[1])

    district_to_specific[district] += (
    "\n- Support regulating CO2 as a pollutant: "
        "\n\t- {0:.2f}% in {1}, and {2:.2f}% in {3}"
    ).format(min_pop_regulate, min_pop_county[1], max_pop_regulate, max_pop_county[1])

    district_to_specific[district] += (
    "\n- Support tax rebates for people who purchase energy-efficient vehicles or solar panels: "
        "\n\t- {0:.2f}% in {1}, and {2:.2f}% in {3}").format(min_pop_rebates, min_pop_county, max_pop_rebates, max_pop_county)

rep_and_district_info_districts = list(rep_and_district_info['District'])
rep_and_district_info_chambers = list(rep_and_district_info['Branch'])
rep_and_district_info_candidate_first = list(rep_and_district_info['First Name'])
rep_and_district_info_candidate_last = list(rep_and_district_info['Last Name'])

sanitized_candidate_names = []
for first, last in zip(rep_and_district_info_candidate_first,rep_and_district_info_candidate_last):
    sanitized_candidate_names.append(first + " " + last)

candidate_to_district = {}
for (candidate, district, chamber) in zip(
        sanitized_candidate_names,
        rep_and_district_info_districts,
        rep_and_district_info_chambers):
    district_num = -1
    if "th" in district or "st" in district or "nd" in district or "rd" in district:
         district_num = district[:-2]
    else:
         district_num = district
    chamber_abbr = "SS" if chamber == "Senate" else "SH" if chamber == "House" else "??"
    candidate_to_district[candidate] = "%s-%s" % (chamber_abbr, district_num)

candidate_to_voting_record_sentences = defaultdict(list)

for row in voting_history.values:
    candidate_name = row[1] + " " + row[2]
    for i in range(4, len(row)):
        candidate_to_voting_record_sentences[candidate_name].append(row[i].replace("Candidate", candidate_name))

# Parse the voting record
    # We have positive and negative votes, but I think we really just need the sentences
    # Drop first x columns
candidate_to_voting_record_text = {}
for candidate,voting_record_sentences in candidate_to_voting_record_sentences.items():
    voting_record_text = ""
    for sentence in voting_record_sentences:
        if sentence != "-":
            voting_record_text += sentence + " "
    candidate_to_voting_record_text[candidate] = voting_record_text

# Write output to file
with open('output.txt', 'a') as outfile:
    for candidate in sanitized_candidate_names:
        d = candidate_to_district[candidate]
        if d == 'Senate-39':
            print(d, candidate, district_to_specific.keys())
        district_text = (
            district_to_asthma_text[d] + "\n\n" +
            district_to_overview[d] + "\n\n" +
            district_to_specific[d] + "\n\n" +
            candidate_to_voting_record_text[candidate]
        )

        outfile.write("_" * 80 + "\n")
        outfile.write(district_text + "\n")
        outfile.write("_" * 80 + "\n")

# Print output for convenience
with open('output.txt', 'r') as outfile:
    for line in outfile:
        print(line)
