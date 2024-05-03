from pyspark.sql.types import StructType, TimestampType


def handle_pyspark_timestamp_in_schema(pyspark_schema: StructType) -> StructType:
    """
    Recursively traverses a PySpark schema and converts fields with a 'format' metadata key
    and value of 'date-time' or 'date' to TimestampType.

    Args:
        pyspark_schema (StructType): The PySpark schema to be processed.

    Returns:
        StructType: The updated PySpark schema with converted field types.
    """

    def is_struct_type(field):
        return field.simpleString()[:6] == "struct"

    def is_array_type(field):
        return field.simpleString()[:5] == "array"

    # for each field in schema
    for field in pyspark_schema.fields:
        field_metadata = field.metadata
        if is_struct_type(field.dataType):
            handle_pyspark_timestamp_in_schema(field.dataType)  # type: ignore
        elif is_array_type(field.dataType):
            if is_struct_type(field.dataType.elementType):  # type: ignore
                handle_pyspark_timestamp_in_schema(field.dataType.elementType)  # type: ignore
        # if 'format' is in field metadata key and the value is 'date-time' or 'date'
        # convert field type to TimestampType
        elif "format" in field_metadata.keys():
            field_format = field_metadata["format"]
            if field_format in ("date-time", "date"):
                field.dataType = TimestampType()
    return pyspark_schema
