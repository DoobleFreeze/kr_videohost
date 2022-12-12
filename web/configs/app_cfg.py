# Конфигурация документации OpenAPI v.3.0.3 (Swagger)

template = {
    'openapi': '3.0.3',
    "info": {
        "title": "Video hosting API",
        "description": "KR Osipov N. RTU MIREA",
    },
    "components": {
        "schemas": {
            "NotFound": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Page not found."
                    }
                },
                "required": [
                    "error"
                ]
            },
            "InvalidRequest": {
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "example": "Invalid request"
                    }
                },
                "required": [
                    "error"
                ]
            },
            "PostSuccess": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": "string",
                        "example": "Success"
                    }
                },
                "required": [
                    "result"
                ]
            },
            "register": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "Osipov N."
                    },
                    "password": {
                        "type": "string",
                        "example": "qwerty"
                    },
                },
                "required": [
                    "name",
                    "password",
                ]
            },
        },
    },
    "paths": {
        "/register": {
            "post": {
                "summary": "Register new user",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": '#/components/schemas/register'
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Data received successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/PostSuccess'
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "invalid request. The server failed to recognize the request due to a syntax error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/InvalidRequest'
                                }
                            }
                        }
                    },
                }
            },
        },
        "/auth": {
            "post": {
                "summary": "Get API key",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": '#/components/schemas/register'
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Data received successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/PostSuccess'
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "invalid request. The server failed to recognize the request due to a syntax error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/InvalidRequest'
                                }
                            }
                        }
                    },
                }
            },
        },
        "/add_video/{key}": {
            "post": {
                "summary": "Upload new video",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": '#/components/schemas/register'
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Data received successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/PostSuccess'
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "invalid request. The server failed to recognize the request due to a syntax error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/InvalidRequest'
                                }
                            }
                        }
                    },
                }
            },
        },
        "/get_video/{file_path}": {
            "get": {
                "summary": "Get video with file_path",
                "parameters": [{
                    "in": "path",
                    "name": "uid",
                    "required": True,
                    "description": "ID",
                    "schema": {
                        "type": "integer",
                        "example": 0
                    }
                }],
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/GetContact'
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "invalid request. The server failed to recognize the request due to a syntax error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/InvalidRequest'
                                }
                            }
                        }
                    },
                }
            },
        },
        "/get_all_videos": {
            "get": {
                "summary": "Get all video",
                "parameters": [{
                    "in": "path",
                    "name": "uid",
                    "required": True,
                    "description": "ID",
                    "schema": {
                        "type": "integer",
                        "example": 0
                    }
                }],
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/GetContact'
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "invalid request. The server failed to recognize the request due to a syntax error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/InvalidRequest'
                                }
                            }
                        }
                    },
                }
            },
        },
        "/get_user_videos/{user_name}": {
            "get": {
                "summary": "Get all video by user",
                "parameters": [{
                    "in": "path",
                    "name": "uid",
                    "required": True,
                    "description": "ID",
                    "schema": {
                        "type": "integer",
                        "example": 0
                    }
                }],
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/GetContact'
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "invalid request. The server failed to recognize the request due to a syntax error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/InvalidRequest'
                                }
                            }
                        }
                    },
                }
            },
        },
        "/get_users": {
            "get": {
                "summary": "Get all users",
                "parameters": [{
                    "in": "path",
                    "name": "uid",
                    "required": True,
                    "description": "ID",
                    "schema": {
                        "type": "integer",
                        "example": 0
                    }
                }],
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/GetContact'
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "invalid request. The server failed to recognize the request due to a syntax error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/InvalidRequest'
                                }
                            }
                        }
                    },
                }
            },
        },
        "/search_video/{search_phrase}": {
            "get": {
                "summary": "Get video with phrase",
                "parameters": [{
                    "in": "path",
                    "name": "uid",
                    "required": True,
                    "description": "ID",
                    "schema": {
                        "type": "integer",
                        "example": 0
                    }
                }],
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/GetContact'
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "invalid request. The server failed to recognize the request due to a syntax error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/InvalidRequest'
                                }
                            }
                        }
                    },
                }
            },
        },
        "/delete_video/{file_path}/{key}": {
            "delete": {
                "summary": "Delete video",
                "parameters": [{
                    "in": "path",
                    "name": "uid",
                    "required": True,
                    "description": "ID",
                    "schema": {
                        "type": "integer",
                        "example": 0
                    }
                }],
                "responses": {
                    "200": {
                        "description": "OK",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/PostSuccess'
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "invalid request. The server failed to recognize the request due to a syntax error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": '#/components/schemas/InvalidRequest'
                                }
                            }
                        }
                    },
                }
            },
        },
    }
}
