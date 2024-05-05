import urllib.request
import zipfile
import io
from typing import Tuple
import warnings
import polars as pl
from scipy.io import mmread
from scipy.sparse import issparse, coo_matrix
import numpy as np

from .datasets import ParquetDataset


class Weizmann3CA(ParquetDataset):
    """Curated Cancer Cell Atlas of collected, annotated and analyzed cancer scRNA-seq datasets from the Weizmann Institute of Science."""

    COLLECTION = "weizmann_ccca"
    SOURCE = "https://raw.githubusercontent.com/aion-labs/aiondata/main/data/3ca_links.parquet"

    def __getitem__(
        self, study_name_to_find: str
    ) -> Tuple[pl.DataFrame, list, pl.DataFrame, coo_matrix]:
        """
        Retrieve data for a specific study name.

        Args:
            study_name_to_find (str): The study name to search for.

        Returns:
            Tuple: A tuple containing the following data:
                - cells (DataFrame): The cells data.
                - genes (List): The genes data.
                - metadata (DataFrame): The metadata.
                - exp_data (NDArray[Any]): The experimental data.

        Raises:
            ValueError: If the study name is not found in the dataset.
        """
        links = self.to_df()
        row = links.filter(pl.col("Study name") == study_name_to_find)
        if row.height == 0:
            raise ValueError(
                f"Study name {study_name_to_find} not found in the dataset."
            )

        data_url = row.get_column("Data")[0]

        zip_file = self._download_or_cache(study_name_to_find, data_url)

        with warnings.catch_warnings():
            # Polars raises a UserWarning when reading a CSV file from a file-like object
            # The warning is only performance-related and can be safely ignored
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(zip_file) as zip_file:
                cells = self._load_csv_from_zip(zip_file, "Cells.csv")
                genes = self._load_gene_list_file(zip_file, "Genes.txt")
                metadata = self._load_csv_from_zip(zip_file, "Meta-data.csv")
                # Find matrix market file in zip
                matrix_file_name = [
                    f for f in zip_file.namelist() if f.endswith(".mtx")
                ][0]
                exp_data = self._load_mtx_from_zip(zip_file, matrix_file_name)

        return cells, genes, metadata, exp_data

    def get_gene_expression_by_cell(self, study_name: str) -> list:
        """
        Retrieves the gene expression data for each cell in a given study.

        Args:
            study_name (str): The name of the study.

        Returns:
            list: A list of dictionaries, where each dictionary represents the gene expression data for a cell.
                  Each dictionary contains the cell name as well as the gene expression values for that cell.
        """
        cells, genes, _, exp_data = self[study_name]

        cell_gene_expression_dicts = []

        if issparse(exp_data):
            exp_data_csc = exp_data.tocsc()  # Ensure it's in a column-suitable format
        else:
            raise ValueError("exp_data must be a scipy sparse matrix.")

        cell_names = cells["cell_name"].to_list()
        cell_types = cells["cell_type"].to_list()

        for col_idx, (cell_name, cell_type) in enumerate(zip(cell_names, cell_types)):
            cell_data = (
                exp_data_csc[:, col_idx].toarray().ravel()
            )  # Get expression values for the current cell
            gene_expression_dict = {
                genes[row_idx]: cell_data[row_idx]
                for row_idx in range(len(genes))
                if cell_data[row_idx] != 0
            }

            if gene_expression_dict:
                # Prepend the cell name to the dictionary
                cell_gene_expression = {
                    "_cell_name": cell_name,
                    "_cell_type": cell_type,
                    **gene_expression_dict,
                }
                cell_gene_expression_dicts.append(cell_gene_expression)

        return cell_gene_expression_dicts

    def _download_or_cache(self, study_name: str, data_url: str) -> "os.PathLike":
        filename = study_name.replace(" ", "_") + ".zip"
        cache = self.get_cache_path().parent / filename
        if not cache.exists():
            response = urllib.request.urlopen(data_url)
            with open(cache, "wb") as fd:
                fd.write(response.read())
        return cache

    def _load_csv_from_zip(
        self, zip_file: zipfile.ZipFile, file_name: str
    ) -> pl.DataFrame:
        with zip_file.open(file_name) as fd:
            return pl.read_csv(fd)

    def _load_mtx_from_zip(
        self, zip_file: zipfile.ZipFile, file_name: str
    ) -> "NDArray[Any]":
        with zip_file.open(file_name) as fd:
            # Convert file-like object to StringIO to be compatible with mmread
            content = io.StringIO(fd.read().decode())
            matrix = mmread(content)
            return matrix

    def _load_gene_list_file(self, zip_file: zipfile.ZipFile, file_name: str) -> list:
        with zip_file.open(file_name) as fd:
            # Convert file-like object to list of strings and remove quotes
            content = fd.read().decode().splitlines()
            content = [x.replace('"', "") for x in content]
        return content
