from .contact_phones_local_constants import CONTACT_PHONES_PYTHON_PACKAGE_CODE_LOGGER_OBJECT
from logger_local.Logger import Logger
from database_mysql_local.generic_mapping import GenericMapping
from phone_local.phones_local import PhonesLocal
from phonenumbers import (NumberParseException, PhoneNumberFormat,
                          format_number, parse)

DEFAULT_SCHEMA_NAME = 'contact_phone'
DEFAULT_ENTITY_NAME1 = 'contact'
DEFAULT_ENTITY_NAME2 = 'phone'
DEFAULT_ID_COLUMN_NAME = 'contact_phone_id'
DEFAULT_TABLE_NAME = 'contact_phone_table'
DEFAULT_VIEW_TABLE_NAME = 'contact_phone_view'


class ContactPhonesLocal(GenericMapping):
    def __init__(self, default_schema_name: str = DEFAULT_SCHEMA_NAME, default_entity_name1: str = DEFAULT_ENTITY_NAME1,
                 default_entity_name2: str = DEFAULT_ENTITY_NAME2, default_id_column_name: str = DEFAULT_ID_COLUMN_NAME,
                 default_table_name: str = DEFAULT_TABLE_NAME, default_view_table_name: str = DEFAULT_VIEW_TABLE_NAME,
                 is_test_data: bool = False):

        super().__init__(default_schema_name=default_schema_name, default_entity_name1=default_entity_name1,
                         default_entity_name2=default_entity_name2, default_id_column_name=default_id_column_name,
                         default_table_name=default_table_name, default_view_table_name=default_view_table_name,
                         is_test_data=is_test_data)
        self.phones_local = PhonesLocal()
        self.logger = Logger.create_logger(object=CONTACT_PHONES_PYTHON_PACKAGE_CODE_LOGGER_OBJECT)

    # UPSERT
    # TODO Why do we have region as a parameter? - Should be able to extract it from the phone or contact_id
    # TODO Expected phone_number is original_phone_number of processed_phone_number?
    def insert_contact_and_link_to_existing_or_new_phone(self, contact_dict: dict, phone_number: str,
                                                         contact_id: int, region: str = None) -> int:
        """
        Insert contact and link to existing or new phone
        :param contact_dict: contact dict
        :param phone_number: phone number
        :param contact_id: contact id
        :param region: region (For example, 'US' stands for the United States, 'GB' for the United Kingdom)
        :return: contact_phone_id
        """
        self.logger.start(object={"contact_dict": contact_dict, "phone_number": phone_number,
                                  "contact_id": contact_id, "region": region})

        # phone = new PhoneLocal( phone_number );
                                                           
        proccessed_phone_number = self.process_phone_number(original_number=phone_number, region=region)

        # Add the people(person/contact/profile/user) to the Country Group based on their phone internationa_dialing_code                                                   
        # TODO call process_people_phone_number( entity_name='Contact', phone) from phone-local-python-package

        # I would recommend moving this code to the PhoneLocal class and calling it in the Phone constructor
        # TODO Can we replace this by UPSERT?
        phone_id_tuple = self.phones_local.select_one_tuple_by_where(
            select_clause_value="phone_id",
            where="full_number_normalized = %s",
            params=(proccessed_phone_number['full_number_normalized'],)
        )
        if not phone_id_tuple:
            # create new phone and add it to phone_table
            self.logger.info(log_message="phone_id is None, adding new phone")
            phone_compare_data_json = {
                "number_original": proccessed_phone_number.get("number_original"),
            }
            phone_id = self.phones_local.upsert(data_json=proccessed_phone_number, data_json_compare=phone_compare_data_json,
                                                view_table_name="phone_view", table_name="phone_table")
            contact_phone_id = self.insert_mapping(entity_name1=self.default_entity_name1,
                                                   entity_name2=self.default_entity_name2,
                                                   entity_id1=contact_id, entity_id2=phone_id)
        else:
            # link to existing phone
            self.logger.info(log_message="phone_id is not None, linking to existing phone")
            phone_id = phone_id_tuple[0]
            mapping_tuple = self.select_multi_mapping_tuple_by_id(entity_name1=self.default_entity_name1,
                                                                  entity_name2=self.default_entity_name2,
                                                                  entity_id1=contact_id, entity_id2=phone_id)
            if not mapping_tuple:
                self.logger.info(log_message="mapping_tuple is None, creating new mapping")
                contact_phone_id = self.insert_mapping(entity_name1=self.default_entity_name1,
                                                       entity_name2=self.default_entity_name2,
                                                       entity_id1=contact_id, entity_id2=phone_id)
            else:
                self.logger.info(log_message="mapping_tuple is not None")
                contact_phone_id = mapping_tuple[0][0]

        self.logger.end(object={"contact_phone_id": contact_phone_id})
        return contact_phone_id

    # TODO: Move this to PhoneLocal
    def process_phone_number(self, original_number: str, region: str = None) -> dict:
        try:
            parsed_number = parse(original_number, region)
            international_code = parsed_number.country_code
            full_number_normalized = format_number(parsed_number, PhoneNumberFormat.E164)
            local_number_normalized = str(parsed_number.national_number)
            # TODO: Shall we add area_code? what shall it be? How can we do it?
            # TODO Can we move number_info to data member in PhoneLocal class
            number_info = {
                "number_original": original_number,
                "international_code": international_code,
                "full_number_normalized": full_number_normalized,
                "local_number_normalized": local_number_normalized,
            }
            return number_info
        #TODO e -> exception
        except NumberParseException as e:
            self.logger.error(
                # TODO Add a second parameter with exception and all parameters of the method
                f"Invalid phone number: {original_number}. Exception: {str(e)}")
