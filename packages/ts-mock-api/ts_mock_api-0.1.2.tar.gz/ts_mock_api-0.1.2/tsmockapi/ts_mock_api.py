import json
import random

from tsinterface.ts_interface import TsInterface


class TsMockAPI(TsInterface):

    @staticmethod
    def load() -> str:
        val = {
            "message": "Mock interface validated",
            "loaded": True
        } if bool(random.getrandbits(1)) else {
            "message": "Mock interface validation error",
            "loaded": False
        }

        return json.dumps(val)

        pass

    @staticmethod
    def predict(json_input) -> str:
        return json.dumps(
            {
                "detections": [
                    {
                        "image": "ABCDEFGHIJKLMNOPQRSTUV",
                        "classes": [
                            {
                                "label": "ABCDEFGHIJKLMNO",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDEFGHIJKLMNOPQRSTU",
                                "probability": 0.0
                            }
                        ],
                        "bbox": {
                            "x": 0.0,
                            "y": 0.0,
                            "width": 0.0,
                            "height": 0.0
                        }
                    },
                    {
                        "image": "ABCDEFGHIJKLMNOPQRSTUVWXY",
                        "classes": [
                            {
                                "label": "ABCDEFGHIJKLMNO",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDE",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDEFGHIJKLMNOPQRSTUVWXYZAB",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                "probability": 0.0
                            }
                        ],
                        "bbox": {
                            "x": 0.0,
                            "y": 0.0,
                            "width": 0.0,
                            "height": 0.0
                        }
                    },
                    {
                        "image": "ABCDEFGHIJKLMNOP",
                        "classes": [],
                        "bbox": {
                            "x": 0.0,
                            "y": 0.0,
                            "width": 0.0,
                            "height": 0.0
                        }
                    },
                    {
                        "image": "ABCDEFGHIJKLMNOPQRSTUVWXYZABC",
                        "classes": [
                            {
                                "label": "ABCDEFGHIJKLMNOPQRSTUVWXYZA",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDEFGHIJKLMNOPQRSTUVW",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDEFGHIJKLMNO",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDEFGHIJKLMNOP",
                                "probability": 0.0
                            }
                        ],
                        "bbox": {
                            "x": 0.0,
                            "y": 0.0,
                            "width": 0.0,
                            "height": 0.0
                        }
                    },
                    {
                        "image": "ABCDEFGHIJKLMNOPQRST",
                        "classes": [
                            {
                                "label": "ABCDEFGHIJKLMNOPQR",
                                "probability": 0.0
                            }
                        ],
                        "bbox": {
                            "x": 0.0,
                            "y": 0.0,
                            "width": 0.0,
                            "height": 0.0
                        }
                    },
                    {
                        "image": "ABCDEFGHIJKLMNOP",
                        "classes": [
                            {
                                "label": "ABCDEFGHIJKLMNOPQRSTUVWXYZA",
                                "probability": 0.0
                            }
                        ],
                        "bbox": {
                            "x": 0.0,
                            "y": 0.0,
                            "width": 0.0,
                            "height": 0.0
                        }
                    },
                    {
                        "image": "ABCDEFGHIJKLMNOPQRS",
                        "classes": [],
                        "bbox": {
                            "x": 0.0,
                            "y": 0.0,
                            "width": 0.0,
                            "height": 0.0
                        }
                    },
                    {
                        "image": "ABCDEFGHIJKLMNOP",
                        "classes": [
                            {
                                "label": "ABCDEFGHIJKLMNO",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDEFGHIJKLMNOPQRSTUVWX",
                                "probability": 0.0
                            },
                            {
                                "label": "ABCDEFGHIJKLMNOPQR",
                                "probability": 0.0
                            }
                        ],
                        "bbox": {
                            "x": 0.0,
                            "y": 0.0,
                            "width": 0.0,
                            "height": 0.0
                        }
                    }
                ]
            }
        )

    @staticmethod
    def validate() -> str:
        val = {
            "message": "Mock interface validated",
            "validated": True
        } if bool(random.getrandbits(1)) else {
            "message": "Mock interface validation error",
            "validated": False
        }
        return json.dumps(val)


if __name__ == '__main__':
    ts = TsMockAPI()
    ts.load()
    ts.validate()
    input_json = json.dumps({})
    output = ts.predict('test')
    print(output)
