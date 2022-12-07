from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from CNPM import db, app
from flask_login import UserMixin
from datetime import datetime
from enum import Enum as UserEnum


class UserRole(UserEnum):
    USER = 1
    EMPLOYEE = 2
    ADMIN = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class TuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    so_luot_bay= Column(Integer, default=0)
    ty_le=Column(Float, default=0)
    doanh_thu=Column(Float, default=0)
    chuyen_bay = relationship('ChuyenBay', backref='tuyenbay', lazy=True)

    def __str__(self):
        return self.name


class SanBay(BaseModel):
    name=Column(String(50), nullable=False)
    city=Column(String(50), nullable=False)
    country=Column(String(50), nullable=False)
    chuyen_bay_co_san_bay_di=relationship('ChuyenBay', backref='san_bay_di', lazy=True)
    chuyen_bay_co_san_bay_den=relationship('ChuyenBay', backref='san_bay_den', lazy=True)
    def __str__(self):
        return self.name


class ThoiDiemBay(BaseModel):
    thoi_gian_bay=Column(DateTime, nullable=False)
    thoi_gian_dung=Column(DateTime, nullable=False)
    chuyenbay=relationship('ChuyenBay', backref='thoi_diem_bay', lazy=True)
    def __str__(self):
        return self.name



ChuyenBayCoSanBayTrungGian = db.Table('sb_trunggian', Column('chuyenBay_id' ,Integer, ForeignKey('chuyen_bay.id'), primary_key=True), Column('sanBayTrungGian_id' ,Integer, ForeignKey('san_bay.id'), primary_key=True))


MayBayThuocChuyenBay = db.Table('may_bay_thuoc_chuyen_bay', Column('mayBay_id', Integer, ForeignKey('may_bay.id'), primary_key=True), Column('chuyenBay_id', Integer, ForeignKey('chuyen_bay.id'), primary_key=True))



class ChuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    sanBayDi_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    sanBayDen_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    thoiDiemBay_id = Column(Integer, ForeignKey(ThoiDiemBay.id), nullable=False)
    tuyenBay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    ve = relationship('Ve', backref='chuyen_bay', lazy=True)
    khach_hang = relationship('KhachHang', backref='chuyen_bay', lazy=True)
    san_bay_trung_gian = relationship('SanBay', secondary='sb_trunggian', lazy=True, backref=backref('chuyen_bay', lazy=True))
    may_bay=relationship('MayBay', secondary='may_bay_thuoc_chuyen_bay', lazy=True, backref=backref('chuyen_bay', lazy=True))

    def __str__(self):
        return self.name


class User(BaseModel):
    name = Column(String(10), nullable=False)
    lastName = Column(String(50), nullable=False)
    cccd = Column(String(12), nullable=False)
    sdt = Column(String(12), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    ve = relationship('Ve', backref='nhan_vien', lazy=True)
    ve_id = Column(Integer, ForeignKey('ve.id'), nullable=False)
    chuyenBay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    def  __str__(self):
        return self.name


class MayBay(BaseModel):
    name = Column(String(50), nullable=False)
    hang_ve = relationship('HangVe', backref='may_bay', lazy=True)
    def  __str__(self):
        return self.name


class HangVe(BaseModel):
    price = Column(Float, default=0)
    so_luong_con_lai = Column(Integer, default=80)
    mayBay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    ve = relationship('Ve', backref='hang_ve', lazy=True)
    def  __str__(self):
        return self.name


class Ve(BaseModel):
    name = Column(String(50), nullable=False)
    nhanVien_id = Column(Integer, ForeignKey(User.id), nullable=False)
    chuyenBay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    hangVe_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    khachhang = relationship('KhachHang', backref='ve', lazy=True)

    def __str__(self):
        return self.name


# class KhachHang(BaseModel):
#     name = Column(String(10), nullable=False)
#     lastName = Column(String(50), nullable=False)
#     cccd = Column(String(12), nullable=False)
#     sdt = Column(String(12), nullable=False)
#     ve_id = Column(Integer, ForeignKey(Ve.id), nullable=False)
#     chuyenBay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
#
#     def __str__(self):
#         return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()