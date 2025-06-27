from flask import Blueprint, request, jsonify
from models import MachineMetric

bp = Blueprint('dashboard', __name__)

@bp.route('/machines/<int:machine_id>/dashboard/<string:param>', methods=['GET'])
def get_machine_metric(machine_id, param):
    """
    Get machine metric data over time (OEE, availability, performance, etc.)
    ---
    parameters:
      - name: machine_id
        in: path
        type: integer
        required: true
        description: ID of the machine
      - name: param
        in: path
        type: string
        required: true
        description: Metric to retrieve (oee, availability, performance, output_quality, status)
        enum: ['oee', 'availability', 'performance', 'output_quality', 'status']
      - name: days
        in: query
        type: integer
        required: false
        description: Number of most recent records to retrieve (e.g. 30 = last 30 days)
    responses:
      200:
        description: List of metric values for the machine
        schema:
          type: object
          properties:
            machine_id:
              type: integer
              example: 7
            metric:
              type: string
              example: "performance"
            days_requested:
              type: integer
              example: 30
            data:
              type: array
              items:
                type: object
                properties:
                  timestamp:
                    type: string
                    format: date
                    example: "2024-06-15"
                  value:
                    type: number
                    example: 89.5
      400:
        description: Invalid metric name
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid parameter 'xyz'. Must be one of ['oee', 'availability', 'performance', 'output_quality', 'status']."
    """
    allowed_params = {'oee', 'availability', 'performance', 'output_quality', 'status'}
    if param not in allowed_params:
        return jsonify({"error": f"Invalid parameter '{param}'. Must be one of {list(allowed_params)}."}), 400

    days = request.args.get('days', type=int)  # e.g. ?days=30

    query = MachineMetric.query.filter_by(machine_id=machine_id).order_by(MachineMetric.timestamp.desc())

    if days:
        query = query.limit(days)

    metrics = query.all()
    metrics.reverse()  # oldest to newest

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
