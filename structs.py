class Structs:
    def __init__(self):
        pass

    @staticmethod
    def list_object_def(state_name="$", library_id="", field_defs=None, field_labels=None, sort_criterias=None,
                        inital_data_fetch=None):
        if inital_data_fetch is None:
            inital_data_fetch = []
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
                "qInitialDataFetch": inital_data_fetch
                }
