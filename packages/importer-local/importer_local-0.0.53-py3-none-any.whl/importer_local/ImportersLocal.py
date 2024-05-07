from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger
from user_context_remote.user_context import UserContext

IMPORTER_LOCAL_PYTHON_COMPONENT_ID = 114
IMPORTER_LOCAL_PYTHON_COMPONENT_NAME = 'importer-local-python-package'

logger_code_init = {
    'component_id': IMPORTER_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': IMPORTER_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'idan.a@circlez.ai'
}
logger = Logger.create_logger(object=logger_code_init)


class ImportersLocal(GenericCRUD):
    def __init__(self):
        super().__init__(default_schema_name="importer", default_table_name="importer_table",
                         default_view_table_name="importer_view", default_id_column_name="importer_id")
        self.user_context = UserContext()

    def insert(self, data_source_id: int, location_id: int, entity_type_id: int, entity_id: int, url: str,
               user_external_id: int, google_people_api_resource_name: str = None) -> int:
        # TODO Can we have data type for url which is not str?
        #   (like what?)
        object1 = {
            'data_source_id': data_source_id,
            'location_id': location_id,
            'entity_type_name': entity_type_id,
            'entity_id': entity_id,
            'url': url,
            'user_external_id': user_external_id,
            'google_people_api_resource_name': google_people_api_resource_name
        }
        logger.start(object=object1)
        try:
            country_id = self._get_country_id(location_id)
            data_json = {
                "data_source_id": data_source_id,
                "user_external_country_id_old": country_id,
                "entity_type_id": entity_type_id,
                "entity_id": entity_id,
                "url": url,
                "created_user_id": self.user_context.get_effective_user_id(),
                "user_external_id": user_external_id,
                "google_people_api_resource_name": google_people_api_resource_name
            }
            importer_id = super().insert(data_json=data_json)
            if not importer_id:
                logger.error("insert importer record failed", object={'data_json': data_json})
                raise Exception("insert importer record failed with data_json: " + str(data_json))

            logger.end("add importer record succeeded", object={'importer_id': importer_id})
            return importer_id
        except Exception as e:
            logger.exception(object=e)
            raise

    # TODO I think we should move/merge this function into location-local-python-package
    def _get_country_id(self, location_id: int) -> int:
        country_id = super().select_one_value_by_id(schema_name="location", view_table_name="location_view",
                                                    id_column_name="location_id", id_column_value=location_id,
                                                    select_clause_value="country_id")
        if not country_id:
            raise Exception("importer local python location_id not found")
        else:
            return country_id
