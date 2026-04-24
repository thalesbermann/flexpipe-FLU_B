#!/usr/bin/env python3

import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
np.random.seed(SEED)

REGION_MAP = {
    "Brazil": "Latin America and the Caribbean",
    "Argentina": "Latin America and the Caribbean",
    "Chile": "Latin America and the Caribbean",
    "Colombia": "Latin America and the Caribbean",
    "Peru": "Latin America and the Caribbean",
    "Uruguay": "Latin America and the Caribbean",
    "Paraguay": "Latin America and the Caribbean",
    "Bolivia": "Latin America and the Caribbean",
    "Ecuador": "Latin America and the Caribbean",
    "Venezuela": "Latin America and the Caribbean",
    "Guyana": "Latin America and the Caribbean",
    "Suriname": "Latin America and the Caribbean",
    "French Guiana": "Latin America and the Caribbean",
    "Mexico": "Latin America and the Caribbean",
    "Guatemala": "Latin America and the Caribbean",
    "Belize": "Latin America and the Caribbean",
    "Honduras": "Latin America and the Caribbean",
    "El Salvador": "Latin America and the Caribbean",
    "Nicaragua": "Latin America and the Caribbean",
    "Costa Rica": "Latin America and the Caribbean",
    "Panama": "Latin America and the Caribbean",
    "Cuba": "Latin America and the Caribbean",
    "Jamaica": "Latin America and the Caribbean",
    "Haiti": "Latin America and the Caribbean",
    "Dominican Republic": "Latin America and the Caribbean",
    "Puerto Rico": "Latin America and the Caribbean",
    "Trinidad and Tobago": "Latin America and the Caribbean",

    "USA": "Northern America",
    "United States": "Northern America",
    "Canada": "Northern America",

    "United Kingdom": "Northern Europe",
    "Ireland": "Northern Europe",
    "Norway": "Northern Europe",
    "Sweden": "Northern Europe",
    "Finland": "Northern Europe",
    "Denmark": "Northern Europe",
    "Iceland": "Northern Europe",

    "France": "Western Europe",
    "Germany": "Western Europe",
    "Netherlands": "Western Europe",
    "Belgium": "Western Europe",
    "Luxembourg": "Western Europe",
    "Austria": "Western Europe",
    "Switzerland": "Western Europe",

    "Italy": "Southern Europe",
    "Spain": "Southern Europe",
    "Portugal": "Southern Europe",
    "Greece": "Southern Europe",
    "Croatia": "Southern Europe",
    "Serbia": "Southern Europe",
    "Slovenia": "Southern Europe",
    "Bosnia and Herzegovina": "Southern Europe",
    "Montenegro": "Southern Europe",
    "Albania": "Southern Europe",
    "North Macedonia": "Southern Europe",

    "Russia": "Eastern Europe",
    "Poland": "Eastern Europe",
    "Ukraine": "Eastern Europe",
    "Romania": "Eastern Europe",
    "Bulgaria": "Eastern Europe",
    "Czech Republic": "Eastern Europe",
    "Slovakia": "Eastern Europe",
    "Hungary": "Eastern Europe",
    "Belarus": "Eastern Europe",
    "Lithuania": "Eastern Europe",
    "Latvia": "Eastern Europe",
    "Estonia": "Eastern Europe",
    "Moldova": "Eastern Europe",

    "China": "Eastern Asia",
    "Japan": "Eastern Asia",
    "South Korea": "Eastern Asia",
    "North Korea": "Eastern Asia",
    "Mongolia": "Eastern Asia",
    "Taiwan": "Eastern Asia",
    "Hong Kong": "Eastern Asia",
    "Macau": "Eastern Asia",

    "Thailand": "South-eastern Asia",
    "Vietnam": "South-eastern Asia",
    "Malaysia": "South-eastern Asia",
    "Singapore": "South-eastern Asia",
    "Philippines": "South-eastern Asia",
    "Indonesia": "South-eastern Asia",
    "Cambodia": "South-eastern Asia",
    "Laos": "South-eastern Asia",
    "Myanmar": "South-eastern Asia",
    "Brunei": "South-eastern Asia",
    "Timor-Leste": "South-eastern Asia",

    "India": "Southern Asia",
    "Pakistan": "Southern Asia",
    "Bangladesh": "Southern Asia",
    "Nepal": "Southern Asia",
    "Bhutan": "Southern Asia",
    "Sri Lanka": "Southern Asia",
    "Maldives": "Southern Asia",
    "Afghanistan": "Southern Asia",

    "Saudi Arabia": "Western Asia",
    "United Arab Emirates": "Western Asia",
    "Qatar": "Western Asia",
    "Kuwait": "Western Asia",
    "Oman": "Western Asia",
    "Bahrain": "Western Asia",
    "Jordan": "Western Asia",
    "Israel": "Western Asia",
    "Lebanon": "Western Asia",
    "Turkey": "Western Asia",
    "Iraq": "Western Asia",
    "Iran": "Western Asia",
    "Yemen": "Western Asia",
    "Syria": "Western Asia",

    "Kenya": "Sub-Saharan Africa",
    "South Africa": "Sub-Saharan Africa",
    "Nigeria": "Sub-Saharan Africa",
    "Ghana": "Sub-Saharan Africa",
    "Uganda": "Sub-Saharan Africa",
    "Tanzania": "Sub-Saharan Africa",
    "Ethiopia": "Sub-Saharan Africa",
    "Mozambique": "Sub-Saharan Africa",
    "Zambia": "Sub-Saharan Africa",
    "Zimbabwe": "Sub-Saharan Africa",
    "Botswana": "Sub-Saharan Africa",
    "Namibia": "Sub-Saharan Africa",
    "Senegal": "Sub-Saharan Africa",
    "Cameroon": "Sub-Saharan Africa",
    "Democratic Republic of the Congo": "Sub-Saharan Africa",
    "Congo": "Sub-Saharan Africa",
    "Rwanda": "Sub-Saharan Africa",
    "Burundi": "Sub-Saharan Africa",
    "Angola": "Sub-Saharan Africa",
    "Madagascar": "Sub-Saharan Africa",

    "Australia": "Australia and New Zealand",
    "New Zealand": "Australia and New Zealand",

    "Papua New Guinea": "Melanesia",
    "Fiji": "Melanesia",
    "Solomon Islands": "Melanesia",
    "Vanuatu": "Melanesia",
    "New Caledonia": "Melanesia",
}


def normalize_country(country: str) -> str:
    if pd.isna(country):
        return ""
    country = str(country).strip()
    aliases = {
        "United States of America": "USA",
        "US": "USA",
        "U.S.A.": "USA",
        "Republic of Korea": "South Korea",
        "Korea, South": "South Korea",
        "Viet Nam": "Vietnam",
        "Russian Federation": "Russia",
        "UK": "United Kingdom",
    }
    return aliases.get(country, country)


def infer_region(country: str) -> str:
    country = normalize_country(country)
    return REGION_MAP.get(country, "Other")


def choose_best_accession_col(df: pd.DataFrame) -> str:
    candidates = ["Accession", "accession", "seqName", "strain", "name"]
    for col in candidates:
        if col in df.columns:
            return col
    for col in df.columns:
        if "accession" in col.lower():
            return col
    sys.exit("Erro: não encontrei coluna de acesso no metadata.")


def choose_best_date_col(df: pd.DataFrame) -> str:
    candidates = ["Collection_Date", "date", "collection_date"]
    for col in candidates:
        if col in df.columns:
            return col
    for col in df.columns:
        if "date" in col.lower():
            return col
    sys.exit("Erro: não encontrei coluna de data no metadata.")


def choose_best_country_col(df: pd.DataFrame) -> str:
    candidates = ["Country", "country", "geoLocCountry", "Location"]
    for col in candidates:
        if col in df.columns:
            return col
    for col in df.columns:
        if "country" in col.lower():
            return col
    sys.exit("Erro: não encontrei coluna de país no metadata.")


def detect_delimiter(path: Path) -> str:
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as fh:
        sample = fh.read(10000)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        return dialect.delimiter
    except Exception:
        counts = {d: sample.count(d) for d in [",", ";", "\t"]}
        return max(counts, key=counts.get)


def read_table_auto(path: Path) -> pd.DataFrame:
    sep = detect_delimiter(path)
    print(f"Lendo {path.name} com separador detectado: {repr(sep)}")
    try:
        return pd.read_csv(path, sep=sep, dtype=str, engine="python")
    except Exception as e:
        sys.exit(f"Erro ao ler {path} com separador {repr(sep)}: {e}")


def add_priority_columns(df: pd.DataFrame, accession_col: str, date_col: str) -> pd.DataFrame:
    df = df.copy()

    df["date_precision_score"] = 0
    df.loc[df[date_col].str.match(r"^\d{4}-\d{2}-\d{2}$", na=False), "date_precision_score"] = 3
    df.loc[df[date_col].str.match(r"^\d{4}-\d{2}$", na=False), "date_precision_score"] = 2
    df.loc[df[date_col].str.match(r"^\d{4}$", na=False), "date_precision_score"] = 1

    if "length" in df.columns:
        df["length_score"] = pd.to_numeric(df["length"], errors="coerce").fillna(0)
    elif "Length" in df.columns:
        df["length_score"] = pd.to_numeric(df["Length"], errors="coerce").fillna(0)
    else:
        df["length_score"] = 0

    df["clade_major"] = df["clade"].astype(str).str.split(".").str[0]
    df["accession_len_score"] = df[accession_col].astype(str).str.len()

    return df


def allocate_targets_by_stratum(df_global: pd.DataFrame, target_total: int) -> tuple[pd.DataFrame, int]:
    strata_counts = (
        df_global.groupby(["region", "year"])
        .size()
        .reset_index(name="n")
        .sort_values(["region", "year"])
        .reset_index(drop=True)
    )

    n_strata = len(strata_counts)
    if n_strata == 0:
        return strata_counts.assign(target=0), 0

    target_per_stratum = max(1, target_total // n_strata)
    strata_counts["target"] = strata_counts["n"].clip(upper=target_per_stratum)
    projected_total = int(strata_counts["target"].sum())

    return strata_counts, projected_total


def sample_stratum(group: pd.DataFrame, n_target: int) -> pd.DataFrame:
    group = group.copy()

    if len(group) <= n_target:
        return group

    sampled_parts = []

    # 1) Garante 1 por clado completo, do raro -> comum
    clade_counts = group["clade"].value_counts(dropna=False).sort_values()
    for clade in clade_counts.index.tolist():
        sub = group[group["clade"] == clade].copy()
        sub = sub.sort_values(
            by=["date_precision_score", "length_score", "Collection_Date"],
            ascending=[False, False, False]
        )
        sampled_parts.append(sub.head(1))

    sampled = pd.concat(sampled_parts).drop_duplicates(subset=["Accession"])

    if len(sampled) >= n_target:
        return sampled.sort_values(
            by=["date_precision_score", "length_score", "Collection_Date"],
            ascending=[False, False, False]
        ).head(n_target)

    # 2) Garante 1 por clado major entre os restantes, do raro -> comum
    remaining = group.loc[~group.index.isin(sampled.index)].copy()
    if len(remaining) > 0:
        major_parts = []
        major_counts = remaining["clade_major"].value_counts(dropna=False).sort_values()
        for clade_major in major_counts.index.tolist():
            sub = remaining[remaining["clade_major"] == clade_major].copy()
            sub = sub.sort_values(
                by=["date_precision_score", "length_score", "Collection_Date"],
                ascending=[False, False, False]
            )
            major_parts.append(sub.head(1))

        if major_parts:
            major_sampled = pd.concat(major_parts).drop_duplicates(subset=["Accession"])
            sampled = pd.concat([sampled, major_sampled]).drop_duplicates(subset=["Accession"])

    if len(sampled) >= n_target:
        return sampled.sort_values(
            by=["date_precision_score", "length_score", "Collection_Date"],
            ascending=[False, False, False]
        ).head(n_target)

    # 3) Completa com os abundantes, priorizando qualidade/recência
    remaining = group.loc[~group.index.isin(sampled.index)].copy()
    remaining = remaining.sort_values(
        by=["date_precision_score", "length_score", "Collection_Date"],
        ascending=[False, False, False]
    )

    n_needed = n_target - len(sampled)
    extra = remaining.head(n_needed)

    sampled = pd.concat([sampled, extra]).drop_duplicates(subset=["Accession"])
    return sampled


def cap_country_global(group: pd.DataFrame, max_per_country_global: int) -> pd.DataFrame:
    group = group.copy()
    if len(group) <= max_per_country_global:
        return group

    return group.sort_values(
        by=["date_precision_score", "length_score", "Collection_Date"],
        ascending=[False, False, False]
    ).head(max_per_country_global)


def cap_year(group: pd.DataFrame, max_per_year_global: int) -> pd.DataFrame:
    group = group.copy()
    if len(group) <= max_per_year_global:
        return group

    return group.sort_values(
        by=["date_precision_score", "length_score", "Collection_Date"],
        ascending=[False, False, False]
    ).head(max_per_year_global)


def main():
    parser = argparse.ArgumentParser(
        description="Subsample de Influenza B Victoria com merge de clados do Nextclade, uniformidade por região+ano e diversidade de clados."
    )
    parser.add_argument("--metadata", required=True, help="Metadata filtrado pós-QC")
    parser.add_argument("--nextclade", required=True, help="CSV/TSV de saída do Nextclade")
    parser.add_argument("--output-prefix", required=True, help="Prefixo dos arquivos de saída")
    parser.add_argument("--start-year", type=int, default=2010, help="Ano inicial")
    parser.add_argument("--target-size", type=int, default=2000, help="Tamanho alvo antes dos caps finais")
    parser.add_argument("--keep-country", default="Brazil", help="País focal a manter integralmente")
    parser.add_argument("--max-per-country-global", type=int, default=100, help="Cap máximo por país no conjunto global")
    parser.add_argument("--max-per-year-global", type=int, default=100, help="Cap máximo por ano no dataset final")
    args = parser.parse_args()

    metadata_path = Path(args.metadata)
    nextclade_path = Path(args.nextclade)

    if not metadata_path.exists():
        sys.exit(f"Erro: metadata não encontrado -> {metadata_path}")
    if not nextclade_path.exists():
        sys.exit(f"Erro: nextclade não encontrado -> {nextclade_path}")

    metadata = read_table_auto(metadata_path)
    nextclade = read_table_auto(nextclade_path)

    accession_col = choose_best_accession_col(metadata)
    date_col = choose_best_date_col(metadata)
    country_col = choose_best_country_col(metadata)

    if "seqName" not in nextclade.columns:
        sys.exit(f"Erro: nextclade precisa ter coluna 'seqName'. Colunas encontradas: {list(nextclade.columns)[:15]}")
    if "clade" not in nextclade.columns:
        sys.exit(f"Erro: nextclade precisa ter coluna 'clade'. Colunas encontradas: {list(nextclade.columns)[:15]}")

    print(f"Metadata inicial: {len(metadata):,}")
    print(f"Nextclade inicial: {len(nextclade):,}")

    metadata[accession_col] = metadata[accession_col].astype(str).str.strip()
    nextclade["seqName"] = nextclade["seqName"].astype(str).str.strip()
    nextclade["clade"] = nextclade["clade"].astype(str).str.strip()

    nextclade_small = nextclade[["seqName", "clade"]].drop_duplicates(subset=["seqName"]).copy()

    df = metadata.merge(
        nextclade_small,
        left_on=accession_col,
        right_on="seqName",
        how="left"
    )

    print(f"Após merge com Nextclade: {len(df):,}")

    df = df[df["clade"].notna()].copy()
    df["clade"] = df["clade"].astype(str).str.strip()

    # remove vazios e unassigned
    df = df[
        (df["clade"] != "") &
        (df["clade"].str.lower() != "unassigned")
    ].copy()

    print(f"Com clado disponível e sem unassigned: {len(df):,}")

    df = df.rename(columns={
        accession_col: "Accession",
        date_col: "Collection_Date",
        country_col: "Country"
    })

    df["Collection_Date"] = df["Collection_Date"].astype(str).str.strip()
    df["Country"] = df["Country"].astype(str).map(normalize_country)

    df = df[df["Collection_Date"].str.match(r"^\d{4}-\d{2}-\d{2}$", na=False)].copy()
    print(f"Após filtro de data completa: {len(df):,}")

    df["year"] = pd.to_numeric(df["Collection_Date"].str[:4], errors="coerce")
    df = df[df["year"].notna()].copy()
    df["year"] = df["year"].astype(int)

    df = df[df["year"] >= args.start_year].copy()
    print(f"Após filtro >= {args.start_year}: {len(df):,}")

    df = df[df["Country"].notna() & (df["Country"].str.strip() != "")].copy()
    print(f"Após remover Country vazio: {len(df):,}")

    df["region"] = df["Country"].map(infer_region)
    df = add_priority_columns(df, "Accession", "Collection_Date")

    with_clades_path = f"{args.output_prefix}_with_clades.tsv"
    df.to_csv(with_clades_path, sep="\t", index=False)
    print(f"Arquivo com clados salvo em: {with_clades_path}")

    keep_country_norm = normalize_country(args.keep_country)
    df["is_focal_country"] = df["Country"].eq(keep_country_norm)

    df_keep = df[df["is_focal_country"]].copy()
    df_global = df[~df["is_focal_country"]].copy()

    print(f"{keep_country_norm} mantido integralmente: {len(df_keep):,}")
    print(f"Pool global para subsampling: {len(df_global):,}")

    target_available = max(0, args.target_size - len(df_keep))
    strata_counts, projected_total = allocate_targets_by_stratum(df_global, target_available)

    print(f"Número de estratos region+year: {len(strata_counts):,}")
    print(f"Target disponível para o pool global: {target_available:,}")
    if len(strata_counts) > 0:
        print(f"Target por estrato escolhido: {int(strata_counts['target'].max())}")
    print(f"Total projetado para o pool global: {projected_total:,}")

    target_lookup = {
        (row["region"], row["year"]): int(row["target"])
        for _, row in strata_counts.iterrows()
    }

    sampled_groups = []
    for (region, year), group in df_global.groupby(["region", "year"], dropna=False):
        n_target = target_lookup.get((region, year), 0)
        if n_target <= 0:
            continue
        sampled_groups.append(sample_stratum(group, n_target))

    if sampled_groups:
        df_global_sampled = (
            pd.concat(sampled_groups, ignore_index=False)
            .drop_duplicates(subset=["Accession"])
            .copy()
        )
    else:
        df_global_sampled = df_global.head(0).copy()

    print(f"Após subsampling por region+year com diversidade de clado: {len(df_global_sampled):,}")

    df_global_capped = (
        df_global_sampled
        .groupby("Country", group_keys=False)
        .apply(lambda g: cap_country_global(g, args.max_per_country_global))
        .reset_index(drop=True)
    )

    print(f"Após cap por país ({args.max_per_country_global}): {len(df_global_capped):,}")

    df_final = pd.concat([df_keep, df_global_capped], ignore_index=True)
    df_final = df_final.drop_duplicates(subset=["Accession"]).copy()

    df_final = (
        df_final
        .groupby(df_final["Collection_Date"].str[:4], group_keys=False)
        .apply(lambda g: cap_year(g, args.max_per_year_global))
        .reset_index(drop=True)
    )

    print(f"Após cap por ano ({args.max_per_year_global}): {len(df_final):,}")

    print("\nResumo final")
    print("============")
    print(f"Total final: {len(df_final):,}")
    print(f"País focal mantido (antes dos caps finais): {len(df_keep):,}")

    print("\nTop 20 regiões no dataset final:")
    print(df_final["region"].value_counts().head(20).to_string())

    print("\nTop 20 países no dataset final:")
    print(df_final["Country"].value_counts().head(20).to_string())

    print("\nTop 20 clados no dataset final:")
    print(df_final["clade"].value_counts().head(20).to_string())

    print("\nDistribuição por ano (dataset final):")
    year_counts = df_final["Collection_Date"].str[:4].value_counts().sort_index()
    print(year_counts.to_string())

    print("\nDistribuição por ano (%)")
    year_perc = (year_counts / year_counts.sum() * 100).round(2)
    print(year_perc.to_string())

    final_path = f"{args.output_prefix}_subsampled.tsv"
    df_final.to_csv(final_path, sep="\t", index=False)
    print(f"\nArquivo final salvo em: {final_path}")

if __name__ == "__main__":
    main()
