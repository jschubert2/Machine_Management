from flask import Blueprint, request, jsonify
from models import Tool

bp = Blueprint('tools', __name__)

@bp.route('/tools', methods=['GET'])
def get_tools():
    """
    Get a paginated list of tools
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number
      - name: per_page
        in: query
        type: integer
        required: false
        default: 30
        description: Number of tools per page
    responses:
      200:
        description: A paginated list of tools with associated metrics
        schema:
          type: object
          properties:
            tools:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Hammer"
                  type:
                    type: string
                    example: "Hand Tool"
                  created_at:
                    type: string
                    format: date
                    example: "2024-06-01"
                  metrics:
                    type: array
                    items:
                      type: object
                      properties:
                        status:
                          type: string
                          example: "Operational"
                        storage_location:
                          type: string
                          example: "Shelf A3"
                        wear_level:
                          type: number
                          example: 12.5
            total:
              type: integer
              example: 42
            page:
              type: integer
              example: 1
            pages:
              type: integer
              example: 2
    """
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

    print("result: ", result)
    return jsonify({
        "tools": result,
        "total": tools_paginated.total,
        "page": tools_paginated.page,
        "pages": tools_paginated.pages
    })