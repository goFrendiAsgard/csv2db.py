def make_db():
    from sqlalchemy import Column, Integer, String, text, ForeignKey, Table, ForeignKeyConstraint, create_engine
    from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
    from sqlalchemy.ext.declarative import declarative_base

    # create Base
    Base = declarative_base()

    class Transaction(Base):
        __tablename__ = 'trans'
        id = Column(Integer, primary_key=True)
        code = Column(String)
        date = Column(String)

    class Item(Base):
        __tablename__ = 'item'
        id = Column(Integer, primary_key=True)
        code = Column(String)
        name = Column(String)
        price = Column(Integer)
        unit = Column(String)

    class Transaction_Detail(Base):
        __tablename__ = 'trans_detail'
        id = Column(Integer, primary_key=True)
        qty = Column(Integer)
        id_transaction = Column(Integer, ForeignKey('trans.id'))
        id_item = Column(Integer, ForeignKey('item.id'))

    # create engine
    engine = create_engine('sqlite:///test.db', echo=True)    

    #################### ORM ########################################

    # create db session
    db_session = scoped_session(sessionmaker(bind=engine))
    Base.metadata.create_all(bind=engine)
    db_session.commit()

if __name__ == '__main__':
    make_db()