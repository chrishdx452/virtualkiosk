import pandas as pd
import os

path_dir_einzugsfiles = os.path.join(os.getcwd(), 'Einzugslisten')
curr_file = r"220805 EZ 730.csv"

global_df = pd.read_csv(os.path.join(path_dir_einzugsfiles, curr_file), sep=';')
global_df = global_df[global_df['V-Art'].str.match("Basis")] # Nur Neueinzügler

path_bereichsfile = os.path.join(os.getcwd(), "bereiche_zu_bungalows.csv")
bereich_df = pd.read_csv(path_bereichsfile, sep=';')

def parse_hh(bereich):
    df = global_df[global_df['VO-Nr.'].str.match(".*-7" + bereich + "-.*")] # Filter by apartment regex

    df2 = df['VO-Nr.'].str.split("-", expand=True)
    # df2.rename(columns={2: 'Stockwerk', 3: 'Nummer'}, inplace=True)
    df2.sort_values([2, 3], inplace=True)
    return zip([bereich for _ in range(len(df))], df2[2] + df2[3])

def parse_bungalow(bereich):
    df = global_df[global_df['VO-Nr.'].str.match("730-03-0.*")]

    df2 = df['VO-Nr.'].str.split("-", expand=True)
    df2.rename(columns={2: 'Reihe', 3: 'Nummer'}, inplace=True)
    df2['Reihe'] = df2['Reihe'].str[1]
    df2['Nummer'] = df2['Nummer'].astype(int)

    # Match Row to row for Correct Area
    joined_df = df2.merge(
        bereich_df.loc[bereich_df['Bereich'] == bereich],
        on=['Reihe', 'Nummer'],
        how='inner',
        sort=True
    )

    return zip(joined_df['Reihe'], joined_df['Nummer'])

def parse_stufenbauten(bereich):
    df = global_df[global_df['VO-Nr.'].str.match("730-0[A-E]-.*")]

    df2 = df['VO-Nr.'].str.split("-", expand=True)
    df2.rename(columns={1: 'Reihe', 2: 'Nummer'}, inplace=True)
    df2['Reihe'] = df2['Reihe'].str[1]
    df2['Nummer'] = (df2['Nummer'].str[1] + df2[3]).astype(int)

    df2.sort_values(['Reihe', 'Nummer'], inplace=True)

    return zip(df2['Reihe'], df2['Nummer'])

def parse_function(bereich):
    if bereich == "HJK":
        return parse_stufenbauten, bereich

    assert len(bereich) == 1, "Bereich kann nur für HJK Länge 3 haben"

    if bereich in "AB":
        return parse_hh, bereich
    if bereich in "CDEFG":
        return parse_bungalow, bereich
    
    raise ValueError("Diesen Bereich gibt es nicht!")

if __name__ == '__main__':
    bereich = input("Was ist dein Bereich?: ").upper()
    bereich_func, bereich = parse_function(bereich)
    print("\nDas sind deine Neueinzügler:\n")
    for args in bereich_func(bereich):
        print("{} {}".format(*args))