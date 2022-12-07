from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from CNPM import db, app
from flask_login import UserMixin
from datetime import datetime


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class TuyenBay(BaseModel):
    __tablename__ = 'tuyenbay'
    name = Column(String(50), nullable=False)
    soLuotBay= Column(Integer, default=0)
    tyLe=Column(Float, default=0)
    doanhThu=Column(Float, default=0)
    chuyenbay = relationship('ChuyenBay', backref='tuyenBay', lazy=True)

    def __str__(self):
        return self.name


class SanBay(BaseModel):
    name=Column(String(50), nullable=False)
    city=Column(String(50), nullable=False)
    country=Column(String(50), nullable=False)
    chuyenbaycosanbaydi=relationship('ChuyenBay', backref=backref('sanbaydi'), lazy=True)
    chuyenbaycosanbayden=relationship('ChuyenBay', backref=backref('sanbayden'), lazy=True)
    def __str__(self):
        return self.name


class ThoiDiemBay(BaseModel):
    thoiGianBay=Column(DateTime, nullable=False)
    thoiGianDung=Column(DateTime, nullable=False)
    chuyenbay=relationship('ChuyenBay', backref=backref('thoidiembay'), lazy=True)
    def __str__(self):
        return self.name



ChuyenBayCoSanBayTrungGian = db.table('sb_trunggian', Column('chuyenBay_id' ,Integer, ForeignKey('chuyenBay.id'), primary_key=True), Column('sanBayTrungGian_id' ,Integer, ForeignKey('sanbay.id'), primary_key=True))


MayBayThuocChuyenBay = db.table('MayBayThuocChuyenBay', Column('mayBay_id', Integer, ForeignKey('maybay.id'), primary_key=True), Column('chuyenBay_id', Integer, ForeignKey('chuyenbay.id'), primary_key=True))



class ChuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    sanBayDi_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    sanBayDen_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    thoiDiemBay_id = Column(Integer, ForeignKey(ThoiDiemBay.id), nullable=False)
    tuyenBay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    ve = relationship('Ve', backref=backref('chuyenbay', lazy=True))
    khachang = relationship('KhachHang', backref=backref('chuyenbay'), lazy=True)
    sanbaytrunggian = relationship('SanBay', secondary='sb_trunggian', backref=backref('chuyenbay'), lazy=True)
    maybay=relationship('MayBay', secondary='MayBayThuocChuyenBay', backref=backref('chuyenbay'), lazy=True)
    tags = relationship('Tag', secondary='tuyenBay_id', lazy='subquery',
                        backref=backref('chuyenbay', lazy=True))

    def __str__(self):
        return self.name


class NhanVien(BaseModel):
    name = Column(String(10), nullable=False)
    lastName = Column(String(50), nullable=False)
    ve = relationship('Ve', backref=backref('nhanvien'), lazy=True)
    def  __str__(self):
        return self.name


class MayBay(BaseModel):
    name = Column(String(50), nullable=False)
    hangVe = relationship('HangVe', backref=backref('maybay'), lazy=True)
    def  __str__(self):
        return self.name


class HangVe(BaseModel):
    price = Column(Float, default=0)
    soLuongChoConLai = Column(Integer, default=80)
    mayBay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    ve = relationship('Ve', backref=backref('hangve'), lazy=True)
    def  __str__(self):
        return self.name


class Ve(BaseModel):
    name = Column(String(50), nullable=False)
    nhanVien_id = Column(Integer, ForeignKey(NhanVien.id), nullable=False)
    chuyenBay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    hangVe_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    khachang = relationship('KhachHang', backref=backref('ve'), lazy=True)
    tags = relationship('Tag', secondary='tuyenBay_id', lazy='subquery',
                        backref=backref('chuyenbay', lazy=True))

    def __str__(self):
        return self.name


class KhachHang(BaseModel):
    name = Column(String(10), nullable=False)
    lastName = Column(String(50), nullable=False)
    cccd = Column(String(12), nullable=False)
    sdt = Column(String(12), nullable=False)
    ve_id = Column(Integer, ForeignKey(Ve.id), nullable=False)
    chuyenBay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)

    def __str__(self):
        return self.name


# class ChuyenBayCoSanBayTrungGian(BaseModel):
#     name =Column(String(50), nullable=False)
#     chuyenBay_id=Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
#     sanBay_id=Column(Integer, ForeignKey(SanBay.id), nullable=False)
#     def __str__(self):
#         return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()