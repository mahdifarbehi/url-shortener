import sqlalchemy as sa
import sqlalchemy.orm as sao

from core.settings import settings

BIND = sa.create_engine(settings.DATABASE_URL, isolation_level="REPEATABLE READ")

DEFAULT_SESSION_FACTORY = sao.sessionmaker(bind=BIND)


TEST_DATABASE_URL = "sqlite:///:memory:"

TEST_BIND = sa.create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=sa.StaticPool,
)
TEST_SESSION_FACTORY = sao.sessionmaker(bind=TEST_BIND)
