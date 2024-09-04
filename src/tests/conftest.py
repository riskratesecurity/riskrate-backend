import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import drop_database

from riskrate_backend.core.config import settings
from riskrate_backend.model.models import Base


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(settings.DATABASE_URL)

    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)

    yield engine
    drop_database(engine.url)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Fixture para fornecer uma sessão de banco de dados para os testes."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
