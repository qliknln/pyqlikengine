import engine_communicator
import engine_global_api
import engine_app_api
import engine_generic_object_api
import engine_field_api
import structs


class QixEngine:

    def __init__(self, url):
        self.url = url
        self.conn = engine_communicator.EngineCommunicator(url)
        self.ega = engine_global_api.EngineGlobalApi(self.conn)
        self.eaa = engine_app_api.EngineAppApi(self.conn)
        self.egoa = engine_generic_object_api.EngineGenericObjectApi(self.conn)
        self.efa = engine_field_api.EngineFieldApi(self.conn)
        self.Structs = structs.Structs()
        self.app_handle = ''

    def create_app(self, app_name='my_app'):
        app = self.ega.create_app(app_name)
        return app['qAppId']

    def load_script(self, script):
        self.eaa.set_script(self.app_handle, script)
        return self.eaa.do_reload_ex(self.app_handle)['qSuccess']

    def open_app(self, app_obj):
        opened_app = self.ega.open_doc(app_obj)
        self.app_handle = self.ega.get_handle(opened_app)
        return opened_app['qGenericId']

    def create_hypercube(self, list_of_dimensions=[], list_of_measures=[], rows_to_return=1000):
        no_of_columns = len(list_of_dimensions) + len(list_of_measures)
        hc_inline_dim = self.Structs.nx_inline_dimension_def(list_of_dimensions)
        hc_dim = self.Structs.nx_hypercube_dimensions(hc_inline_dim)
        for m in list_of_measures:
            hc_mes_sort = self.Structs.nx_sort_by()
            hc_inline_mes = self.Structs.nx_inline_measure_def(m)
            hc_mes = self.Structs.nx_hypercube_measure(hc_mes_sort, hc_inline_mes)
        nx_page = self.Structs.nx_page(0, 0, rows_to_return, no_of_columns)
        hc_def = self.Structs.hypercube_def("$", [hc_dim], [hc_mes], [nx_page])
        hc_response = self.eaa.create_object(self.app_handle, "CH01", "Chart", "qHyperCubeDef", hc_def)
        hc_handle = self.ega.get_handle(hc_response)
        self.egoa.get_layout(hc_handle)
        hc_data = self.egoa.get_hypercube_data(hc_handle, "/qHyperCubeDef", [nx_page])
        elems = hc_data["qDataPages"][0]['qMatrix']
        dim_list = []
        mes_list = []
        for elem in range(len(elems)):
            dim_list.append(elems[elem][0]["qText"])
            mes_list.append(elems[elem][1]["qNum"])
        return dim_list, mes_list

    def select_in_dimension(self,dimension_name, list_of_values):
        lb_field = self.eaa.get_field(self.app_handle, dimension_name)
        fld_handle = self.ega.get_handle(lb_field)
        values_to_select = []
        for val in list_of_values:
            val = {'qText': val}
            values_to_select.append(val)
        return self.efa.select_values(fld_handle, values_to_select)

    def delete_app(self, app_name):
        return self.ega.delete_app(app_name)['qSuccess']

    def disconnect(self):
        self.conn.close_qvengine_connection(self.conn)
