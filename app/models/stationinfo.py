# coding: utf8
'测定站信息表'

from app import db
from app.models.stationerrorcodereference import StationErrorcodeReference


class StationInfo(db.Model):
    '''
    测定站信息表
    '''
    __tablename__ = 'station_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stationid = db.Column(db.String(12), unique=True)
    comment = db.Column(db.String(50))
    status = db.Column(db.Enum('on', 'off'))
    changetime = db.Column(db.Integer())
    errorcode = db.Column(db.String(5))

    def __init__(self, params=None):
        if params:
            self.stationid = params.get('stationid')
            self.comment = params.get('comment')
            self.status = params.get('status')
            self.changetime = params.get('changetime')
            self.errorcode = params.get('errorcode')

    def get_all_station(self):
        '''
        查询所有的测定站列表
        :return:
        '''
        return db.session \
            .query(StationInfo.id, StationInfo.stationid, StationInfo.comment, StationInfo.status,
                   StationInfo.changetime,
                   StationInfo.errorcode,
                   StationErrorcodeReference.comment.label('reason')) \
            .outerjoin(StationErrorcodeReference, StationInfo.errorcode == StationErrorcodeReference.errorcode) \
            .all()

    def add_one(self):
        '''
        添加一个测定站记录
        :return:
        '''
        db.session.add(self)
        db.session.commit()

    def delete_one(self):
        '''
        删除一个测定站记录
        :return:
        '''
        res = StationInfo.query.filter_by(stationid=self.stationid).first()
        db.session.delete(res)
        db.session.commit()

    def update_one(self):
        '''
        更改测定站信息
        :return:
        '''
        res = StationInfo.query.filter_by(stationid=self.stationid).first()
        if self.comment != None:
            res.comment = self.comment
        if self.status != None:
            res.status = self.status
        if self.changetime != None:
            res.changetime = self.changetime
        if self.errorcode != None:
            res.errorcode = self.errorcode
        db.session.commit()

    def exist_update_or_add(self, stationid, status, errorcode, changetime):
        '''
        当stationid存在的时候，则将状态更改到数据库中，否则如果不存在该stationid，即添加到数据库中
        :return:
        '''
        res = StationInfo.query.filter_by(stationid=stationid).first()
        if res == None:
            # add
            self.add_one()
        else:
            # update
            res.status = status
            res.errorcode = errorcode
            res.changetime = changetime
            db.session.commit()

    def __repr__(self):
        return '<StationInfo %r>' % self.stationid
