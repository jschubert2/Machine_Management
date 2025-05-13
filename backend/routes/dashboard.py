from flask import Blueprint, request, jsonify
from models import MachineMetric

bp = Blueprint('dashboard', __name__)

@bp.route('/machines/<int:machine_id>/dashboard/<string:param>', methods=['GET'])
def get_machine_metric(machine_id, param):
    allowed_params = {'oee', 'availability', 'performance', 'output_quality', 'status'}
    if param not in allowed_params:
        return jsonify({"error": f"Invalid parameter '{param}'. Must be one of {list(allowed_params)}."}), 400

    days = request.args.get('days', type=int)  #for example: ?days=30

    query = MachineMetric.query.filter_by(machine_id=machine_id).order_by(MachineMetric.timestamp.desc())

    if days:
        query = query.limit(days)

    metrics = query.all()

    #oldest to newest
    metrics.reverse()

    result = [
        {
            "timestamp": m.timestamp.strftime('%Y-%m-%d'),
            "value": getattr(m, param)
        } for m in metrics
    ]

    return jsonify({
        "machine_id": machine_id,
        "metric": param,
        "days_requested": days,
        "data": result
    })
