from common.exceptions.parameter_exception import ParameterException


def validate_json_structure(data):
    required_fields = {
        "zip_url": str,
        "model_type": str,
        "confidence_threshold": (float, int, None),
        "word": str,
    }

    for field, field_type in required_fields.items():
        if field not in data:
            raise ParameterException(f"The parameter {field} do")