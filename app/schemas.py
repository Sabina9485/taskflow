from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Role = Literal["operator", "admin"]
Status = Literal["open", "in_progress", "done"]
Priority = Literal["low", "medium", "high"]


class UserBase(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=255)
    role: Role = "operator"


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    display_name: str | None = Field(default=None, min_length=1, max_length=255)
    role: Role | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class LabelBase(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    color: str = Field(default="#6b7280", pattern=r"^#[0-9a-fA-F]{6}$")


class LabelCreate(LabelBase):
    pass


class LabelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=64)
    color: str | None = Field(default=None, pattern=r"^#[0-9a-fA-F]{6}$")


class LabelRead(LabelBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TaskBase(BaseModel):
    project_id: int
    assignee_id: int | None = None
    label_id: int | None = None
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: Status = "open"
    priority: Priority = "medium"


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    project_id: int | None = None
    assignee_id: int | None = None
    label_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class CommentBase(BaseModel):
    task_id: int
    author_id: int
    body: str = Field(min_length=1)


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    body: str = Field(min_length=1)


class CommentRead(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
