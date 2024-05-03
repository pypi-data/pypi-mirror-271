from collections import defaultdict
from functools import partial

import numpy as np
import pandas as pd

from .index import (END_COORDS,
                    count_base_types,
                    get_length,
                    has_mids,
                    iter_base_types,
                    stack_end_coords)
from ..rel import MATCH, NOCOV, RelPattern
from ..seq import POS_NAME, DNA


def count_end_coords(end5s: np.ndarray,
                     end3s: np.ndarray,
                     weights: pd.DataFrame | None = None):
    """ Count each pair of 5' and 3' end coordinates. """
    # Make a MultiIndex of all 5' and 3' coordinates.
    index = pd.MultiIndex.from_frame(pd.DataFrame(stack_end_coords(end5s,
                                                                   end3s),
                                                  columns=END_COORDS,
                                                  copy=False))
    # Convert the read weights into a Series/DataFrame with that index.
    if weights is not None:
        weights = pd.DataFrame(weights.values, index, weights.columns)
    else:
        weights = pd.Series(1., index)
    # Sum the weights for each unique pair of 5'/3' coordinates.
    return weights.groupby(level=list(range(weights.index.nlevels))).sum()


def get_half_coverage_matrix(pos_nums: np.ndarray,
                             pos5s: np.ndarray,
                             pos3s: np.ndarray):
    # Reshape the positions and 5'/3' ends to row and column vectors,
    # then make a boolean matrix where each element indicates whether
    # the read (row) covers the position (column).
    return np.logical_and(pos5s[:, np.newaxis] <= pos_nums[np.newaxis, :],
                          pos_nums[np.newaxis, :] <= pos3s[:, np.newaxis])


def get_coverage_matrix(pos_index: pd.Index,
                        end5s: np.ndarray,
                        mid5s: np.ndarray | None,
                        mid3s: np.ndarray | None,
                        end3s: np.ndarray,
                        read_nums: np.ndarray):
    pos_nums = pos_index.get_level_values(POS_NAME).values
    if has_mids(mid5s, mid3s):
        # If 5' and 3' middle coordinates are present, then take the
        # union of the coverage of both mates.
        coverage_matrix = np.logical_or(
            get_half_coverage_matrix(pos_nums, end5s, mid3s),
            get_half_coverage_matrix(pos_nums, mid5s, end3s)
        )
    else:
        # Otherwise, just take the coverage between the 5' and 3' ends.
        coverage_matrix = get_half_coverage_matrix(pos_nums, end5s, end3s)
    return pd.DataFrame(coverage_matrix,
                        index=read_nums,
                        columns=pos_index,
                        copy=False)


def get_cover_per_pos(coverage_matrix: pd.DataFrame,
                      read_weights: pd.DataFrame | None = None):
    """ Number of reads covering each position. """
    if read_weights is not None:
        if not read_weights.index.equals(coverage_matrix.index):
            raise ValueError(f"Read numbers differ between the coverage matrix "
                             f"({coverage_matrix.index}) and the weights "
                             f"({read_weights.index})")
        cover_per_pos = pd.DataFrame(0.,
                                     index=coverage_matrix.columns,
                                     columns=read_weights.columns)
        for pos_base, coverage in coverage_matrix.items():
            for cluster, weights in read_weights.items():
                cover_per_pos.loc[pos_base, cluster] = weights[coverage].sum()
        return cover_per_pos
    return pd.Series(np.count_nonzero(coverage_matrix.values, axis=0),
                     index=coverage_matrix.columns)


def get_cover_per_read(coverage_matrix: pd.DataFrame):
    """ Number of positions covered by each read. """
    cover_per_read = {
        base: pd.Series(np.count_nonzero(coverage_matrix.loc[:, index], axis=1),
                        index=coverage_matrix.index)
        for base, index in iter_base_types(coverage_matrix.columns)
    }
    if not cover_per_read:
        cover_per_read = {
            base: pd.Series(0, index=coverage_matrix.index)
            for base in DNA.alph()
        }
    return pd.DataFrame.from_dict(cover_per_read)


def get_rels_per_pos(mutations: dict[int, dict[int, np.ndarray]],
                     num_reads: int | pd.Series,
                     cover_per_pos: pd.Series | pd.DataFrame,
                     read_indexes: np.ndarray | None = None,
                     read_weights: pd.DataFrame | None = None):
    """ For each relationship, the number of reads at each position. """
    slice_type = type(num_reads)
    array_type = type(cover_per_pos)
    pos_index = cover_per_pos.index
    if read_weights is not None:
        data_type = float
        if not isinstance(read_weights, array_type):
            raise TypeError(f"Expected read_weights to be {array_type}, "
                            f"but got {type(read_weights)}")
        clusters = read_weights.columns
        if slice_type is not pd.Series:
            raise TypeError(f"Expected num_reads to be {pd.Series}, "
                            f"but got {slice_type}")
        slice_indexes = dict(index=clusters)
        if array_type is not pd.DataFrame:
            raise TypeError(f"Expected cover_per_pos to be {pd.DataFrame}, "
                            f"but got {array_type}")
        array_indexes = dict(index=pos_index, columns=clusters)
        if isinstance(read_indexes, np.ndarray):
            if read_indexes.ndim != 1:
                raise ValueError(f"Expected read_indexes to have 1 dimension, "
                                 f"but got {read_indexes.ndim}")
        else:
            raise TypeError(f"Expected read_indexes to be {np.ndarray}, "
                            f"bot got {type(read_indexes)}")
        if not clusters.equals(num_reads.index):
            raise ValueError(f"Clusters differ between the number of reads "
                             f"({num_reads.index}) and the weights "
                             f"({clusters})")
        if not clusters.equals(cover_per_pos.columns):
            raise ValueError(f"Clusters differ between the coverage matrix "
                             f"({cover_per_pos.columns}) and the weights "
                             f"({clusters})")
    else:
        data_type = int
        if slice_type is not int:
            raise TypeError(f"Expected num_reads to be {int}, "
                            f"but got {slice_type}")
        slice_indexes = dict()
        if array_type is not pd.Series:
            raise TypeError(f"Expected cover_per_pos to be {pd.Series}, "
                            f"but got {array_type}")
        array_indexes = dict(index=pos_index)
    counts = defaultdict(partial(array_type, data_type(0), **array_indexes))
    for pos_base in cover_per_pos.index:
        pos, base = pos_base
        num_reads_pos = slice_type(data_type(0), **slice_indexes)
        for mut, reads in mutations.get(pos, dict()).items():
            if read_weights is not None:
                rows = read_indexes[reads]
                num_reads_pos_mut = read_weights.values[rows].sum(axis=0)
            else:
                num_reads_pos_mut = get_length(reads, "read numbers")
            num_reads_pos += num_reads_pos_mut
            counts[mut].loc[pos_base] = num_reads_pos_mut
        # The number of matches is the coverage minus the number of
        # reads with another kind of relationship that is not the
        # no-coverage relationship (no coverage is counted later).
        counts[MATCH].loc[pos_base] = (cover_per_pos.loc[pos_base]
                                       - num_reads_pos)
        # The number of non-covered positions is the number of reads
        # minus the number that cover the position.
        counts[NOCOV].loc[pos_base] = num_reads - cover_per_pos.loc[pos_base]
    return dict(counts)


def get_rels_per_read(mutations: dict[int, dict[int, np.ndarray]],
                      pos_index: pd.Index,
                      cover_per_read: pd.DataFrame,
                      read_indexes: np.ndarray):
    """ For each relationship, the number of positions in each read. """
    bases = list(cover_per_read.columns)
    counts = defaultdict(partial(pd.DataFrame,
                                 0,
                                 index=cover_per_read.index,
                                 columns=cover_per_read.columns))
    counts[NOCOV] = count_base_types(pos_index) - cover_per_read
    counts[MATCH] = cover_per_read.copy()
    for pos, base in pos_index:
        column = bases.index(base)
        for mut, reads in mutations.get(pos, dict()).items():
            rows = read_indexes[reads]
            counts[MATCH].values[rows, column] -= 1
            counts[mut].values[rows, column] += 1
    return dict(counts)


def get_reads_per_pos(pattern: RelPattern,
                      mutations: dict[int, dict[int, np.ndarray]],
                      pos_index: pd.Index):
    """ For each position, find all reads matching a pattern. """
    reads = dict()
    for pos, base in pos_index:
        pos_reads = [pos_mut_reads for mut, pos_mut_reads
                     in mutations.get(pos, dict()).items()
                     if all(pattern.fits(base, mut))]
        reads[pos] = np.hstack(pos_reads) if pos_reads else np.array([], int)
    return reads


def get_count_per_pos(pattern: RelPattern,
                      cover_per_pos: pd.Series | pd.DataFrame,
                      rels_per_pos: dict[int, pd.Series | pd.DataFrame]):
    """ Count the reads that fit a pattern at each position. """
    array_type = type(cover_per_pos)
    pos_index = cover_per_pos.index
    if array_type is pd.Series:
        data_type = int
        indexes = dict(index=pos_index)
    elif array_type is pd.DataFrame:
        data_type = float
        indexes = dict(index=pos_index, columns=cover_per_pos.columns)
    else:
        raise TypeError(f"Expected cover_per_pos to be {pd.Series} or "
                        f"{pd.DataFrame}, but got {array_type}")
    info = array_type(data_type(0), **indexes)
    fits = array_type(data_type(0), **indexes)
    for base, index in iter_base_types(pos_index):
        for rel, counts in rels_per_pos.items():
            is_info, is_fits = pattern.fits(base, rel)
            if is_info:
                pos_counts = counts.loc[index]
                info.loc[index] += pos_counts
                if is_fits:
                    fits.loc[index] += pos_counts
    return info, fits


def get_count_per_read(pattern: RelPattern,
                       cover_per_read: pd.DataFrame,
                       rels_per_read: dict[int, pd.DataFrame],
                       read_weights: pd.DataFrame | None = None):
    """ Count the positions that fit a pattern in each read. """
    read_nums = cover_per_read.index
    if read_weights is not None:
        data_type = float
        array_type = pd.DataFrame
        array_indexes = dict(index=read_nums, columns=read_weights.columns)
    else:
        data_type = int
        array_type = pd.Series
        array_indexes = dict(index=read_nums)
    info = array_type(data_type(0), **array_indexes)
    fits = array_type(data_type(0), **array_indexes)
    for rel, rel_counts in rels_per_read.items():
        for base, base_counts in rel_counts.items():
            is_info, is_fits = pattern.fits(str(base), rel)
            if is_info:
                if read_weights is not None:
                    read_counts = (read_weights.values
                                   * base_counts.values[:, np.newaxis])
                else:
                    read_counts = base_counts.values
                info += read_counts
                if is_fits:
                    fits += read_counts
    return info, fits

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
