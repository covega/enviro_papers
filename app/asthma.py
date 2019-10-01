from sqlalchemy import func
from app.models import CountyAsthmaCounts, DistrictAsthmaCounts, CountyFragment

def create_district_astham_counts(session):
    dacs_created = 0

    query = session.query(CountyFragment).\
                    join(CountyAsthmaCounts).\
                    group_by(CountyFragment.district_shortcode).\
                    with_entities(
                        CountyFragment.district_shortcode,
                        func.sum(CountyFragment.percent_of_whole *
                                 CountyAsthmaCounts.num_adults).\
                             label('num_adults'),
                        func.sum(CountyFragment.percent_of_whole *
                                 CountyAsthmaCounts.num_children).\
                             label('num_children'))

    for res in query:
        dac = DistrictAsthmaCounts(district_shortcode=res.district_shortcode,
                                   num_children=int(res.num_children),
                                   num_adults=int(res.num_adults))
        dacs_created += 1
        session.add(dac)

    print("District-level asthma records created: %d" % dacs_created)
    session.commit()
