import python_sdk_remote.utilities as utilities
import requests
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger
from url_remote.action_name_enum import ActionName
from url_remote.component_name_enum import ComponentName
from url_remote.entity_name_enum import EntityName
from url_remote.url_circlez import OurUrl
from user_context_remote.user_context import UserContext

GROUP_PROFILE_COMPONENT_ID = 211
GROUP_PROFILE_COMPONENT_NAME = "Group Profile Remote Python"
COMPONENT_CATEGORY = LoggerComponentEnum.ComponentCategory.Code.value
COMPONENT_TYPE = LoggerComponentEnum.ComponentType.Remote.value
DEVELOPER_EMAIL = "yarden.d@circ.zone"

obj = {
    'component_id': GROUP_PROFILE_COMPONENT_ID,
    'component_name': GROUP_PROFILE_COMPONENT_NAME,
    'component_category': COMPONENT_CATEGORY,
    'component_type': COMPONENT_TYPE,
    "developer_email": DEVELOPER_EMAIL
}

GROUP_PROFILE_API_VERSION_PER_ENVIRONMENT = {
    "play1": 1,
    "dvlp1": 1
}

user_context = UserContext()


class GroupProfilesRemote:

    def __init__(self, is_test_data: bool = False):
        self.url_circlez = OurUrl()
        self.logger = Logger.create_logger(object=obj, level="INFO")
        self.brand_name = utilities.get_brand_name()
        self.environment_name = utilities.get_environment_name()
        self.is_test_data = is_test_data

    def create(self, group_id: int, relationship_type_id: int, **kwargs):
        self.logger.start("Start create group-rofile-remote")
        response = None
        try:
            url = self.url_circlez.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP_PROFILE.value,
                entity_name=EntityName.GROUP_PROFILE.value,
                version=GROUP_PROFILE_API_VERSION_PER_ENVIRONMENT.get(self.environment_name),
                action_name=ActionName.CREATE_GROUP_PROFILE.value,  # "createGroupProfile",
            )

            json_payload = {
                "groupId": str(group_id),
                "profileId": str(user_context.get_effective_profile_id()),
                "relationshipTypeId": str(relationship_type_id),
                # TODO: not implemented: "is_test_data": kwargs.get("is_test_data", self.is_test_data)
            }

            # TODO Shall we move all the http related functions to module i.e. our_http?
            headers = utilities.create_authorization_http_headers(user_context.get_user_jwt())
            self.logger.info("POST create", object={
                "json_payload": json_payload, "url": url, "action_name": ActionName.CREATE_GROUP_PROFILE.value})
            response = requests.post(url=url, json=json_payload, headers=headers)
            return response

        except requests.ConnectionError as e:
            self.logger.exception("Network problem (e.g. failed to connect)", object=e)
            raise
        except requests.Timeout as e:
            self.logger.exception("Request timed out", object=e)
            raise
        except requests.RequestException as e:
            self.logger.exception(f"General error: {e}", object=e)
            raise
        except Exception as e:
            self.logger.exception(f"An unexpected error occurred: {e}", object=e)
            raise
        finally:
            self.logger.end("End create group-profile-remote", object={"response": response})

    def get_group_profiles_by_group_id_profile_id_relationship_type_id(
            self, *, group_id: int, relationship_type_id: int = None,
            profile_id: int = user_context.get_effective_profile_id()):
        self.logger.start("Start get group-profile-remote")
        try:
            query_parameters = {
                'groupId': group_id,
                'profileId': profile_id
            }
            if relationship_type_id:
                query_parameters["relationshipTypeId"] = relationship_type_id
            url = self.url_circlez.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP_PROFILE.value,
                entity_name=EntityName.GROUP_PROFILE.value,
                version=GROUP_PROFILE_API_VERSION_PER_ENVIRONMENT.get(self.environment_name),
                # "getGroupProfileByGroupIdProfileIdRelationshipTypeId",
                action_name=ActionName.GET_GROUP_PROFILE.value,
                query_parameters=query_parameters
            )

            headers = utilities.create_authorization_http_headers(user_context.get_user_jwt())
            self.logger.info("GET get_group_profiles_by_group_id_profile_id_relationship_type_id", object={
                "query_parameters": query_parameters, "url": url, "action_name": ActionName.GET_GROUP_PROFILE.value})
            response = requests.get(url, headers=headers)
            self.logger.end(f"End get group-profile-remote, response: {response}")
            return response

        except requests.ConnectionError as error:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=error)
            raise
        except requests.Timeout as error:
            self.logger.exception("Request timed out", object=error)
            raise
        except requests.RequestException as error:
            self.logger.exception(f"General error: {error}", object=error)
            raise
        except Exception as error:
            self.logger.exception(
                f"An unexpected error occurred: {error}", object=error)
            self.logger.end("End get group-profile-remote")
            raise

    def get_group_profiles_by_group_id_and_profile_id(
            self, group_id: int, profile_id: int = user_context.get_effective_profile_id()):
        self.logger.start("Start get group-profile-remote")
        try:
            query_parameters = {
                'groupId': group_id,
                'profileId': profile_id
            }
            url = self.url_circlez.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP_PROFILE.value,
                entity_name=EntityName.GROUP_PROFILE.value,
                version=GROUP_PROFILE_API_VERSION_PER_ENVIRONMENT.get(self.environment_name),
                # "getGroupProfileByGroupIdProfileIdRelationshipTypeId",
                action_name=ActionName.GET_GROUP_PROFILE.value,
                query_parameters=query_parameters
            )

            headers = utilities.create_authorization_http_headers(user_context.get_user_jwt())
            self.logger.info("GET get_group_profiles_by_group_id_and_profile_id", object={
                "query_parameters": query_parameters, "url": url, "action_name": ActionName.GET_GROUP_PROFILE.value})
            response = requests.get(url, headers=headers)
            self.logger.end(f"End get group-profile-remote, response: {response}")
            return response

        except requests.ConnectionError as error:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=error)
            raise
        except requests.Timeout as error:
            self.logger.exception("Request timed out", object=error)
            raise
        except requests.RequestException as error:
            self.logger.exception(f"General error: {error}", object=error)
            raise
        except Exception as error:
            self.logger.exception(
                f"An unexpected error occurred: {error}", object=error)
            self.logger.end("End get group-profile-remote")
            raise

    def delete_group_profile(self, *, group_id: int, relationship_type_id: int):
        self.logger.start("Start delete group-profile-remote")
        try:
            url = self.url_circlez.endpoint_url(
                brand_name=self.brand_name,
                environment_name=self.environment_name,
                component_name=ComponentName.GROUP_PROFILE.value,
                entity_name=EntityName.GROUP_PROFILE.value,
                version=GROUP_PROFILE_API_VERSION_PER_ENVIRONMENT.get(self.environment_name),
                action_name=ActionName.DELETE_GROUP_PROFILE.value,  # "deleteGroupProfile",
            )

            payload = {
                'groupId': str(group_id),
                'profileId': str(user_context.get_effective_profile_id()),
                'relationshipTypeId': relationship_type_id
            }

            headers = utilities.create_authorization_http_headers(user_context.get_user_jwt())
            self.logger.info("PUT delete_group_profile", object={
                "url": url, "action_name": ActionName.DELETE_GROUP_PROFILE.value, "payload": payload})

            response = requests.put(url, json=payload, headers=headers)
            self.logger.end(
                f"End delete group-profile-remote, response: {response}")
            return response

        except requests.ConnectionError as e:
            self.logger.exception(
                "Network problem (e.g. failed to connect)", object=e)
            raise
        except requests.Timeout as e:
            self.logger.exception("Request timed out", object=e)
            raise
        except requests.RequestException as e:
            self.logger.exception(f"General error: {e}", object=e)
            raise
        except Exception as e:
            self.logger.exception(
                f"An unexpected error occurred: {e}", object=e)
            self.logger.end("End delete group-profile-remote")
            raise
