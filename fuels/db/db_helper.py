from .database import *

def get_nearest(x, y):
    trg = 'POINT({} {})'.format(x, y)

    subq_last_status = session.query(
        Status.station_id,
        func.max(Status.date).label('max_date')
    ).group_by(Status.station_id).subquery('t2')

    subq_available_status = session.query(Status).join(
        subq_last_status,
        and_(
            Status.station_id == subq_last_status.c.station_id,
            Status.date == subq_last_status.c.max_date
        )
    ).filter(Status.is_avail == True) \
        .subquery('t3')

    return session.query(
        Station,
        geofunc.ST_DistanceSphere(Station.coordinates, trg).label('distance')) \
        .join(subq_available_status, Station.id == subq_available_status.c.station_id) \
        .order_by('distance') \
        .all()