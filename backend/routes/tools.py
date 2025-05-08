from flask import Blueprint, request, jsonify
from models import Tool

bp = Blueprint('tools', __name__)

@bp.route('/tools', methods=['GET'])
def get_tools():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    tools_paginated = Tool.query.paginate(page=page, per_page=per_page, error_out=False)

    result = []
    for tool in tools_paginated.items:
        tool_data = {
            "id": tool.id,
            "name": tool.name,
            "type": tool.type,
            "created_at": tool.created_at.strftime('%Y-%m-%d'),
            "metrics": []
        }

        for metric in tool.metrics:
            tool_data["metrics"].append({
                "status": metric.status,
                "storage_location": metric.storage_location,
                "wear_level": metric.wear_level
            })

        result.append(tool_data)
    print("result: ",result)
    return jsonify({
        "tools": result,
        "total": tools_paginated.total,
        "page": tools_paginated.page,
        "pages": tools_paginated.pages
    })
