import os

import click
import numpy as np
import pandas as pd
import pyBigWig
from scipy.signal import argrelextrema
from scipy.stats import gaussian_kde
from sklearn.preprocessing import QuantileTransformer

from bioseba.util import divide, read_fa


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--data_dir_path", help="Folder path for insulation score files (.bw)", type=str
)
@click.option("--fasta_path", type=str)
@click.option("--output_path", type=str)
def prepross(data_dir_path, fasta_path, output_path):
    file_paths = [
        os.path.join(data_dir_path, file)
        for _, _, files in os.walk(data_dir_path, topdown=False)
        for file in files
    ]

    insulation_scores = None
    for file_path in file_paths:
        bw = pyBigWig.open(file_path)
        insulation_score = pd.DataFrame()
        for chrom in bw.chroms():
            _insulation_score = pd.DataFrame(
                bw.intervals(chrom),
                columns=[
                    "start",
                    "end",
                    os.path.splitext(os.path.basename(file_path))[0],
                ],
            )
            _insulation_score["chrom"] = chrom
            insulation_score = pd.concat([insulation_score, _insulation_score])
        insulation_score = insulation_score.set_index(["chrom", "start", "end"])

        if insulation_scores is None:
            insulation_scores = insulation_score
        else:
            insulation_scores = pd.concat([insulation_scores, insulation_score], axis=1)
    insulation_scores = insulation_scores.sort_index()

    cdbs = insulation_scores.copy()
    fa_dic = read_fa(fasta_path)

    def _generate_sequence(series):
        chrom, start, end = series.name
        return fa_dic[chrom][start:end]

    cdbs["sequence"] = cdbs.apply(_generate_sequence, axis=1)

    cdbs.to_csv(output_path, sep="\t")


@cli.command()
@click.option("--file_path", type=str, help="The path of the file to be processed")
@click.option("--output_path", type=str)
@click.option(
    "--valtest_percentage",
    default=0.2,
    type=float,
    help="Percentage of data used for val",
)
@click.option("--random_seed", default=42, type=int)
def create_dataset(file_path, output_path, valtest_percentage, random_seed):
    raw_datas = pd.read_csv(file_path, sep="\t")

    for chrom in raw_datas["chrom"].unique():
        for column in raw_datas.columns.drop(["chrom", "start", "end", "sequence"]):
            q1 = raw_datas.loc[raw_datas["chrom"] == chrom, column].quantile(0.25)
            _data = raw_datas.loc[
                (raw_datas["chrom"] == chrom) & (raw_datas[column] <= q1),
                ["start", column],
            ].copy()
            local_min_indices = argrelextrema(_data[column].values, np.less)[0]
            raw_datas.loc[
                (raw_datas["chrom"] == chrom)
                & (raw_datas["start"].isin(_data["start"].iloc[local_min_indices])),
                column,
            ] = 1
            raw_datas.loc[
                (raw_datas["chrom"] == chrom)
                & (~raw_datas["start"].isin(_data["start"].iloc[local_min_indices])),
                column,
            ] = 0
    raw_datas["SCI-CDB"] = raw_datas.drop(
        columns=["chrom", "start", "end", "sequence"]
    ).sum(axis=1)

    datas = pd.DataFrame()
    for chrom in raw_datas["chrom"].unique():
        _data = raw_datas.loc[raw_datas["chrom"] == chrom, ["start", "SCI-CDB"]].copy()
        _kde = gaussian_kde(_data["SCI-CDB"], bw_method=5)
        _peaks = _kde.pdf(_data["SCI-CDB"])
        local_max_indices = argrelextrema(_peaks, np.less)[0]
        _data = raw_datas.loc[
            (raw_datas["chrom"] == chrom)
            & (raw_datas["start"].isin(_data["start"].iloc[local_max_indices]))
        ].copy()
        datas = pd.concat([datas, _data])

    datas = datas[~datas["sequence"].str.contains("N")]

    quantile_transformer = QuantileTransformer(
        output_distribution="normal", random_state=random_seed
    )
    datas["label"] = quantile_transformer.fit_transform(
        np.expand_dims(datas["SCI-CDB"].values, axis=-1)
    ).flatten()
    datas = datas[datas["label"] > -4]

    train, val = divide(datas, valtest_percentage, random_seed)
    train.to_csv(os.path.join(output_path, "train.csv"))
    val.to_csv(os.path.join(output_path, "dev.csv"))


if __name__ == "__main__":
    cli()
