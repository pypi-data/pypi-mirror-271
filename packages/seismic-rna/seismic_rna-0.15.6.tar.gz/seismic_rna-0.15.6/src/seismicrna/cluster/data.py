from functools import cached_property
from logging import getLogger

from .batch import ClusterMutsBatch
from .io import ClusterBatchIO
from .report import ClusterReport
from ..core.data import ChainedMutsDataset, LoadedDataset, LoadFunction
from ..core.header import index_orders_clusts
from ..core.report import NumClustsF
from ..mask.batch import MaskMutsBatch
from ..mask.data import load_mask_dataset

logger = getLogger(__name__)


class ClusterReadDataset(LoadedDataset):
    """ Load clustering results. """

    @classmethod
    def get_report_type(cls):
        return ClusterReport

    @classmethod
    def get_batch_type(cls):
        return ClusterBatchIO

    @cached_property
    def max_order(self):
        """ Number of clusters. """
        return self.report.get_field(NumClustsF)

    @property
    def pattern(self):
        return None


class ClusterMutsDataset(ChainedMutsDataset):
    """ Merge cluster responsibilities with mutation data. """

    @classmethod
    def get_dataset1_load_func(cls):
        return load_mask_dataset

    @classmethod
    def get_dataset2_type(cls):
        return ClusterReadDataset

    @property
    def min_mut_gap(self):
        return getattr(self.data1, "min_mut_gap")

    @property
    def pattern(self):
        return self.data1.pattern

    @cached_property
    def section(self):
        return self.data1.section

    @cached_property
    def max_order(self):
        return getattr(self.data2, "max_order")

    @cached_property
    def clusters(self):
        return index_orders_clusts(self.max_order)

    def _chain(self, batch1: MaskMutsBatch, batch2: ClusterBatchIO):
        return ClusterMutsBatch(batch=batch1.batch,
                                refseq=batch1.refseq,
                                muts=batch1.muts,
                                end5s=batch1.end5s,
                                mid5s=batch1.mid5s,
                                mid3s=batch1.mid3s,
                                end3s=batch1.end3s,
                                resps=batch2.resps,
                                sanitize=False)


load_cluster_dataset = LoadFunction(ClusterMutsDataset)

########################################################################
#                                                                      #
# © Copyright 2024, the Rouskin Lab.                                   #
#                                                                      #
# This file is part of SEISMIC-RNA.                                    #
#                                                                      #
# SEISMIC-RNA is free software; you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation; either version 3 of the License, or    #
# (at your option) any later version.                                  #
#                                                                      #
# SEISMIC-RNA is distributed in the hope that it will be useful, but   #
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANT- #
# ABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General     #
# Public License for more details.                                     #
#                                                                      #
# You should have received a copy of the GNU General Public License    #
# along with SEISMIC-RNA; if not, see <https://www.gnu.org/licenses>.  #
#                                                                      #
########################################################################
