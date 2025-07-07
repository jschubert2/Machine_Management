# tests/test_cases.py
def test_get_machines_empty(client):
    response = client.get('/machines')
    assert response.status_code == 200
    data = response.get_json()
    assert data["machines"] == []
    assert data["total"] == 0
    

def test_assign_and_get_tool(client, db):
    # Setup: create a machine and tool
    from models import Machine, Tool, ToolAssignment, ToolMetric
    from datetime import date

    machine = Machine(
        name="Cutter",
        category="Cut",
        group="G1",
        manufacturer="ACME",
        created_at=date(2024, 1, 1)  # ← Fix here
    )

    tool = Tool(
        name="Drill Bit A",
        type="Drill",
        created_at=date(2024, 1, 1)  # ← And here
    )

    db.session.add(machine)
    db.session.add(tool)
    db.session.commit()

    # Assign tool to machine
    res_put = client.put(f'/machines/{machine.id}/tool', json={"tool_id": tool.id})
    assert res_put.status_code == 200

    # Add wear metric
    metric = ToolMetric(
        tool_id=tool.id,
        wear_level=23.5,
        status="Active",
        storage_location="Aisle 3, Shelf B"  # or whatever dummy location works
    )
    db.session.add(metric)
    db.session.commit()

    # Fetch tool info
    res_get = client.get(f'/machines/{machine.id}/tool')
    assert res_get.status_code == 200
    data = res_get.get_json()
    assert data["tool_name"] == "Drill Bit A"
    assert data["wear_level"] == 23.5

def test_get_valid_metric(client, setup_metrics):
    resp = client.get('/machines/1/dashboard/performance')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['machine_id'] == 1
    assert data['metric'] == 'performance'
    assert data['days_requested'] is None
    assert len(data['data']) == 10
    # Check ordering oldest -> newest
    dates = [entry['timestamp'] for entry in data['data']]
    assert dates == sorted(dates)

def test_get_metric_with_days(client, setup_metrics):
    resp = client.get('/machines/1/dashboard/oee?days=5')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['days_requested'] == 5
    assert len(data['data']) == 5

def test_invalid_metric_param(client):
    resp = client.get('/machines/1/dashboard/invalidparam')
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Invalid parameter" in data['error']

def test_no_metrics_for_machine(client):
    resp = client.get('/machines/9999/dashboard/oee')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['machine_id'] == 9999
    assert data['data'] == []

def test_get_machine_maintenance(client, setup_user_and_logs):
    user, logs = setup_user_and_logs
    resp = client.get('/machines/1/maintenance')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['machine_id'] == 1
    assert len(data['maintenance_logs']) == 2
    # Check performed_by name concatenation
    for log in data['maintenance_logs']:
        assert log['performed_by'] == f"{user.firstname} {user.lastname}"
    # Dates ascending
    dates = [log['date'] for log in data['maintenance_logs']]
    assert dates == sorted(dates)

def test_post_maintenance_success(client, setup_user_and_logs):
    user, _ = setup_user_and_logs
    new_log = {
        "machine_id": 1,
        "performed_by": user.username,
        "notes": "Replaced filter",
        "date": "2024-07-01T14:30:00",
        "planned": True
    }
    resp = client.post('/maintenance', json=new_log)
    assert resp.status_code == 201
    data = resp.get_json()
    assert "Maintenance log added successfully" in data['message']

def test_post_maintenance_missing_field(client):
    payload = {
        "machine_id": 1,
        # Missing performed_by
        "notes": "Replaced filter",
        "date": "2024-07-01T14:30:00",
        "planned": True
    }
    resp = client.post('/maintenance', json=payload)
    assert resp.status_code == 400
    data = resp.get_json()
    assert "Missing field: performed_by" in data['error']

def test_post_maintenance_user_not_found(client):
    payload = {
        "machine_id": 1,
        "performed_by": "nonexistent_user",
        "notes": "Test note",
        "date": "2024-07-01T14:30:00",
        "planned": True
    }
    resp = client.post('/maintenance', json=payload)
    assert resp.status_code == 404
    data = resp.get_json()
    assert "User not found" in data['error']

def test_post_maintenance_invalid_date(client, setup_user_and_logs):
    user, _ = setup_user_and_logs
    payload = {
        "machine_id": 1,
        "performed_by": user.username,
        "notes": "Invalid date test",
        "date": "not-a-date",
        "planned": True
    }
    resp = client.post('/maintenance', json=payload)
    assert resp.status_code == 500
    data = resp.get_json()
    assert "Invalid isoformat string" in data['error'] or "value error" in data['error'].lower()

def test_get_tools_default_pagination(client, setup_tools_with_metrics):
    response = client.get('/tools')
    assert response.status_code == 200

    data = response.get_json()
    assert 'tools' in data
    assert 'total' in data
    assert data['total'] == 5
    assert data['page'] == 1
    assert data['pages'] == 1
    assert len(data['tools']) == 5

    tool = data['tools'][0]
    assert 'id' in tool
    assert 'name' in tool
    assert 'type' in tool
    assert 'created_at' in tool
    assert 'metrics' in tool
    assert isinstance(tool['metrics'], list)
    assert 'status' in tool['metrics'][0]
    assert 'storage_location' in tool['metrics'][0]
    assert 'wear_level' in tool['metrics'][0]

def test_get_tools_with_custom_pagination(client, setup_tools_with_metrics):
    response = client.get('/tools?page=1&per_page=2')
    assert response.status_code == 200

    data = response.get_json()
    assert data['page'] == 1
    assert data['pages'] == 3
    assert len(data['tools']) == 2

def test_get_tools_empty_result(client):
    response = client.get('/tools')
    assert response.status_code == 200
    data = response.get_json()
    assert data['tools'] == []
    assert data['total'] == 0
    assert data['page'] == 1
    assert data['pages'] == 0

def test_get_users(client, create_users):
    response = client.get('/users')
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2

    user = data[0]
    assert 'id' in user
    assert 'username' in user
    assert 'firstname' in user
    assert 'lastname' in user
    assert 'created_at' in user

def test_register_user_success(client, db):
    from models import User
    payload = {
        "username": "newuser",
        "first_name": "New",
        "last_name": "User"
    }

    response = client.post('/user', json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert "message" in data
    assert data["message"] == "New user added successfully!"

    # Confirm user was actually added
    user = User.query.filter_by(username="newuser").first()
    assert user is not None
    assert user.firstname == "New"
    assert user.lastname == "User"

def test_register_user_missing_field(client):
    payload = {
        "username": "incompleteuser",
        "first_name": "OnlyFirstName"
        # missing last_name
    }

    response = client.post('/user', json=payload)
    assert response.status_code == 500  # internal error due to missing field

    data = response.get_json()
    assert "error" in data
    assert "last_name" in data["error"]  # should raise a KeyError