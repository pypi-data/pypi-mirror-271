import os
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from supabase import create_client, Client



def get_supabase_client():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    client: Client = create_client(url, key)

    return client


sb_client = get_supabase_client()


def sb_table(model):
    if not isinstance(model, str) and hasattr(model, '__tablename__'):
        table_name = model.__tablename__
    else:
        table_name = model

    return sb_client.table(table_name)


def get_current_month_range():
    now = datetime.now()
    first_day_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_of_month = now.replace(hour=23, minute=59, second=59, microsecond=0)
    
    return first_day_of_month, last_day_of_month


def get_model_field_names(model_cls: type, related_name: str = None) -> List[str]:
    fields = []
    for field_name, field_obj in model_cls.__fields__.items():
        if related_name and field_name != related_name:
            continue        

        if field_obj.json_schema_extra and "related_name" in field_obj.json_schema_extra:
            extra_related_name = field_obj.json_schema_extra.get("related_name")
            nested_fields = [f"{field_name}({subfield})" for subfield in get_model_field_names(field_obj.annotation, related_name=extra_related_name)]
            fields.extend(nested_fields)
        else:
            fields.append(field_name)
    return fields


class BaseService:
    model = None

    @property
    def table(self):
        model_fields = get_model_field_names(self.model)
        return sb_table(self.model).select(", ".join(model_fields), count="exact")

    def execute(self):
        data = self.table.execute()
        return [self.model(**dt) for dt in data.data]

    def all(self):
        return self.execute()