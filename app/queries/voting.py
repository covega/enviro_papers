from sqlalchemy import func
from sqlalchemy.orm import aliased
from app.models import District, Bill, Vote, DistrictIncumbentVote
from app.config import VOTING_DATASETS

def create_district_incumbent_record(session):
    records_created = 0

    for state_abbr, latest_year, _ in VOTING_DATASETS:
        latest_vote = aliased(Vote)
        all_votes = aliased(Vote)
        query = session.query(latest_vote).\
                        filter(latest_vote.year==latest_year).\
                        join(District, latest_vote.district_shortcode==District.shortcode).\
                        filter(District.state==state_abbr).\
                        join(all_votes, all_votes.legislator_name==latest_vote.legislator_name).\
                        join(Bill, all_votes.bill_id==Bill.id).\
                        group_by(all_votes.district_shortcode, all_votes.legislator_name, Bill.code).\
                        with_entities(
                            all_votes.district_shortcode,
                            all_votes.legislator_name,
                            all_votes.classification,
                            all_votes.year,
                            Bill.id,
                            Bill.code,
                            Bill.title,
                            Bill.pro_environment_decision,
                            Bill.description)

        for res in query:
            records_created += 1
            div = DistrictIncumbentVote(
                district_shortcode=res.district_shortcode,
                legislator_name=res.legislator_name,
                classification=res.classification,
                bill_id=res.id,
                bill_pro_environment_decision=res.pro_environment_decision,
                bill_title=res.title,
                bill_code=res.code,
                bill_description=res.description,
                year=res.year)
            session.add(div)

    print("District-level incumbent voting records created: %d" % records_created)
    session.commit()
