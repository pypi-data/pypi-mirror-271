import unittest as ut

from seismicrna.core.rel import IRREC, MATCH, NOCOV, SUB_G
from seismicrna.relate.py.relate import find_rels_line, _merge_mates, SamRead
from seismicrna.relate.aux.iterread import iter_alignments
from seismicrna.align.sim import as_sam
from seismicrna.core.arg import opt_min_mapq
from seismicrna.core.ngs import OK_QUAL
from seismicrna.core.seq import DNA


class TestRelateRelateLineAmbrel(ut.TestCase):
    """ Test function `relate.relate_line`. """

    MAPQ = opt_min_mapq.default

    @staticmethod
    def relate(ref: str,
               refseq: DNA,
               read: DNA,
               qual: str,
               mapq: int,
               cigar: str,
               end5: int):
        """ Generate a SAM line from the given information, and use it
        to compute a relation vector. """
        sam_line = as_sam("read",
                          99,
                          ref,
                          end5,
                          mapq,
                          cigar,
                          "=",
                          1,
                          len(read),
                          read,
                          qual)
        return find_rels_line(sam_line,
                              "",
                              ref,
                              refseq,
                              opt_min_mapq.default,
                              OK_QUAL,
                              True,
                              False)

    def iter_cases(self, refseq: DNA, max_ins: int = 2):
        """ Iterate through every test case. """
        for read, qual, cigar, end5, end3, rels in iter_alignments(refseq,
                                                                   max_ins,
                                                                   max_ins,
                                                                   max_ins):
            with self.subTest(refseq=refseq,
                              read=read,
                              qual=qual,
                              end5=end5,
                              cigar=cigar,
                              rels=rels):
                name, end5_, mid5, mid3, end3_, rels_ = self.relate("ref",
                                                                    refseq,
                                                                    read,
                                                                    qual,
                                                                    self.MAPQ,
                                                                    cigar,
                                                                    end5)
                self.assertEqual(end5_, end5)
                self.assertEqual(mid5, end5)
                self.assertEqual(mid3, end3)
                self.assertEqual(end3_, end3)
                self.assertEqual(rels_, rels)

    def test_aaaa_0ins(self):
        """ Test all possible reads with 0 insertions from AAAA. """
        self.iter_cases(DNA("AAAA"), 0)

    @ut.skip("Takes a long time to run; burdensome while debugging others")
    def test_aaaaaa_0ins(self):
        """ Test all possible reads with 0 insertions from AAAAAA. """
        self.iter_cases(DNA("AAAAAA"), 0)

    @ut.skip("Takes a long time to run; burdensome while debugging others")
    def test_aacc_1ins(self):
        """ Test all possible reads with ≤ 1 insertion from AACC. """
        self.iter_cases(DNA("AACC"), 1)

    def test_acgt_1ins(self):
        """ Test all possible reads with ≤ 1 insertion from ACGT. """
        self.iter_cases(DNA("ACGT"), 1)


class TestMergeMates(ut.TestCase):

    SAM_READ = SamRead("read-name\t"
                       "147\tref-seq\t189\t36\t42M5S\t=\t10\t-240\tGGGAT"
                       "TGTTCATGGTGCATTTCACGCTACTCGTTCCTTTCGAACGAG\tCCCCCCCCCC"
                       "CC;CCCCCC;CCCCCCCCC;CCCCCCCCCCCCCCCCC\tAS:i:84\tXN:i:0"
                       "\tXM:i:0\tXO:i:0\tXG:i:0\tYS:i:66\tYT:Z:CP\tMD:Z:42\tN"
                       "M:i:0")
    OVERHANGS = True

    def test_empty(self):
        result = _merge_mates(1, 10, {}, 1, 10, {}, TestMergeMates.OVERHANGS,
                                                    TestMergeMates.SAM_READ)
        expect = ({}, (1, 1, 10, 10))
        self.assertEqual(result, expect)

    def test_read1(self):
        end51 = 1
        end31 = 20
        end52 = 11
        end32 = 30
        for pos in range(end51, end31 + 1):
            for rel in range(MATCH + 1, NOCOV):
                result = _merge_mates(end51, end31, {pos: rel},
                                     end52, end32, {},
                                     TestMergeMates.OVERHANGS,
                                     TestMergeMates.SAM_READ)
                if end52 <= pos <= end32:
                    # The relationship can be compensated by read 2.
                    if rel & MATCH:
                        # The match in read 2 compensated.
                        expect = ({}, (1, 11, 20, 30))
                    else:
                        # The match in read 2 is irreconcilable.
                        expect = ({pos: IRREC}, (1, 11, 20, 30))
                else:
                    # Read 2 cannot compensate.
                    expect = ({pos: rel}, (1, 11, 20, 30))
                self.assertEqual(result, expect)

    def test_read2(self):
        end51 = 1
        end31 = 20
        end52 = 11
        end32 = 30
        for pos in range(end52, end32 + 1):
            for rel in range(MATCH + 1, NOCOV):
                result = _merge_mates(end51, end31, {},
                                     end52, end32, {pos: rel},
                                     TestMergeMates.OVERHANGS,
                                     TestMergeMates.SAM_READ)
                if end51 <= pos <= end31:
                    # The relationship can be compensated by read 1.
                    if rel & MATCH:
                        # The match in read 1 compensated.
                        expect = ({}, (1, 11, 20, 30))
                    else:
                        # The match in read 1 is irreconcilable.
                        expect = ({pos: IRREC},  (1, 11, 20, 30))
                else:
                    # Read 1 cannot compensate.
                    expect = ({pos: rel},  (1, 11, 20, 30))
                self.assertEqual(result, expect)

    def test_both_reads(self):
        end51 = 1
        end31 = 2
        end52 = 2
        end32 = 3
        for pos1 in range(end51, end31 + 1):
            for rel1 in range(MATCH + 1, NOCOV):
                rels1 = {pos1: rel1}
                for pos2 in range(end52, end32 + 1):
                    for rel2 in range(MATCH + 1, NOCOV):
                        rels2 = {pos2: rel2}
                        with self.subTest(pos1=pos1, rel1=rel1,
                                          pos2=pos2, rel2=rel2):
                            result = _merge_mates(end51, end31, rels1,
                                                 end52, end32, rels2,
                                                 TestMergeMates.OVERHANGS,
                                                 TestMergeMates.SAM_READ)
                            if pos1 == pos2:
                                merged = rel1 & rel2
                                if merged == MATCH:
                                    expect = ({}, (1, 2, 2, 3))
                                else:
                                    expect = ({pos1: merged}, (1, 2, 2, 3))
                            else:
                                expect = (dict(), (1, 2, 2, 3))
                                merged1 = rel1 & MATCH if end52 <= pos1 <= end32 else rel1
                                if merged1 != MATCH:
                                    expect[0][pos1] = merged1
                                merged2 = rel2 & MATCH if end51 <= pos2 <= end31 else rel2
                                if merged2 != MATCH:
                                    expect[0][pos2] = merged2
                            self.assertEqual(result, expect)

    def test_both_blank(self):
        end51 = 1
        end31 = 2
        end52 = 2
        end32 = 3
        for pos1 in range(end51, end31 + 1):
            rels1 = {pos1: NOCOV}
            for pos2 in range(end52, end32 + 1):
                rels2 = {pos2: NOCOV}
                with self.subTest(pos1=pos1, pos2=pos2):
                    if end52 <= pos1 <= end32:
                        error = pos2
                    else:
                        error = pos1
                    self.assertRaisesRegex(
                        ValueError,
                        f"Cannot merge two blanks at position {error}",
                        _merge_mates,
                        end51, end31, rels1,
                        end52, end32, rels2,
                        TestMergeMates.OVERHANGS, TestMergeMates.SAM_READ
                    )

    def test_overhangs(self):
        sam_read = TestMergeMates.SAM_READ
        rels1 = {pos: SUB_G for pos in range(1, 10)}
        rels2 = {pos: SUB_G for pos in range(1, 10)}
        for overhangs in [True, False]:
            for rev_flag in [True, False]:
                end51 = 1
                end31 = 3
                end52 = 4
                end32 = 6
                sam_read.flag.rev = rev_flag
                while end31 <= 9:
                    if ((sam_read.flag.rev and end51 > end32) or
                        (not TestMergeMates.SAM_READ.flag.rev and end31 < end52)):
                        self.assertRaisesRegex(ValueError,
                                               "Mate orientation for"
                                               f" {repr(sam_read.qname)} cannot"
                                               " be merged with --no-overhangs")
                    else:
                        result = _merge_mates(end51,
                                              end31,
                                              rels1,
                                              end52,
                                              end32,
                                              rels2,
                                              overhangs,
                                              sam_read)
                        ends = (((end51,
                                max(end51, end52),
                                min(end32, end31),
                                end32)
                                if sam_read.flag.rev else
                                (end52,
                                 max(end52, end51),
                                 min(end31, end32),
                                 end31))
                                if not overhangs else
                                (min(end51, end52),
                                 max(end51, end52),
                                 min(end31, end32),
                                 max(end31, end32)))
                        rels = (({pos: SUB_G for pos in range(end51, end32+1)}
                                 if sam_read.flag.rev else
                                 {pos: SUB_G for pos in range(end52, end31+1)})
                                if not overhangs else
                                ({pos: SUB_G for pos in range(min(end51, end52),
                                                              max(end31, end32)+1)}))
                        expect = (rels, ends)
                        self.assertEqual(result, expect)
                    end51 += 1
                    end31 += 1


if __name__ == "__main__":
    ut.main()

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
