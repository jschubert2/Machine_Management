import pytest
from app import create_app
from models import db as _db
from datetime import datetime, timedelta
from models import MachineMetric,ToolMetric,Tool,User

@pytest.fixture
def create_users(db):
    users = [
        User(username="jdoe", firstname="John", lastname="Doe", created_at=datetime(2024, 6, 1)),
        User(username="asmith", firstname="Alice", lastname="Smith", created_at=datetime(2024, 6, 2))
    ]
    db.session.add_all(users)
    db.session.commit()
    return users

@pytest.fixture
def setup_tools_with_metrics(db):
    tools = []
    for i in range(5):
        tool = Tool(
            name=f"Tool {i}",
            type="Test Type",
            created_at=datetime(2024, 6, 1)
        )
        db.session.add(tool)
        db.session.flush()  # to get tool.id before commit

        metric = ToolMetric(
            tool_id=tool.id,
            status="Operational",
            storage_location=f"Shelf A{i}",
            wear_level=10.0 + i
        )
        db.session.add(metric)
        tools.append(tool)

    db.session.commit()
    return tools

@pytest.fixture
def setup_user_and_logs(db):
    from models import User, MaintenanceLog
    # Create a test user
    user = User(
        username="techA",
        firstname="Technician",
        lastname="A",
        created_at=datetime.utcnow()
    )

    db.session.add(user)
    db.session.commit()

    # Create maintenance logs for machine 1
    logs = [
        MaintenanceLog(
            machine_id=1,
            performed_by=user.id,
            notes="Checked belts",
            date=datetime(2024, 6, 10),
            planned=True
        ),
        MaintenanceLog(
            machine_id=1,
            performed_by=user.id,
            notes="Lubricated motor",
            date=datetime(2024, 6, 12),
            planned=False
        )
    ]
    db.session.add_all(logs)
    db.session.commit()

    return user, logs

@pytest.fixture
def setup_metrics(db):
    """Create test metrics for machine_id=1."""
    base_date = datetime.now().date()
    metrics = []
    for i in range(10):
        m = MachineMetric(
            machine_id=1,
            timestamp=base_date - timedelta(days=i),
            oee=90 - i,
            availability=95 - i * 0.5,
            performance=85 + i,
            output_quality=99 - i * 0.2,
            status=1 if i % 2 == 0 else 0
        )
        db.session.add(m)
        metrics.append(m)
    db.session.commit()
    return metrics

@pytest.fixture
def app():
    app = create_app(testing=True)
    with app.app_context():
        _db.drop_all()
        _db.create_all()
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db(app):
    return _db