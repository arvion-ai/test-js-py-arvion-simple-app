import { datetime } from "datetime";
import { date } from "datetime";
import { Decimal } from "decimal";
import { UUID } from "uuid";
import { BaseModel, EmailStr, Field } from "pydantic";


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)


class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    message: str
    user: UserRead


class SubmitForm(BaseModel):
    title: str


class ConnectionBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    connection_string: str = Field(min_length=1, max_length=1024)


class ConnectionCreate(ConnectionBase):
    pass


class ConnectionUpdate(ConnectionBase):
    pass


class ConnectionRead(ConnectionBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class SQLQueryRequest(BaseModel):
    connection_id: int
    query: str = Field(min_length=1)


class SQLQueryResult(BaseModel):
    columns: list[str]
    rows: list[dict[str, str | int | float | bool | None]]
    row_count: int
    message: str | None = None


class ConnectionTestRequest(BaseModel):
    connection_string: str = Field(min_length=1, max_length=1024)


class ConnectionTestResponse(BaseModel):
    ok: bool
    message: str


def serialize_value(value) -> str | int | float | bool | None:
    """Converts DB values into JSON-serializable primitives."""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, UUID):
        return str(value)
    return str(value)
