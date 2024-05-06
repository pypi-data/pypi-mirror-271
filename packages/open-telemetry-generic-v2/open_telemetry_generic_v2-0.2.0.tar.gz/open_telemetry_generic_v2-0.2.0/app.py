
from opentelemetry import trace
from opentelemetry import metrics

from functools import wraps
    
def wrapper_function(func):
    tracer_generic = trace.get_tracer("generictracer.tracer")
    meter_generic = metrics.get_meter("genericmeter.meter")

    generic_counter = meter_generic.create_counter(
    "generic.calls",
    description="The number of times function has been called",
    )
    @wraps(func)
    def inner_function():
        with tracer.start_as_current_span("generic") as generic:
            result = func()
            generic.set_attribute("generic.value", result)
            counter.add(1, {"generic.value": result})
            return result
        
    return inner_function

def hello():
    print("hello")








