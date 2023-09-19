import sys

sys.path.insert(0, '../')

from datetime import datetime
from koala.infra.adapters.database.sqlite.models.base import Base
from koala.infra.adapters.database.sqlite.models.expense import Expense
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as ISession

import pytest


def describe_extract_expense_from_pdf():

    @pytest.fixture(scope='function')
    def session():
        # Configuração do banco de dados em memória para testes
        engine = create_engine('sqlite:///:memory:', echo=False)
        Session = sessionmaker(bind=engine)
        session = Session()
        engine.connect()
        Base.metadata.create_all(engine)
        yield session
        session.rollback()

    def test_expense_creation(session: ISession):
        # Cria uma instância do modelo Expense
        expense = Expense(purchased_at=datetime.utcnow(),
                          name="Test Expense",
                          type='fixed',
                          amount=100.0)

        # Adiciona e faz o commit no banco de dados
        session.add(expense)
        session.commit()

        # Verifica se o Expense foi criado corretamente
        assert expense.id is not None
        assert expense.created_at is not None
        assert expense.updated_at is not None
        assert expense.purchased_at is not None
        assert expense.name == "Test Expense" # type: ignore
        assert expense.type == "fixed" # type: ignore
        assert expense.amount == 100.0 # type: ignore
        assert expense.installment_of is None
        assert expense.installment_to is None

    def test_expense_constraints(session):
        # Tenta criar uma instância do modelo Expense sem campos obrigatórios
        with pytest.raises(Exception):
            expense = Expense()
            session.add(expense)
            session.commit()
