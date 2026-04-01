#!/usr/bin/env python3

"""
Export Sequenza segment tables to IGV-compatible .seg files for Figure 3.

This script generates two track types per sample:
1. relative copy-number tracks: seg.mean = CNt - sample_ploidy
2. absolute copy-number tracks: seg.mean = CNt - 2
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Optional
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export Sequenza segments to IGV .seg files for Figure 3."
    )
    parser.add_argument(
        "--sequenza-dir",
        required=True,
        help="Path to directory containing per-sample Sequenza result folders.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Path to output directory for exported .seg files.",
    )
    parser.add_argument(
        "--sample-list",
        default=None,
        help="Optional text file with one sample ID per line. If omitted, all valid sample folders are used.",
    )
    return parser.parse_args()


def load_sample_list(sample_list_path: Optional[str]) -> Optional[List[str]]:
    if sample_list_path is None:
        return None

    with open(sample_list_path, "r") as handle:
        samples = [line.strip() for line in handle if line.strip()]
    return samples


def discover_samples(sequenza_dir: Path, requested_samples: Optional[List[str]]) -> List[str]:
    if requested_samples is not None:
        return requested_samples

    samples = []
    for child in sorted(sequenza_dir.iterdir()):
        if not child.is_dir():
            continue
        sample_name = child.name
        seg_file = child / f"{sample_name}_segments.txt"
        cp_file = child / f"{sample_name}_confints_CP.txt"
        if seg_file.exists() and cp_file.exists():
            samples.append(sample_name)
    return samples


def choose_ploidy_row(confints_df: pd.DataFrame) -> pd.Series:
    """
    Reproduce notebook behavior as closely as possible.

    Preferred behavior:
    - if a probability-like column exists, use the maximum-probability row
    - otherwise, if there are exactly 3 rows, use the middle row (index 1)
    - otherwise, use the first row
    """
    probability_candidates = [
        "probability",
        "posterior",
        "likelihood",
        "LL",
    ]
    for col in probability_candidates:
        if col in confints_df.columns:
            return confints_df.loc[confints_df[col].idxmax()]

    if len(confints_df) == 3:
        return confints_df.iloc[1]

    return confints_df.iloc[0]


def load_ploidy_estimates(sequenza_dir: Path, samples: List[str]) -> Dict[str, float]:
    ploidy_dict: Dict[str, float] = {}

    for sample in samples:
        cp_file = sequenza_dir / sample / f"{sample}_confints_CP.txt"
        confints_df = pd.read_csv(cp_file, sep="\t", low_memory=False)

        best_row = choose_ploidy_row(confints_df)

        if "ploidy.estimate" not in confints_df.columns:
            raise ValueError(f"Missing 'ploidy.estimate' column in {cp_file}")

        ploidy_dict[sample] = float(best_row["ploidy.estimate"])

    return ploidy_dict


def load_segments(sequenza_dir: Path, sample: str) -> pd.DataFrame:
    seg_file = sequenza_dir / sample / f"{sample}_segments.txt"
    df = pd.read_csv(seg_file, sep="\t", low_memory=False)

    required_cols = {"chromosome", "start.pos", "end.pos", "CNt"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in {seg_file}: {sorted(missing)}")

    return df


def format_seg_dataframe(df: pd.DataFrame, sample: str, seg_mean: pd.Series) -> pd.DataFrame:
    out = df.copy()
    out["ID"] = sample
    out["chrom"] = out["chromosome"].astype(str).str.replace("chr", "", regex=False)
    out["loc.start"] = out["start.pos"]
    out["loc.end"] = out["end.pos"]
    out["seg.mean"] = seg_mean

    return out[["ID", "chrom", "loc.start", "loc.end", "seg.mean"]]


def write_seg(df: pd.DataFrame, outfile: Path) -> None:
    outfile.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(outfile, sep="\t", index=False)


def main() -> None:
    args = parse_args()

    sequenza_dir = Path(args.sequenza_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()

    requested_samples = load_sample_list(args.sample_list)
    samples = discover_samples(sequenza_dir, requested_samples)

    if not samples:
        raise ValueError("No valid sample folders found.")

    ploidy_dict = load_ploidy_estimates(sequenza_dir, samples)

    relative_dir = output_dir / "relative_seg"
    absolute_dir = output_dir / "absolute_seg"

    for sample in samples:
        seg_df = load_segments(sequenza_dir, sample)

        relative_seg = format_seg_dataframe(
            df=seg_df,
            sample=sample,
            seg_mean=seg_df["CNt"] - ploidy_dict[sample],
        )
        write_seg(relative_seg, relative_dir / f"{sample}.seg")

        absolute_seg = format_seg_dataframe(
            df=seg_df,
            sample=sample,
            seg_mean=seg_df["CNt"] - 2,
        )
        write_seg(absolute_seg, absolute_dir / f"{sample}.seg")

    print(f"Exported {len(samples)} samples.")
    print(f"Relative SEG files: {relative_dir}")
    print(f"Absolute SEG files: {absolute_dir}")


if __name__ == "__main__":
    main()