import sys
from lasertools_rffthelper import Axes
from lasertools_trace import models


def trace_model(
    axes: Axes,
    labels: models.base.Labels,
    parameter_information: models.base.ParameterInformation,
    model_information: models.base.ModelInformation,
):
    """Define a trace based on a model

    Keyword arguments:
    - axes -- Object storing Fourier axes
    - labels -- Object storing Fourier and parameter labels
    - parameter_information -- Object storing parameter information
    - model_information -- Object storing model information
    """

    trace_class = None
    for _trace_class in models.trace_classes.values():
        _test_trace_class = _trace_class(
            axes, labels, parameter_information, model_information
        )
        if _test_trace_class.check_id():
            trace_class = _test_trace_class

    if not trace_class:
        sys.exit("Trace model not found.")

    trace_class.initialize()

    return trace_class
