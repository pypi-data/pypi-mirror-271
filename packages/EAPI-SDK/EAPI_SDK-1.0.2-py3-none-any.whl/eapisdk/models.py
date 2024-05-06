from dataclasses import dataclass
from typing import List, Optional

@dataclass
class User:
    id: int
    username: str
    email: str
    created_at: str

@dataclass
class ErrorResponse:
    error_code: int
    message: str

@dataclass
class PaginatedResponse:
    total_count: int
    items_per_page: int
    current_page: int
    results: List[User]

# 示例：如果某个OpenAPI接口返回的是用户列表
def parse_user_response(json_data: dict) -> List[User]:
    return [User(**user_data) for user_data in json_data.get('users', [])]

# 示例：如果某个OpenAPI接口返回的是分页用户数据
def parse_paginated_user_response(json_data: dict) -> PaginatedResponse:
    return PaginatedResponse(
        total_count=json_data['totalCount'],
        items_per_page=json_data['itemsPerPage'],
        current_page=json_data['currentPage'],
        results=[User(**user_data) for user_data in json_data['results']],
    )