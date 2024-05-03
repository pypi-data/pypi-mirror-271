import inspect
import json
import os
from datetime import datetime
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel, field_validator, model_validator
from pyspark.sql.dataframe import DataFrame

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))


DATE_FORMATTER = {
    "year": lambda x: str(x.year),
    "month": lambda x: str(x.month).zfill(2),
    "day": lambda x: str(x.day).zfill(2),
}


class FileType(str, Enum):
    """
    Represents the type of file used in data pipelines.

    Attributes:
        CSV (str): Represents a CSV file.
        JSON (str): Represents a JSON file.
        PARQUET (str): Represents a Parquet file.
    """

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"


class Layer(str, Enum):
    """
    Enum class representing different layers in a data pipeline.

    The available layers are:
    - LANDING: The landing layer where raw data is initially ingested.
    - RAW: The raw layer where the ingested data is stored without any transformations.
    - TRUSTED: The trusted layer where the data is cleaned and validated.
    - ANALYTICS: The analytics layer where the data is transformed and aggregated for analysis.
    """

    LANDING = "landing"
    RAW = "raw"
    TRUSTED = "trusted"
    ANALYTICS = "analytics"


class Env(str, Enum):
    """
    Enumeration representing different environments.

    Attributes:
        DEV (str): Development environment.
        PRD (str): Production environment.
    """

    DEV = "dev"
    PRD = "prd"


class DatePartition(str, Enum):
    """
    Enum representing different types of date partitions.

    Attributes:
        PART_YEAR (str): Represents a partition by year, with name "part_year".
        PART_MONTH (str): Represents a partition by month, with name "part_month".
        PART_DAY (str): Represents a partition by day, with name "part_day".
        YEAR (str): Represents a partition by year, with name "year".
        MONTH (str): Represents a partition by month, with name "month".
        DAY (str): Represents a partition by day, with name "day".
    """

    PART_YEAR = "part_year"
    PART_MONTH = "part_month"
    PART_DAY = "part_day"
    YEAR = "year"
    MONTH = "month"
    DAY = "day"


class FnKind(str, Enum):
    """
    Enumeration representing the kind of function.

    Attributes:
        SINGLE (str): Represents a single function.
        BATCH (str): Represents a batch function.
    """

    SINGLE = "single"
    BATCH = "batch"


class BaseModelJsonDumps(BaseModel):
    """A base model class that extends Pydantic's BaseModel by overriding the __str__ to pretty print the model as JSON."""

    def __str__(self):
        return json.dumps(self.model_dump(), indent=2, default=str)


class AWSCredentials(BaseModelJsonDumps):
    """
    Represents AWS credentials required for authentication.

    Attributes:
        aws_access_key_id (str): The AWS access key ID.
        aws_secret_access_key (str): The AWS secret access key.
    """

    aws_access_key_id: str
    aws_secret_access_key: str


class S3BucketParams(BaseModelJsonDumps):
    """
    Represents the parameters for an S3 bucket, most specially the bucket name.

    Attributes:
        env (Env): The environment. Must be one of "Env.DEV" or "Env.PRD".
        layer (Optional[Layer]): The layer (optional).
        ng_prefix (str): The NG prefix. Defaults to "ng".
        bucket_name (Optional[str]): The bucket name (optional). If not provided, it will be generated based on the layer, environment, and NG prefix.
    """

    env: Env
    layer: Optional[Layer] = None
    ng_prefix: str = "ng"
    bucket_name: Optional[str] = None

    @model_validator(mode="before")
    def set_bucket_name_if_not_provided(cls, data):
        layer = data.get("layer").value if data.get("layer") is not None else None
        env = data.get("env").value
        ng_prefix = data.get("ng_prefix", "ng")
        bucket_name = data.get("bucket_name")

        if bucket_name is None:
            if layer is None:
                raise ValueError(
                    "'layer' must be provided if 'bucket_name' is not provided"
                )
            data["bucket_name"] = f"{ng_prefix}-datalake-{layer}-{env}"

        return data


class S3ReadJsonParams(BaseModelJsonDumps):
    """
    Represents the parameters for reading a JSON file from an S3 bucket.

    Attributes:
        bucket_params (S3BucketParams): The parameters for the S3 bucket.
        path (str): The path to the JSON file in the S3 bucket.

    Methods:
        strip_slashes(cls, v: str) -> str: A class method that strips leading and trailing slashes from the path.
        ensure_path_to_file_has_json_extension(cls, v: str) -> str: A class method that ensures the path has a '.json' extension.

    Raises:
        ValueError: If the path does not have a '.json' extension.

    """

    bucket_params: S3BucketParams
    path: str

    @field_validator("path")
    @classmethod
    def strip_slashes(cls, v: str) -> str:
        return v.strip("/")

    @field_validator("path")
    @classmethod
    def ensure_path_to_file_has_json_extension(cls, v: str) -> str:
        if not v.endswith(".json"):
            raise ValueError(
                f"For S3 schema, 'path' must have a '.json' extension. Received path: '{v}'"
            )

        return v


class DataFrameReadWriteParams(BaseModelJsonDumps):
    """
    Represents the parameters for reading and writing a DataFrame.

    Attributes:
        bucket_params (S3BucketParams): The parameters for the S3 bucket.
        specific_path (Optional[Union[List[str], str]]): The specific path to the data within the bucket.
        path_to_dataframe_root (Optional[str]): The path to the root folder of the DataFrame within the bucket.
        file_type (FileType): The type of file to read or write.
        processing_date (Union[List[datetime], datetime, Literal["{{processing_date}}"], Literal["{{processing_date_previous}}"]]): The processing date or dates to use for partitioning.
        processing_date_partitions (Optional[List[DatePartition]]): The list of date partitions to use for filtering.
        processing_date_partitions_first (bool): Flag indicating whether to process date partitions first.
        column_partitions (Optional[List[str]]): The list of column partitions to use for filtering.
    """
    bucket_params: S3BucketParams
    specific_path: Optional[Union[List[str], str]] = None
    path_to_dataframe_root: Optional[str] = None
    file_type: FileType
    processing_date: Union[
        List[datetime],
        datetime,
        Literal["{{processing_date}}"],
        Literal["{{processing_date_previous}}"],
    ] = "{{processing_date}}"
    processing_date_partitions: Optional[List[DatePartition]] = None
    processing_date_partitions_first: bool = True
    column_partitions: Optional[List[str]] = None

    @model_validator(mode="before")
    def xor_specific_path_and_path_to_dataframe_root(cls, data):
        """
        Validates that 'specific_path' and 'path_to_dataframe_root' are not passed together.

        Args:
            data (dict): The input data.

        Raises:
            ValueError: If 'specific_path' and 'path_to_dataframe_root' are passed together.

        Returns:
            dict: The validated data.
        """
        specific_path = data.get("specific_path")
        path_to_dataframe_root = data.get("path_to_dataframe_root")

        if specific_path is not None and path_to_dataframe_root is not None:
            raise ValueError(
                "'specific_path' and 'path_to_dataframe_root' cannot be passed together"
            )

        if specific_path is None and path_to_dataframe_root is None:
            raise ValueError(
                "Either 'specific_path' or 'path_to_dataframe_root' should be passed"
            )

        return data

    @field_validator("path_to_dataframe_root", "specific_path")
    def strip_slashes(cls, v: Union[str, List[str]]) -> str:
        """
        Strips leading and trailing slashes from the input string.

        Args:
            v (str): The input string.

        Returns:
            str: The input string with leading and trailing slashes stripped.
        """
        if v is not None:
            if isinstance(v, list):
                return [x.strip("/") for x in v] # type: ignore
            else:
                return v.strip("/")

    @field_validator("path_to_dataframe_root")
    def ensure_dataframe_root_parent_folder(cls, v: str) -> str:
        """
        Ensures that 'path_to_dataframe_root' has at least one parent folder inside the bucket.

        Args:
            v (str): The input string.

        Raises:
            ValueError: If 'path_to_dataframe_root' does not have at least one parent folder.

        Returns:
            str: The input string.
        """
        if v is not None and "/" not in v:
            raise ValueError(
                f"'path_to_dataframe_root' should have at least one parent folder inside the bucket. Ensure there is at least one slash ('/') in the path. Received path: '{v}'"
            )

        return v


class InputDataFrameParams(BaseModelJsonDumps):
    """
    Represents the parameters for an input DataFrame.

    Attributes:
        pyspark_schema_struct (Optional[Dict[str, Any]]): The schema of the input DataFrame in PySpark struct format.
        s3_schema_path_params (Optional[S3ReadJsonParams]): The parameters for reading the schema from an S3 path.
        df_params (DataFrameReadWriteParams): The parameters for reading and writing the DataFrame.
    """

    pyspark_schema_struct: Optional[Dict[str, Any]] = None
    s3_schema_path_params: Optional[S3ReadJsonParams] = None
    df_params: DataFrameReadWriteParams

    @model_validator(mode="before")
    def check_schema_mode(cls, data):
        """
        Check the schema mode and validate the input data.

        Args:
            cls: The class object.
            data: The input data dictionary.

        Returns:
            The validated input data dictionary.

        Raises:
            ValueError: If 'pyspark_schema_struct' and 's3_schema_path_params' are passed together.
        """
        pyspark_schema_struct = data.get("pyspark_schema_struct")
        s3_schema_path_params = data.get("s3_schema_path_params")

        if pyspark_schema_struct is not None and s3_schema_path_params is not None:
            raise ValueError(
                "'pyspark_schema_struct' and 's3_schema_path_params' cannot be passed together"
            )

        return data


class OutputDataFrameParams(BaseModelJsonDumps):
    """
    Represents the parameters for writing an output DataFrame.

    Attributes:
        write_schema_on_s3 (bool): Whether to write the schema on S3.
        overwrite (bool): Whether to overwrite existing data.
        df_params (DataFrameReadWriteParams): Parameters for reading and writing the DataFrame.
    """

    write_schema_on_s3: bool = False
    overwrite: bool = False
    df_params: DataFrameReadWriteParams


class FnIndirect(BaseModelJsonDumps):
    fn_name: str
    fn_path: str


class TransformParams(BaseModelJsonDumps):
    """
    Represents the parameters for a data transformation.

    Attributes:
        transform_label (str): The label for the transformation.
        transform_function (Callable): The transformation function. Must have a (pyspark) DataFrame type hint as first parameter and return type hint, or a dict of [str, DataFrame] as first parameter hint and return type hint.
        fn_kwargs (Optional[dict]): Additional keyword arguments for the transformation function.
        apply_only_on (Optional[List[str]]): A list of target dataframes to apply the transformation on.
    """

    transform_label: str
    transform_function: Callable
    fn_kwargs: Optional[dict] = None
    apply_only_on: Optional[List[str]] = None
    fn_indirect: Optional[FnIndirect] = None
    fn_kind: Optional[FnKind] = None

    @model_validator(mode="before")
    def validate_transform_function_indirect_and_apply_only_on(cls, data):
        fn_indirect = data.get("fn_indirect")
        transform_function = data.get("transform_function")
        apply_only_on = data.get("apply_only_on")

        def get_annotation_kind(annotation):
            origin = get_origin(annotation)
            args = get_args(annotation)

            if origin is dict and args[0] is str and issubclass(args[1], DataFrame):
                return FnKind.BATCH
            elif issubclass(annotation, DataFrame):
                return FnKind.SINGLE
            return None

        if fn_indirect is not None and transform_function is not None:
            raise ValueError(
                "'fn_indirect' and 'transform_function' cannot be passed together"
            )

        if fn_indirect is None and transform_function is None:
            raise ValueError(
                "Either 'fn_indirect' or 'transform_function' should be passed"
            )

        if fn_indirect:
            raise NotImplementedError("fn_indirect is not implemented yet")

        signature = inspect.signature(transform_function)
        parameters = signature.parameters
        first_param_annotation = (
            list(parameters.values())[0].annotation if parameters else None
        )
        return_annotation = signature.return_annotation

        first_param_kind = get_annotation_kind(first_param_annotation)
        return_kind = get_annotation_kind(return_annotation)

        if (first_param_kind is None or return_kind is None) or (
            first_param_kind != return_kind
        ):
            raise ValueError(
                "Function must have a DataFrame type hint as first parameter and return type hint, or a dict of [str, DataFrame] as first parameter hint and return type hint"
            )

        if first_param_kind != FnKind.SINGLE and apply_only_on is not None:
            raise ValueError(
                "'apply_only_on' is only accepted when 'transform_function' is of type 'single', that is, when the first parameter is a DataFrame type hint and the return type hint is also a DataFrame type hint."
            )

        # If the function has a DataFrame as first parameter, then it is a single function. If it has a dict of [str, DataFrame] as first parameter, then it is a batch function
        # TODO: This should be a private attribute
        data["fn_kind"] = first_param_kind

        return data


DataFrameDict = Dict[str, DataFrame]
InputDataFrameParamsDict = Dict[str, InputDataFrameParams]
OutputDataFrameParamsDict = Dict[str, OutputDataFrameParams]
TransformParamsDict = Dict[str, TransformParams]


class StepParams(BaseModelJsonDumps):
    """
    Represents the parameters for a step in a data pipeline.

    Attributes:
        input_dataframes_params (InputDataFrameParamsDict): The parameters for input dataframes.
        transform_params (Optional[TransformParamsDict]): The parameters for the transformation step. Defaults to None.
        output_dataframes_params (Optional[OutputDataFrameParamsDict]): The parameters for output dataframes. Defaults to None.
    """

    input_dataframes_params: InputDataFrameParamsDict
    transform_params: Optional[TransformParamsDict] = None
    output_dataframes_params: Optional[OutputDataFrameParamsDict] = None


StepParamsDict = Dict[str, StepParams]
