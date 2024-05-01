from __future__ import annotations

from math import isfinite, nan
from typing import TYPE_CHECKING, Any, Literal

from polars import DataFrame, Float64, Int64, Utf8, col, concat, lit
from polars.testing import assert_frame_equal
from pytest import mark, param, raises

from utilities.polars import (
    CheckPolarsDataFrameError,
    ColumnsToDictError,
    EmptyPolarsConcatError,
    SetFirstRowAsColumnsError,
    _check_polars_dataframe_predicates,
    _check_polars_dataframe_schema,
    _check_polars_dataframe_schema_inc,
    check_polars_dataframe,
    columns_to_dict,
    join,
    nan_sum_agg,
    nan_sum_cols,
    redirect_empty_polars_concat,
    set_first_row_as_columns,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from polars.type_aliases import PolarsDataType, SchemaDict


class TestCheckPolarsDataFrame:
    def test_main(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df)

    def test_columns_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, columns=[])

    def test_columns_error(self) -> None:
        df = DataFrame()
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must have columns .*; got .*\n\n.*",
        ):
            check_polars_dataframe(df, columns=["value"])

    def test_dtypes_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, dtypes=[])

    def test_dtypes_error(self) -> None:
        df = DataFrame()
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must have dtypes .*; got .*\n\n.*",
        ):
            check_polars_dataframe(df, dtypes=[Float64])

    def test_height_pass(self) -> None:
        df = DataFrame({"value": [0.0]})
        check_polars_dataframe(df, height=1)

    def test_height_error(self) -> None:
        df = DataFrame({"value": [0.0]})
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must satisfy the height requirements; got .*\n\n.*",
        ):
            check_polars_dataframe(df, height=2)

    def test_min_height_pass(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        check_polars_dataframe(df, min_height=1)

    def test_min_height_error(self) -> None:
        df = DataFrame()
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must satisfy the height requirements; got .*\n\n.*",
        ):
            check_polars_dataframe(df, min_height=1)

    def test_max_height_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, max_height=1)

    def test_max_height_error(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must satisfy the height requirements; got .*\n\n.*",
        ):
            check_polars_dataframe(df, max_height=1)

    def test_predicates_pass(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        check_polars_dataframe(df, predicates={"value": isfinite})

    def test_predicates_error_missing_columns_and_failed(self) -> None:
        df = DataFrame({"a": [0.0, nan], "b": [0.0, nan]})
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must satisfy the predicates; missing columns were .* and failed predicates were .*\n\n.*",
        ):
            check_polars_dataframe(df, predicates={"a": isfinite, "c": isfinite})

    def test_predicates_error_missing_columns_only(self) -> None:
        df = DataFrame()
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must satisfy the predicates; missing columns were .*\n\n.*",
        ):
            check_polars_dataframe(df, predicates={"a": isfinite})

    def test_predicates_error_failed_only(self) -> None:
        df = DataFrame({"a": [0.0, nan]})
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must satisfy the predicates; failed predicates were .*\n\n.*",
        ):
            check_polars_dataframe(df, predicates={"a": isfinite})

    def test_schema_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, schema={})

    def test_schema_error_set_of_columns(self) -> None:
        df = DataFrame()
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must have schema .*; got .*\n\n.*",
        ):
            check_polars_dataframe(df, schema={"value": Float64})

    def test_schema_error_order_of_columns(self) -> None:
        df = DataFrame(schema={"a": Float64, "b": Float64})
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must have schema .*; got .*\n\n.*",
        ):
            check_polars_dataframe(df, schema={"b": Float64, "a": Float64})

    def test_schema_inc_pass(self) -> None:
        df = DataFrame({"foo": [0.0], "bar": [0.0]})
        check_polars_dataframe(df, schema_inc={"foo": Float64})

    def test_schema_inc_error(self) -> None:
        df = DataFrame({"foo": [0.0]})
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame schema must include .*; got .*\n\n.*",
        ):
            check_polars_dataframe(df, schema_inc={"bar": Float64})

    def test_shape_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, shape=(0, 0))

    def test_shape_error(self) -> None:
        df = DataFrame()
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must have shape .*; got .*\n\n.*",
        ):
            check_polars_dataframe(df, shape=(1, 1))

    def test_sorted_pass(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        check_polars_dataframe(df, sorted="value")

    def test_sorted_error(self) -> None:
        df = DataFrame({"value": [1.0, 0.0]})
        with raises(
            CheckPolarsDataFrameError, match="DataFrame must be sorted on .*\n\n.*"
        ):
            check_polars_dataframe(df, sorted="value")

    def test_unique_pass(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        check_polars_dataframe(df, unique="value")

    def test_unique_error(self) -> None:
        df = DataFrame({"value": [0.0, 0.0]})
        with raises(
            CheckPolarsDataFrameError, match="DataFrame must be unique on .*\n\n.*"
        ):
            check_polars_dataframe(df, unique="value")

    def test_width_pass(self) -> None:
        df = DataFrame()
        check_polars_dataframe(df, width=0)

    def test_width_error(self) -> None:
        df = DataFrame()
        with raises(
            CheckPolarsDataFrameError,
            match="DataFrame must have width .*; got .*\n\n.*",
        ):
            check_polars_dataframe(df, width=1)


class TestCheckPolarsDataFramePredicates:
    def test_pass(self) -> None:
        df = DataFrame({"value": [0.0, 1.0]})
        _check_polars_dataframe_predicates(df, {"value": isfinite})

    @mark.parametrize(
        "predicates",
        [
            param({"other": Float64}, id="missing column"),
            param({"value": isfinite}, id="failed"),
        ],
    )
    def test_error(self, *, predicates: Mapping[str, Callable[[Any], bool]]) -> None:
        df = DataFrame({"value": [0.0, nan]})
        with raises(CheckPolarsDataFrameError):
            _check_polars_dataframe_predicates(df, predicates)


class TestCheckPolarsDataFrameSchema:
    def test_pass(self) -> None:
        df = DataFrame({"value": [0.0]})
        _check_polars_dataframe_schema(df, {"value": Float64})

    def test_error(self) -> None:
        df = DataFrame()
        with raises(CheckPolarsDataFrameError):
            _check_polars_dataframe_schema(df, {"value": Float64})


class TestCheckPolarsDataFrameSchemaInc:
    def test_pass(self) -> None:
        df = DataFrame({"foo": [0.0], "bar": [0.0]})
        _check_polars_dataframe_schema_inc(df, {"foo": Float64})

    @mark.parametrize(
        "schema_inc",
        [
            param({"bar": Float64}, id="missing column"),
            param({"foo": Int64}, id="wrong dtype"),
        ],
    )
    def test_error(self, *, schema_inc: SchemaDict) -> None:
        df = DataFrame({"foo": [0.0]})
        with raises(CheckPolarsDataFrameError):
            _check_polars_dataframe_schema_inc(df, schema_inc)


class TestColumnsToDict:
    def test_main(self) -> None:
        df = DataFrame(
            [{"a": 1, "b": 11}, {"a": 2, "b": 12}, {"a": 3, "b": 13}],
            schema={"a": Int64, "b": Int64},
        )
        mapping = columns_to_dict(df, "a", "b")
        assert mapping == {1: 11, 2: 12, 3: 13}

    def test_error(self) -> None:
        df = DataFrame(
            [{"a": 1, "b": 11}, {"a": 2, "b": 12}, {"a": 1, "b": 13}],
            schema={"a": Int64, "b": Int64},
        )
        with raises(ColumnsToDictError, match="DataFrame must be unique on 'a'"):
            _ = columns_to_dict(df, "a", "b")


class TestJoin:
    def test_main(self) -> None:
        df1 = DataFrame([{"a": 1, "b": 2}], schema={"a": Int64, "b": Int64})
        df2 = DataFrame([{"a": 1, "c": 3}], schema={"a": Int64, "c": Int64})
        result = join(df1, df2, on="a")
        expected = DataFrame(
            [{"a": 1, "b": 2, "c": 3}], schema={"a": Int64, "b": Int64, "c": Int64}
        )
        assert_frame_equal(result, expected)


class TestNanSumAgg:
    @mark.parametrize(
        ("data", "expected"),
        [
            param([None], None, id="one None"),
            param([None, None], None, id="two Nones"),
            param([0], 0, id="one int"),
            param([0, None], 0, id="one int, one None"),
            param([0, None, None], 0, id="one int, two Nones"),
            param([1, 2], 3, id="two ints"),
            param([1, 2, None], 3, id="two ints, one None"),
            param([1, 2, None, None], 3, id="two ints, two Nones"),
        ],
    )
    @mark.parametrize("dtype", [param(Int64), param(Float64)])
    @mark.parametrize("mode", [param("str"), param("column")])
    def test_main(
        self,
        *,
        data: list[Any],
        expected: int | None,
        dtype: PolarsDataType,
        mode: Literal["str", "column"],
    ) -> None:
        df = DataFrame({"value": data}, schema={"value": dtype}).with_columns(
            lit("id").alias("id")
        )
        match mode:
            case "str":
                agg = "value"
            case "column":
                agg = col("value")
        result = df.group_by("id").agg(nan_sum_agg(agg))
        assert result["value"].item() == expected


class TestNanSumCols:
    @mark.parametrize(
        ("x", "y", "expected"),
        [param(None, None, None), param(None, 0, 0), param(0, None, 0), param(1, 2, 3)],
    )
    @mark.parametrize("x_kind", [param("str"), param("column")])
    @mark.parametrize("y_kind", [param("str"), param("column")])
    def test_main(
        self,
        *,
        x: int | None,
        y: int | None,
        expected: int | None,
        x_kind: Literal["str", "column"],
        y_kind: Literal["str", "column"],
    ) -> None:
        x_use = "x" if x_kind == "str" else col("x")
        y_use = "y" if y_kind == "str" else col("y")
        df = DataFrame([(x, y)], schema={"x": Int64, "y": Int64}).with_columns(
            nan_sum_cols(x_use, y_use).alias("z")
        )
        assert df["z"].item() == expected


class TestRedirectEmptyPolarsConcat:
    def test_main(self) -> None:
        with raises(EmptyPolarsConcatError), redirect_empty_polars_concat():
            _ = concat([])


class TestSetFirstRowAsColumns:
    def test_empty(self) -> None:
        df = DataFrame()
        with raises(SetFirstRowAsColumnsError):
            _ = set_first_row_as_columns(df)

    def test_one_row(self) -> None:
        df = DataFrame(["value"])
        check_polars_dataframe(df, height=1, schema={"column_0": Utf8})
        result = set_first_row_as_columns(df)
        check_polars_dataframe(result, height=0, schema={"value": Utf8})

    def test_multiple_rows(self) -> None:
        df = DataFrame(["foo", "bar", "baz"])
        check_polars_dataframe(df, height=3, schema={"column_0": Utf8})
        result = set_first_row_as_columns(df)
        check_polars_dataframe(result, height=2, schema={"foo": Utf8})
