from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, computed_field


class Site(BaseModel):
    name: str
    description: str | None = None
    site_id: int

    @computed_field
    def key(self) -> dict:
        return {"site_id": self.site_id, "type": "site"}

    def get_storable(self):
        item = self.model_dump(mode="json")
        key = item.pop("key", None)
        if not key:
            item["key"] = {"site_id": item["site_id"], "type": "site"}
            return item
        if isinstance(key, dict):
            key["type"] = "site"
            key["site_id"] = item["site_id"]
            item["key"] = key
        return item


class Users(BaseModel):
    key: dict | str
    first_name: str
    last_name: str
    email: str
    phone: str | None
    attributes: dict

    def get_storable(self):
        item = self.model_dump(mode="json")
        key = item.pop("key", None)
        if not key:
            item["key"] = {"email": item["email"], "type": "user"}
            return item
        if isinstance(key, dict):
            if "test" in key:
                key.pop("test", None)
            key["type"] = "user"
            key["email"] = item["email"]
            item["key"] = key
        return item


class Organization(BaseModel):
    org_id: int | None = Field(None, alias="ID")
    # key: dict | str | None = None
    name: str
    description: str | None = None
    attributes: dict = {}
    model_config: ConfigDict = ConfigDict(cache_strings="all")

    @computed_field
    @property
    def key(self) -> dict:
        return {"name": self.name, "type": "org"}

    def get_storable(self):
        item = self.model_dump(mode="json")
        key = item.pop("key", None)
        if not key:
            item["key"] = {"name": self.name, "type": "org"}
            return item
        if isinstance(key, dict):
            if "type" not in key:
                key["type"] = "org"
            if "name" not in key:
                key["name"] = self.name
            item["key"] = key
        return item

    # groups: list[str] = ["ADMIN", "GUEST"]
