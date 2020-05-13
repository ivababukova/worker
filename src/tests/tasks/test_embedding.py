import pytest
import anndata
import os
from tasks.embedding import ComputeEmbedding
from result import Result
import numpy as np


class TestEmbedding:
    @pytest.fixture(autouse=True)
    def open_test_adata(self):
        self._adata = anndata.read_h5ad(os.path.join("tests", "test.h5ad"))

    def test_computeembedding_throws_on_missing_anndata(self):
        with pytest.raises(TypeError):
            ComputeEmbedding()

    def test_computeembedding_works_with_test_data(self):
        ComputeEmbedding(self._adata)

    def test_pca_edits_object_appropriately(self):
        old = np.array(self._adata.obsm["X_pca"][:, :2])

        res = ComputeEmbedding(self._adata)._PCA()

        assert not np.array_equal(res, old)

    def test_pca_deals_with_incomplete_previous_results(self):
        self._adata.obsm.pop("X_pca", None)
        ComputeEmbedding(self._adata)._PCA()

    def test_computeembedding_throws_on_invalid_embedding_type(self):
        with pytest.raises(Exception):
            ComputeEmbedding(self._adata).compute("definitelynotavalidembedding")