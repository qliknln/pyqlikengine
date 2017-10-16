class Structs:
    def __init__(self):
        pass

    @staticmethod
    def list_object_def(state_name="$", library_id="", field_defs=None, field_labels=None, sort_criterias=None,
                        initial_data_fetch=None):
        if initial_data_fetch is None:
            initial_data_fetch = []
        if sort_criterias is None:
            sort_criterias = []
        if field_labels is None:
            field_labels = []
        if field_defs is None:
            field_defs = []
        return {"qStateName": state_name,
                "qLibraryId": library_id,
                "qDef": {
                    "qFieldDefs": field_defs,
                    "qFieldLabels": field_labels,
                    "qSortCriterias": sort_criterias
                },
                "qInitialDataFetch": initial_data_fetch
                }

    @staticmethod
    def hypercube_def(state_name="$", nx_dims=[], nx_meas=[], nx_page=[], inter_column_sort=[0, 1, 2], suppress_zero=False,
                      suppress_missing=False):
        return {"qStateName": state_name,
                "qDimensions": nx_dims,  # NxDimensions
                "qMeasures": nx_meas,  # NxMeasure
                "qInterColumnSortOrder": inter_column_sort,
                "qSuppressZero": suppress_zero,
                "qSuppressMissing": suppress_missing,
                "qInitialDataFetch": nx_page,  # NxPage
                "qMode": 'S',
                "qNoOfLeftDims": -1,
                "qAlwaysFullyExpanded": False,
                "qMaxStackedCells": 5000,
                "qPopulateMissing": False,
                "qShowTotalsAbove": False,
                "qIndentMode": False,
                "qCalcCond": "",
                "qSortbyYValue": 0
                }

    @staticmethod
    def nx_hypercube_dimensions(dim_def):
        return {"qLibraryId": "",
                "qNullSuppression": False,
                "qDef": dim_def
                }

    @staticmethod
    def nx_inline_dimension_def(field_definitions=[], grouping='N', field_labels=[]):
        return {"qGrouping": grouping,
                "qFieldDefs": field_definitions,
                "qFieldLabels": field_labels
                }

    @staticmethod
    def nx_hypercube_measure(sort_by={}, nx_inline_measures_def=""):
        return {"qSortBy": sort_by,
                "qDef": nx_inline_measures_def
                }

    @staticmethod
    def nx_sort_by(state=0, freq=0, numeric=0, ascii=0, load_order=1):
        return {"qSortByState": state,
                "qSortByFrequency": freq,
                "qSortByNumeric": numeric,
                "qSortByAscii": ascii,
                "qSortByLoadOrder": load_order,
                "qSortByExpression": 0,
                "qExpression": {
                    "qv": ""
                    }
                }

    @staticmethod
    def nx_inline_measure_def(definition, label="", description="", tags=[], grouping="N"):
        return {"qLabel": label,
                "qDescription":	description,
                "qTags": tags,
                "qGrouping": grouping,
                "qDef":	definition
                }

    @staticmethod
    def nx_page(top=0, left=0, height=2, width=2):
        return {"qTop": top,
                "qLeft": left,
                "qHeight": height,
                "qWidth": width
                }