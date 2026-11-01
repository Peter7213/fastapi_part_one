from sqlalchemy.orm import mapped_column, MappedColumn
from sqlalchemy import Integer, Float, String, DateTime, func
from db import Base
import datetime

class Advertisement(Base):
    __tablename__ = 'ads'

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    header: MappedColumn[str] = mapped_column(String)
    description: MappedColumn[str] = mapped_column(String)
    price: MappedColumn[float] = mapped_column(Float)
    author: MappedColumn[str] = mapped_column(String)
    publication_date: MappedColumn[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    @property
    def ad_dict(self):
        return {'id': self.id,
                'header': self.header,
                'description': self.description,
                'author': self.author,
                'price': self.price,
                'publication_date': int(self.publication_date.timestamp())}