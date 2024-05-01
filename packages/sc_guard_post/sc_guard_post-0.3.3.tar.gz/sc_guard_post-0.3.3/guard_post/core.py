import abc
from typing import Dict, Literal, Optional

import devtools as dtz

# from guard_post import Client
from guard_post.api.assigns import (
    assign_edge_api_assigns_add_post as assign_edge,
    check_relationship_api_assigns_check_post as check_relation,
    expand_relationship_api_assigns_expand_post as expand_object,
    list_edges_api_assigns_list_post as list_edges,
    revoke_user_to_org_api_assigns_revoke_post as revoke_edge,
)
from guard_post.api.azure_ad import (
    get_user_api_active_dir_get_user_get as get_user_oauth,
)

# from guard_post.models.http_validation_error import HTTPValidationError
# from guard_post.types import Response
from guard_post.api.orgs import (
    delete_api_orgs_delete_post as delete_orgs,
    list_items_api_orgs_list_get as list_orgs,
    sync_api_orgs_sync_post as sync_orgs,
)
from guard_post.api.sites import (
    delete_api_sites_delete_post as delete_sites,
    list_sites_api_sites_list_get as list_sites,
    sync_api_sites_sync_post as sync_sites,
)
from guard_post.api.users import (
    delete_api_users_delete_post as delete_users,
    list_items_api_users_list_get as list_users,
    sync_api_users_sync_post as sync_users,
)
from guard_post.client import Client
from guard_post.imports import logger

# User, Site, Org
from guard_post.models import (  # CreateSiteAttributes,
    CreateOrg,
    CreateSite,
    CreateUser,
    DeleteOrg,
    DeleteSite,
    DeleteUser,
    EdgeInput,
    ExpandInput,
    ListObjectsInputKey,
    Site as SiteInput,
)

# edge_input,
from guard_post.models.create_user_attributes import CreateUserAttributes
from guard_post.models.edge_keys import EdgeKeys
from guard_post.models.list_objects_input_key_key import ListObjectsInputKeyKey
from guard_post.models.pydantic_models import (
    Organization,
    Organization as OrganizationModel,
    Users,
    Users as UsersModel,
)
from guard_post.models.pydantic_models.relations import (
    EdgeInput as PyEdgeInput,
    EdgeKeys as PyEdgeKeys,
    ExpandInput as PyExpandInput,
)


class Path(abc.ABC):
    def __init__(self, client: "GuardPost") -> None:
        self.client = client

    @abc.abstractmethod
    def get(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def list(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def create_or_sync(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    def remove(self, *args, **kwargs) -> None:
        pass

    def class_name(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        client_repr = repr(self.client)

        return f"{self.class_name().title()}(client={client_repr[:20]} ...)"


class UserPath(Path):
    def get(self, *args, **kwargs) -> None:
        # Implementation for getting user
        logger.info("Calling organization get")
        # self.client.
        return self
        # logger.warning(f"{} in {self.class_name()}")

    def list(self, limit: int = 100) -> None:
        # Implementation for listing users
        return list_users.sync(client=self.client, limit=limit)

    def create_or_sync(
        self,
        *args,
        key: Optional[Dict[str, str]] = None,
        name: Optional[str] = None,
        site_id: Optional[int] = None,
        **kwargs,
    ) -> None:
        # Implementation for creating or syncing user
        key_input = key or kwargs.get("key", None) or {"test": "users", "type": "user"}
        # name_input = name or kwargs.get("name", None) or "test_site"
        # description = kwargs.get("description", None) or "test_org_descriptionssssss"
        # site_id = site_id or kwargs.get("site_id", None) or 4
        # logger.info(f"Calling organization create_or_sync with {key_input}")
        create_site = CreateUser(
            key=key_input,
            first_name="test_first_name",
            last_name="test_last_name",
            email=kwargs.get("email", None) or "kevin.hill@hussmann.com",
            phone=kwargs.get("phone", None) or "1234567890",
            attributes=CreateUserAttributes(),
            # name=name_input,
            # description=description,
            # site_id=site_id,
        )
        return sync_users.sync(client=self.client, json_body=create_site)

    # def create_or_sync_object(self, site: )

    def remove(self, key: dict = dict()) -> None:
        # Implementation for removing user
        if not key:
            raise ValueError("key is required")
        del_input = DeleteUser(key=key)
        return delete_users.sync(client=self.client, json_body=del_input)

    def add_groups(self, key: dict, groups: list = []) -> dict:
        # Implementation for adding groups to user
        return {
            "key": key,
            "groups": groups,
            "success": True,
        }

    def add_group(self, key: dict, group: str) -> dict:
        # Implementation for adding group to user
        group_list = [group]
        return self.add_groups(key=key, groups=group_list)

    def remove_groups(self, key: dict, groups: list = []) -> dict:
        # Implementation for removing groups from user
        return {
            "key": key,
            "groups": groups,
            "success": True,
        }

    def remove_group(self, key: dict, group: str) -> dict:
        # Implementation for removing group from user
        group_list = [group]
        return self.remove_groups(key=key, groups=group_list)

    def read_groups(self, key: dict) -> dict:
        # Implementation for reading groups from user
        # Will need to create httpx call to get groups. Make sure it works in the API first
        return {
            "key": key,
            "groups": ["admin", "member"],
            "success": True,
        }

    # def add_roles(self, key: dict, roles: list = []) -> dict:


class SitePath(Path):
    def get(self, *args, **kwargs) -> None:
        # Implementation for getting user
        logger.info("Calling organization get")
        # self.client.
        return self
        # logger.warning(f"{} in {self.class_name()}")

    def list(self, limit: int = 100) -> None:
        # Implementation for listing users
        return list_sites.sync(client=self.client, limit=limit)

    def create_or_sync(
        self,
        *args,
        key: Optional[Dict[str, str]] = None,
        name: Optional[str] = None,
        site_id: Optional[int] = None,
        **kwargs,
    ) -> None:
        # Implementation for creating or syncing user
        key_input = (
            key or kwargs.get("key", None) or {"test": "organization", "type": "org"}
        )
        name_input = name or kwargs.get("name", None) or "test_site"
        description = kwargs.get("description", None) or "test_org_descriptionssssss"
        site_id = site_id or kwargs.get("site_id", None) or 4
        # logger.info(f"Calling organization create_or_sync with {key_input}")
        create_site = CreateSite(
            key=key_input,
            name=name_input,
            description=description,
            site_id=site_id,
        )
        return sync_sites.sync(client=self.client, json_body=create_site)

    def remove(self, key: dict = dict()) -> None:
        # Implementation for removing user
        if not key:
            raise ValueError("key is required")
        del_input = DeleteSite(key=key)
        return delete_sites.sync(client=self.client, json_body=del_input)


class OrganizationPath(Path):
    def get(self, *args, **kwargs) -> None:
        # Implementation for getting user
        logger.info("Calling organization get")
        # self.client.
        return self
        # logger.warning(f"{} in {self.class_name()}")

    def list(self, limit: int = 100) -> None:
        # Implementation for listing users
        return list_orgs.sync(client=self.client, limit=limit)

    def create_or_sync(
        self,
        *args,
        key: Optional[Dict[str, str]] = None,
        name: Optional[str] = None,
        **kwargs,
    ) -> None:
        # Implementation for creating or syncing user
        key_input = (
            key or kwargs.get("key", None) or {"test": "organization", "type": "org"}
        )
        name_input = name or kwargs.get("name", None) or "test_org"
        descript = kwargs.get("description", None) or "test_org_descriptionssssss"
        # logger.info(f"Calling organization create_or_sync with {key_input}")
        create_org = CreateOrg(
            key=key_input,
            name=name_input,
            description=descript,
        )
        return sync_orgs.sync(client=self.client, json_body=create_org)

    def remove(self, key: dict = dict(), **kwargs) -> None:
        # Implementation for removing user
        if not key:
            raise ValueError("key is required")
        del_input = DeleteOrg(key=key)
        return delete_orgs.sync(client=self.client, json_body=del_input)


class GuardPost(Client):
    @property
    def users(self) -> "UserPath":
        return UserPath(client=self)

    @property
    def sites(self) -> Path:
        return SitePath(client=self)

    @property
    def orgs(self) -> Path:
        return OrganizationPath(client=self)

    @property
    def httpx_client(self):
        return self.get_httpx_client()

    @property
    def async_httpx_client(self):
        return self.get_async_httpx_client()

    def check(self, source: dict, relation: str, target: dict) -> bool:
        logger.info("Calling check")
        edge_input = EdgeInput(
            keys=EdgeKeys(start=source, end=target), relation=relation
        )
        response = check_relation.sync(client=self, json_body=edge_input)

        return response.get("allowed", False)

    def assign(self, source: dict, relation: str, target: dict) -> bool:
        edge_input = EdgeInput(
            keys=EdgeKeys(start=source, end=target), relation=relation
        )
        assigned = assign_edge.sync(client=self, json_body=edge_input)
        return assigned

    def revoke(self, source: dict, relation: str, target: dict) -> bool:
        edge_input = EdgeInput(
            keys=EdgeKeys(start=source, end=target), relation=relation
        )
        revoked = revoke_edge.sync(client=self, json_body=edge_input)
        return revoked

    def expand(self, source: dict, relation: str) -> bool:
        expand_input = ExpandInput(key=source, relation=relation)
        # logger.info(f"Calling expand with {expand_input}")
        response = expand_object.sync(client=self, json_body=expand_input)
        return response

    @logger.catch
    def resources(self, source: dict, relation: str, relation_type: str) -> bool:
        # expand_input = ExpandInput(key=source, relation=relation)
        list_obj_input = ListObjectsInputKey(
            key=source, relation=relation, type=relation_type
        )
        # logger.info(f"Calling expand with {expand_input}")
        response = list_edges.sync(client=self, json_body=list_obj_input)
        return response

    def oauth_token(self, token: str):
        response = get_user_oauth.sync(
            client=self.with_headers({"Authorization": f"Bearer {token}"})
        )
        return response

    def assign_user_roles(
        self,
        org: OrganizationModel,
        user: UsersModel,
        roles: list[Literal["owner", "admin", "member"]] = [],
    ):
        if not roles:
            raise AttributeError(
                "You need to provide groups/roles for the user and organization"
            )

        target_organization = self.orgs.create_or_sync(**org.get_storable())
        if (
            not isinstance(target_organization, dict)
            or "org" not in target_organization
        ):
            raise ValueError("We weren't able to create or retrieve the organization")
        org_key = target_organization["org"]["key"]

        source_user = self.users.create_or_sync(**user.get_storable())
        if not isinstance(source_user, dict) or "user" not in source_user:
            raise ValueError("Couldn't add or retrieve the user")
        user_key = source_user["user"]["key"]

        if not user_key or not org_key:
            raise AttributeError("We need both a user key and an organization key.")

        assignments = [self.assign(user_key, role, org_key) for role in roles]

        return assignments

    def get_user_roles(self, user: Users, org: Organization):
        endpoint = "/api/assigns/get_relationships"
        edge_keys = PyEdgeKeys(start=user.key, end=org.key)
        edge_input = PyEdgeInput(keys=edge_keys, relation="admin")
        # print(edge_input.model_dump(mode="json", warnings=False))
        response = self.httpx_client.post(
            endpoint, json=edge_input.model_dump(mode="json")
        )
        response.raise_for_status()
        resp_json = response.json()
        if "roles" in resp_json:
            return resp_json["roles"]
        return []


def main():
    # /api/active_dir/current_user
    guard = GuardPost(base_url="http://localhost:8000")
    # response = guard.oauth_token(
    #     "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjVCM25SeHRRN2ppOGVORGMzRnkwNUtmOTdaRSJ9.eyJhdWQiOiI1YWRmZGFlNC00MDY3LTQ2YTktOWRkNi1lYzdhMjk1ZmM5Y2QiLCJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vMmU4ZmY3NGQtMDM3Yy00NDA1LWI1MTktOGUwY2IzZGUxZTg1L3YyLjAiLCJpYXQiOjE3MDYyMjc1NTcsIm5iZiI6MTcwNjIyNzU1NywiZXhwIjoxNzA2MjMxNDU3LCJuYW1lIjoiSGlsbCwgS2V2aW4iLCJub25jZSI6ImMwOGE5M2E0LTY0MzgtNDA1Ny04Mzk3LTU1ZjgxMmJhNmU5ZSIsIm9pZCI6IjRkNTcyOWE2LTcxMzMtNDkwNi1iNTBmLTc4NWFlNzVmZjQzZSIsInByZWZlcnJlZF91c2VybmFtZSI6IktldmluLkhpbGxAaHVzc21hbm4uY29tIiwicHJvdl9kYXRhIjpbeyJQcm92IjoiZ2l0aHViLmNvbSIsIkF0Ijp0cnVlLCJBbHRzZWNpZCI6IjI0MDMyNDAiLCJBY2Nlc3NUb2tlbiI6bnVsbH1dLCJyaCI6IjAuQVRjQVRmZVBMbndEQlVTMUdZNE1zOTRlaGVUYTMxcG5RS2xHbmRic2VpbGZ5YzAzQUlJLiIsInN1YiI6IlpKaEZjVzFIcFljblI1cG9ZMTNEUURBcUJ3WVdObi1vZHBxUVpPM3l0OGsiLCJ0aWQiOiIyZThmZjc0ZC0wMzdjLTQ0MDUtYjUxOS04ZTBjYjNkZTFlODUiLCJ1dGkiOiJua2s3M3dxWkZFYXQ1QlhhWkFnY0FRIiwidmVyIjoiMi4wIn0.V01bVZZyFZD1pmNEuo6Tr8xLm0KasdSCHyfodOo8CKh5CfKJD7QffueD9Op3A5i_jpiAyDYlDc9UzDmzp-on8lcLYMKMY4kKwWYpRV4_ucZUWVjWEnsYx0Gfl5kte6XuO01sGAy8fSvVugCn89kE9UxU0g3bVzERJDDTXut5GSlj90SugE3Rqft5mPd-y2IOJEaLsp3ZuZyS8xtdXMs57W67UWmuE0C6dhQsvh5ivuTJE467ky19SUbJnIpYTMicdXiPluMnp6uymJKXTuk0u8Prh-pmgObOCfyNEACNaOJHAH4aGgraad09dPUDs8aOLh5rlvuSiOWsHzwo9YXPww"
    # )
    # dtz.debug(response)
    logger.info("Hello, world!!!!!!!!!!!!!!! I LOVE CANDY!!!!!!!")
    logger.success("I am a success message")
    # logger.debug(guard.users)
    org_key = {"test": "organization", "type": "org", "name": "simple_org"}
    org_key2 = {"test": "organization", "type": "org", "name": "simple_org2"}
    site_key = {"test": "site", "type": "site", "name": "simple_site"}
    user_key = {
        "test": "user",
        "type": "user",
        "name": "simple_user",
        "email": "monika@hussmann.com",
    }
    # logger.debug(site_key)
    # logger.debug(user_key)

    created_org = guard.orgs.create_or_sync(
        key=org_key,
        name="monika's org",
        description="monika's org description",
    )
    logger.warning(created_org)
    created_org2 = guard.orgs.create_or_sync(
        key=org_key2,
        name="kevin's org",
        description="kevin's org description",
    )
    logger.error(created_org2)
    logger.warning(created_org2)
    # dtz.debug(guard.orgs.list(limit=1))
    # # logger.critical(guard.orgs.remove(key=org_key))
    # dtz.debug(guard.orgs.list(limit=1))
    created_site = guard.sites.create_or_sync(
        key=site_key,
        name="monika's site",
        description="monika's site description",
        site_id=44,
    )
    logger.debug(created_site)

    # dtz.debug(guard.sites.list(limit=1))
    # # logger.critical(
    # #     guard.sites.remove(key={"test": "site", "type": "site", "name": "simple_site"})
    # # )

    # dtz.debug(guard.users.list(limit=1))
    created_user = guard.users.create_or_sync(
        key=user_key,
        name="monika's user",
        description="monika's user description",
        phone="+491761234567",
        email="monika@hussmann.com",
    )
    added_groups = guard.users.add_groups(
        key=user_key,
        groups=["admin", "member"],
    )

    logger.warning(created_user)
    # dtz.debug(guard.users.list(limit=1))
    revoked_original = guard.revoke(user_key, "admin", org_key)
    logger.success(revoked_original)
    org_assigned = guard.assign(org_key2, "parent", org_key)
    assigned = guard.assign(user_key, "admin", org_key2)
    logger.success(assigned)
    allowed = guard.check(user_key, "admin", org_key)
    allowed = guard.check(user_key, "can_create_org", org_key)
    allowed = guard.check(user_key, "can_add_member", org_key)
    logger.debug(allowed)
    assert allowed, "check failed"

    expanded = guard.expand(org_key2, "admin")
    logger.info(expanded)
    resources = guard.resources(user_key, "member", "org")
    dtz.debug(resources)


if __name__ == "__main__":
    main()
