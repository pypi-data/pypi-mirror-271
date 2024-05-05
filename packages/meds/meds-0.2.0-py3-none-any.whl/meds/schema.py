import datetime
from typing import Any, List, Mapping, Optional

import pyarrow as pa
from typing_extensions import NotRequired, TypedDict

# Medical Event Data Standard consists of three main components:
# 1. A patient data schema
# 2. A label schema
# 3. A dataset metadata schema.
#
# Patient data and labels are specified using pyarrow. Dataset metadata is specified using JSON.

# We also provide TypedDict Python type signatures for these schemas.

############################################################

# The patient data schema.

# We define some codes for particularly important events
birth_code = "SNOMED/184099003"
death_code = "SNOMED/419620001"

def patient_schema(per_event_properties_schema=pa.null()):
    # Return a patient schema with a particular per event metadata subschema
    event = pa.struct(
        [
            ("time", pa.timestamp("us")), # Static events will have a null timestamp
            ("code", pa.string()),
            ("text_value", pa.string()),
            ("numeric_value", pa.float32()),
            ("datetime_value", pa.timestamp("us")),
            ("properties", per_event_properties_schema),
        ]
    )

    patient = pa.schema(
        [
            ("patient_id", pa.int64()),
            ("events", pa.list_(event)),  # Require ordered by time, nulls must be first
        ]
    )

    return patient


# Python types for the above schema

Event = TypedDict(
    "Event",
    {
        "time": NotRequired[datetime.datetime],
        "code": str,
        "text_value": NotRequired[str],
        "numeric_value": NotRequired[float],
        "datetime_value": NotRequired[datetime.datetime],
        "properties": NotRequired[Any],
    },
)

Patient = TypedDict("Patient", {"patient_id": int, "events": List[Event]})

############################################################

# The label schema.

label = pa.schema(
    [
        ("patient_id", pa.int64()),
        ("prediction_time", pa.timestamp("us")),
        ("boolean_value", pa.bool_()),
        ("integer_value", pa.int64()),
        ("float_value", pa.float64()),
        ("categorical_value", pa.string()),
    ]
)

# Python types for the above schema

Label = TypedDict("Label", {
    "patient_id": int, 
    "prediction_time": datetime.datetime, 
    "boolean_value": Optional[bool],
    "integer_value" : Optional[int],
    "float_value" : Optional[float],
    "categorical_value" : Optional[str],
})

############################################################

# The dataset metadata schema.
# This is a JSON schema.
# This data should be stored in metadata.json within the dataset folder.

code_metadata_entry = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "parent_codes": {"type": "array", "items": {"type": "string"}},
    },
}

code_metadata = {
    "type": "object",
    "additionalProperties": code_metadata_entry,
}

dataset_metadata = {
    "type": "object",
    "properties": {
        "dataset_name": {"type": "string"},
        "dataset_version": {"type": "string"},
        "etl_name": {"type": "string"},
        "etl_version": {"type": "string"},
        "code_metadata": code_metadata,
    },
}

# Python types for the above schema

CodeMetadataEntry = TypedDict("CodeMetadataEntry", {"description": str, "parent_codes": List[str]})
CodeMetadata = Mapping[str, CodeMetadataEntry]
DatasetMetadata = TypedDict(
    "DatasetMetadata",
    {
        "dataset_name": NotRequired[str],
        "dataset_version": NotRequired[str],
        "etl_name": NotRequired[str],
        "etl_version": NotRequired[str],
        "code_metadata": NotRequired[CodeMetadata],
    },
)
