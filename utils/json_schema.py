from jsonschema.validators import validate

if __name__ == "__main__":
    data = {
        "name": "Tom",
        "age": 18,
        "vip": True
    }
    """type字段类型判断"""
    schema_0 = {
        "title": "name必须是字符串",
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            },
            "age": {
                "type": "integer"
            },
            "vip": {
                "type": "boolean"
            },
            "friends": {
                "type": "array"
            }
        }
    }
    """必填字段校验exist"""
    schema_1 = {
        "type": "object",
        "title": "要求字段name,age必须存在",
        "required": ["name", "age"]
    }
    data = {
        "id": 1
    }
    """
    要求：
    必须有 id
    id 是整数"""
    schema = {
        "type": "object",
        "required": ["id"],
        "properties": {
            "id": {
                "type": "integer"
            }
        }
    }
    data = {
        "id": 100,
        "name": "地图1",
        "enable": True
    }
    """
    1. 整体必须是 object
    2. id 必须存在，类型 integer
    3. name 必须存在，类型 string
    4. enable 必须存在，类型 boolean
    """
    schema = {
        "type": "object",
        "required": ["id", "name", "enable"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "enable": {"type": "boolean"}
        }

    }
    """描述数组"""
    data = {
        "maps": [
            {
                "id": 1,
                "name": "map1"
            },
            {
                "id": 2,
                "name": "map2"
            }
        ]
    }
    """要求：
    1. maps 必须存在
    2. maps 是数组
    3. 每个元素必须包含：
    - id integer
    - name string"""
    schema = {
        "type": "object",
        "required": [
            "maps"
        ],
        "properties": {
            "maps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "name": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }

    data = {
        "name": "develop",
        "commit": {
            "sha": "abc123"
        },
        "protected": True
    }
    """
    要求：
    1. name 必须存在
    2. commit 必须是对象
    3. commit.sha 必须是字符串
    4. protected 必须是 boolean
    """
    schema = {
        "type": "object",
        "required": ["name"],
        "properties": {
            "commit": {
                "type": "object",
                "properties": {
                    "sha": {
                        "type": "string"
                    }
                }
            },
            "protected": {
                "type": "boolean"
            }
        }
    }
    data = {
        "username": "tom"
    }
    """要求：
    1. 整体必须是 object
    2. 必须存在 username
    3. username 必须是字符串
    4. username 长度：
    - 最少 3 个字符
    - 最多 10 个字符
    """
    schema = {
        "type": "object",
        "required": ["username"],
        "properties": {
            "username": {
                "type": "string",
                "minLength": 3,
                "maxLength": 10
            }
        }
    }
    data = {
        "age": 25
    }
    """
    要求：
    1. age 必须存在
    2. age 必须是整数
    3. 年龄范围：18 <= age <= 60
    """
    schema = {
        "type": "object",
        "required": ["age"],
        "properties": {
            "age": {
                "type": "integer",
                "minimum": 18,
                "maximum": 60
            }
        }
    }
    data = {
        "status": "running"
    }
    """
    状态只能running stopped error
    """
    schema = {
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "enum": ["running", "stopped", "error"]
            }
        }
    }
    data = {
        "tags": [
            "python",
            "pytest",
            "api"
        ]
    }
    """要求：
    数组基础 array + items
    1. tags 必须存在
    2. tags 必须是数组
    3. 数组每个元素必须是字符串
    """
    schema = {
        "type": "object",
        "required": ["tags"],
        "properties": {
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        }
    }
    """数组里面是对象（接口最常见）"""
    data = {
        "users": [
            {
                "id": 1,
                "name": "Tom"
            },
            {
                "id": 2,
                "name": "Jack"
            }
        ]
    }
    """要求：
    users:
    - 必须存在
    - 是数组
    每个数组元素：
    - 必须是 object
    - 必须有 id
    - 必须有 name
    id:
    - integer
    name:
    - string
    """
    schema = {
        "type": "object",
        "required": ["users"],
        "properties": {
            "users": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "name"],
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"}
                    }
                }
            }
        }
    }


    print(validate(instance=data, schema=schema))
