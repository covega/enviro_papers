from sqlalchemy import func, and_
from app.models import CountyPoll, DistrictPoll, CountyFragment

def _avg(column):
    return (
        func.sum(CountyFragment.population * column) /
        func.sum(CountyFragment.population))

def _subquery_for_fn(session, fn):
    return session.query(CountyFragment).\
                   join(CountyPoll). \
                   group_by(CountyFragment.district_shortcode). \
                   with_entities(
                       CountyFragment.district_shortcode.label('d_sc'),
                       CountyFragment.shortcode.label('c_sc'),
                       CountyPoll.percent_happening,
                       CountyPoll.percent_worried,
                       CountyPoll.percent_regulate,
                       CountyPoll.percent_rebates,
                       fn(CountyFragment.population)). \
                   subquery()


def create_district_polls(session):
    dps_created = 0

    # Make subqueries
    largest = _subquery_for_fn(session, func.max)
    smallest = _subquery_for_fn(session, func.min)

    query = session.query(CountyFragment). \
                    join(CountyPoll). \
                    group_by(CountyFragment.district_shortcode). \
                    join(largest, and_(CountyFragment.district_shortcode ==
                                       largest.c.d_sc)). \
                    join(smallest, and_(CountyFragment.district_shortcode ==
                                       smallest.c.d_sc)). \
                    with_entities(
                        CountyFragment.district_shortcode,
                        largest.c.c_sc.label('largest_county_shortcode'),
                        smallest.c.c_sc.label('smallest_county_shortcode'),
                        largest.c.percent_happening. \
                            label('largest_county_percent_happening'),
                        largest.c.percent_worried. \
                            label('largest_county_percent_worried'),
                        largest.c.percent_regulate. \
                            label('largest_county_percent_regulate'),
                        largest.c.percent_rebates. \
                            label('largest_county_percent_rebates'),
                        smallest.c.percent_happening. \
                            label('smallest_county_percent_happening'),
                        smallest.c.percent_worried. \
                            label('smallest_county_percent_worried'),
                        smallest.c.percent_regulate. \
                            label('smallest_county_percent_regulate'),
                        smallest.c.percent_rebates. \
                            label('smallest_county_percent_rebates'),
                        _avg(CountyPoll.percent_happening). \
                            label('avg_percent_happening'),
                        _avg(CountyPoll.percent_worried). \
                            label('avg_percent_worried'),
                        _avg(CountyPoll.percent_regulate). \
                            label('avg_percent_regulate'),
                        _avg(CountyPoll.percent_rebates). \
                            label('avg_percent_rebates'))

    for res in query:
        dp = DistrictPoll(
            district_shortcode=res.district_shortcode,
            largest_county_shortcode=res.largest_county_shortcode,
            smallest_county_shortcode=res.smallest_county_shortcode,
            largest_county_percent_happening=res.largest_county_percent_happening,
            largest_county_percent_worried=res.largest_county_percent_worried,
            largest_county_percent_regulate=res.largest_county_percent_regulate,
            largest_county_percent_rebates=res.largest_county_percent_rebates,
            smallest_county_percent_happening=res.smallest_county_percent_happening,
            smallest_county_percent_worried=res.smallest_county_percent_worried,
            smallest_county_percent_regulate=res.smallest_county_percent_regulate,
            smallest_county_percent_rebates=res.smallest_county_percent_rebates,
            avg_percent_happening=res.avg_percent_happening,
            avg_percent_worried=res.avg_percent_worried,
            avg_percent_regulate=res.avg_percent_regulate,
            avg_percent_rebates=res.avg_percent_rebates)
        dps_created += 1
        session.add(dp)

    print("District-level polling records created: %d" % dps_created)
    session.commit()
