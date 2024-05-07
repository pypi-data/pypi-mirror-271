# - Dataset

"""
Introduction to the :class:`paguro.Dataset` object wrapper to a Polars DataFrame (or LazyFrame)
which:

- allows you to store and display metadata
- contains some extra methods for data exploration
"""

# <> Imports
import paguro as po
import datetime

# : Creating a Dataset

# %% from a dict

data = po.Dataset(
    {
        "numbers": [1, 2, 3],
        "letters": ["a", "b", "b"],
        "dates": [
            datetime.date(2010, 1, 1),
            datetime.date(2011, 1, 1),
            datetime.date(2012, 1, 1)]
    },
    name="example-dataset"  # optionally: we can give a name to the dataset
)

# <> dir
# collapse
dir(table)

# : Metadata

# %% Name

# %% Info

"""
Check if there is a subtitle
"""

# %%

# import paguro as po
# import pathlib
#
# po.Config.set_width_char(60)
#
# # %% initializing a Dataset
#
# # LazyFrame by default
#
# data = po.Dataset(
#     {
#         "numbers": [1, 2, 3],
#         "letters": ["a", "b", "b"],
#     },
#     name="example"  # not necessary
# )
#
# data
#
# # %%
#
# """Adding info/metadata to a DataFrame/LazyFrame
# """
#
# data.collect()
#
# # %% adding metadata: column level metadata
#
# data = (
#     data
#     .with_info("some descriptions", numbers="some numbers")
#     .with_info(letters="some letters")
# )
#
# data
#
# # %% adding metadata: other column level metadata
#
# (
#     data
#     .with_info("some descriptions new", numbers="some numbers new")
#     .with_info(letters="some letters new")
# )
#
# # %% adding metadata: non-column level metadata
#
# data.with_info(non_column_name="some info")
#
# # %%
#
# data.select("numbers")
#
# # %%
#
# (
#     data
#     .select("numbers", "dates")
#     .rename({"dates": "new_name_for_dates"})
# )
#
# # %% adding non-column level metadata
#
# data = (
#     data
#     .with_info("data info", description="some description")
#     .with_info(
#         "data info",
#         other="other stuff"
#     )
# )
#
# # %%
#
# file_path, file_name = pathlib.Path("/Users/bernardodionisi/Desktop/"), "dataset-example.parquet"
#
# data.write_parquet(file_path / file_name)
#
# # %%
#
# po.scan_parquet(file_path / file_name)
#
# # %%
#
# po.read_parquet(file_path / file_name)
#
# # %%
#
# po.read_parquet_schema_metadata(file_path / file_name)


# %% Column Info


# : Descriptives

# %% tabulate

data.tabulate("numbers", "letters", by=True)

# %%

# data._box.set_pl_titles(("AAsdv", "BBB"))
#
# data.collect()

# %% skim
po.Config.set_width_char(100)

data.skim(by="letters")

# : Polars Methods

"""
The Dataset class implements getattr which intercepts attribute and method access to
provide convenient access to the underlying data object (DataFrame or LazyFrame) stored in
:attr:`data <paguro.Dataset.data>`. This enables you to cleanly chain multiple
operations on the Dataset by calling
methods directly on the Dataset instance, while maintaining the Dataset wrapper.

When you access an attribute or method on a Dataset instance, getattr will access
that attribute or method directly on the underlying DataFrame or LazyFrame stored
in :attr:`data <paguro.Dataset.data>`. However, if the return value is another DataFrame or LazyFrame,
getattr will wrap it in a new Dataset instance before returning it.
"""

# import paguro as po
#
# po.Config.set_width_char(150)
# data = po.read_stata("/Users/bernardodionisi/Downloads/4_clean_tables_stata/FDA_drug_patents.dta")
#
# data.select("edition")
#
# data.skim(hist=True, by="application_type").set_operate_on(None).sort("column")
# import polars as pl
#
# data["edition"].value_counts().sort("edition")
# pl.Config.set_tbl_cols(None)
# pl.Config.set_tbl_rows(100)
#
# import os
# os.environ.get("POLARS_FMT_MAX_ROWS", None)
#
#
# left = pl.DataFrame({"x": [1, 2, 3, 4]}).lazy()
# right = pl.DataFrame({"x": [3, 2, 1]}).lazy()
#
# left.join(right, on="x", how="outer").select("x_right").collect()


#
# Dataset
# *******
#
# Introduction
# ============
#
# A :class:`paguro.Dataset` is a wrapper to a Polars DataFrame (or LazyFrame) which:
#

#
# .. code-example::
#     :collapsible:
#
#     .. ipython:: python
#
#         import paguro
#         from datetime import date
#
#         data = paguro.Dataset(
#             {
#                 "numbers": [1, 2, 3],
#                 "letters": ["a", "b", "c"],
#                 "dates": [date(2010, 1, 1), date(2011, 1, 1), date(2012, 1, 1)]
#             },
#             name="example-dataset"  # we can give the dataset a name
#         )
#
#         data
#
#
# How to ...
# ==========
#
# add information?
# ----------------
#
# .. code-example::
#     :collapsible:
#
#     .. ipython:: python
#
#         data = data
#
# Delegation
