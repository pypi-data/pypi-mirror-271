from flask import Blueprint

from .measure_service import profiling_service

#
# @author: andy
#
profiler_blueprint = Blueprint("profiler", __name__)


@profiler_blueprint.route("/profiler", methods=["GET"])
def index():
    return profiling_service.as_html()
