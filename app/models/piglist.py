# coding: utf8
'种猪信息列表'

from app import db
from sqlalchemy import desc, and_


class PigList(db.Model):
    '''
    种猪信息表
    '''
    __tablename__ = 'pig_list'

    id = db.Column(db.String(15))
    facnum = db.Column(db.String(4))  # 猪场代码
    animalnum = db.Column(db.String(15))  # 种猪号（对种猪的自定义代指）
    earid = db.Column(db.String(12))  # 耳标号 id
    stationid = db.Column(db.String(12))

    entry_time = db.Column(db.Integer)  # 入栏时间
    exit_time = db.Column(db.Integer)  # 出栏时间（只有出栏的猪才会有这个时间）
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 记录的 id

    def __init__(self, params = None):
        if params:
            self.id = params.get('id')
            self.facnum = params.get('facnum')
            self.animalnum = params.get('animalnum')
            self.earid = params.get('earid')
            self.stationid = params.get('stationid')
            self.entry_time = params.get('entry_time')
            self.exit_time = params.get('exit_time')
            self.record_id = params.get('record_id')

    def get_all(self):
        '''
        获取到所有种猪的列表
        :return:
        '''
        return PigList.query.filter(PigList.exit_time.is_(None)).with_entities(PigList.id, PigList.animalnum, PigList.earid, PigList.stationid).all()

    def get_from_station(self, noexit=True):
        '''
        依据测定站查询猪列表
        :return:
        '''
        if noexit:
            # exit_time is None 表示还没有出栏
            return PigList.query.filter(
                and_(PigList.stationid.__eq__(self.stationid), PigList.exit_time.is_(None))
            ).all()
        else:
            return PigList.query.filter_by(stationid=self.stationid).all()

    def can_pig_entry(self):
        '''
        检测种猪是否能入站
        入栏前需要先做测定编号和耳标号检测
        :return:
        '''
        # 未出栏的种猪是否有使用相同的测定编号的
        pid_exist = PigList.query.filter(
            and_(PigList.id.__eq__(self.id), PigList.exit_time.is_(None))
        ).count() > 0
        # 未出栏的种猪是否有使用相同的耳标号的
        earid_exist = PigList.query.filter(
            and_(PigList.earid.__eq__(self.earid), PigList.exit_time.is_(None))
        ).count() > 0

        if pid_exist:
            return {
                'exist': True,
                'msg': '测定编号正在使用'
            }
        elif earid_exist:
            return {
                'exist': True,
                'msg': '耳标号正在使用'
            }
        else:
            return {
                'exist': False,
            }

    def can_update_piginfo(self):
        '''
        检测新修改的种猪信息能否更改
        入栏前需要先做测定编号和耳标号检测
        :return:
        '''
        # 未出栏的种猪是否有使用相同的测定编号的
        # 找不是自己的这条记录
        pid_exist = PigList.query.filter(
            and_(PigList.id.__eq__(self.id), PigList.record_id.__ne__(self.record_id), PigList.exit_time.is_(None))
        ).count() > 0
        # 未出栏的种猪是否有使用相同的耳标号的
        earid_exist = PigList.query.filter(
            and_(PigList.earid.__eq__(self.earid), PigList.record_id.__ne__(self.record_id), PigList.exit_time.is_(None))
        ).count() > 0

        if pid_exist:
            return {
                'exist': True,
                'msg': '测定编号正在使用'
            }
        elif earid_exist:
            return {
                'exist': True,
                'msg': '耳标号正在使用'
            }
        else:
            return {
                'exist': False,
            }

    def entry_one(self):
        '''
        一个种猪入栏
        入栏需要先做测定编号和耳标号检测
        :return:
        '''
        db.session.add(self)
        db.session.commit()
        return self

    def exit_one(self):
        '''
        一个种猪出栏
        :return:
        '''
        PigList.query.filter_by(record_id=self.record_id).update({
            'exit_time': self.exit_time,
        })
        db.session.commit()

    def exit_one_station(self, exit_time):
        '''
        一个测定站的种猪全部出栏
        :return:
        '''
        PigList.query.filter(
            and_(PigList.stationid.__eq__(self.stationid), PigList.exit_time.is_(None))
        ).update({
            'exit_time': exit_time,
        })
        db.session.commit()

    def update_piginfo(self):
        '''
        更改一头猪的信息
        :return:
        '''
        PigList.query.filter_by(record_id=self.record_id).update({
            'id': self.id,
            'animalnum': self.animalnum,
            'earid': self.earid,
        })
        db.session.commit()

    def update_stationid(self):
        '''
        更新所属测定站
        :return:
        '''
        PigList.query.filter_by(id=self.id).update({
            'stationid': self.stationid,
        })
        db.session.commit()

    def __repr__(self):
        return '<PigList %r>' % self.earid
