from structs import Structs
import math
from engine_app_api import EngineAppApi
from engine_global_api import EngineGlobalApi
from engine_generic_object_api import EngineGenericObjectApi
from engine_field_api import EngineFieldApi
import pandas as pd


def getDataFrame(connection, appHandle, measures, dimensions, selections={}):
    engineGlobalApi = EngineGlobalApi(connection)
    ### Define Dimensions of hypercube
    hc_inline_dim = Structs.nx_inline_dimension_def(dimensions)

    ### Set sorting of Dimension by Measure
    hc_mes_sort = Structs.nx_sort_by()

    ### Define Measure of hypercube
    hc_inline_mes = Structs.nx_inline_measure_def(measures)

    ### Build hypercube from above definition
    hc_dim = Structs.nx_hypercube_dimensions(hc_inline_dim)
    hc_mes = Structs.nx_hypercube_measure(hc_mes_sort, hc_inline_mes)

    width = len(measures) + len(dimensions)
    height = int(math.floor(10000 / width))
    nx_page = Structs.nx_page(0, 0, height, width)
    hc_def = Structs.hypercube_def("$", hc_dim, hc_mes, [nx_page])

    engineAppApi = EngineAppApi(connection)
    hc_response = engineAppApi.create_object(appHandle, "CH01", "Chart", "qHyperCubeDef", hc_def)
    hc_handle = engineGlobalApi.get_handle(hc_response)

    engineGenericObjectApi = EngineGenericObjectApi(connection)

    engineFieldApi = EngineFieldApi(connection)

    for field in selections.keys():
        fieldHandle = engineGlobalApi.get_handle(engineAppApi.get_field(appHandle, field))
        values = []
        for selectedValue in selections[field]:
            values.append({'qText': selectedValue})

        engineFieldApi.select_values(fieldHandle, values)

    i = 0
    while i % height == 0:
        nx_page = Structs.nx_page(i, 0, height, width)
        hc_data = engineGenericObjectApi.get_hypercube_data(hc_handle, "/qHyperCubeDef", [nx_page])
        elems = hc_data["qDataPages"][0]['qMatrix']

        df = pd.DataFrame()

        for elem in elems:
            j = 0
            for dim in dimensions:
                df.set_value(i, dim, elem[j]["qText"])
                j += 1
            for meas in measures:
                df.set_value(i, meas, elem[j]["qNum"])
                j += 1

            i += 1

    return df
