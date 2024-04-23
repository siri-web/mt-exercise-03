#! usr/bin/env/ python3
# -*- coding: utf-8 -*-
# author: moritz.steiner2

import argparse
import re
import pandas as pd
import matplotlib.pyplot as plt


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--logfiles", type=str, required=True, nargs='+',
                        help="path to logfile(s) to plot out. Expected name is 'log_[value].csv")
    parser.add_argument("--type", type=str, required=True, default='v',
                        help="either 'v' for validation plot or 't' for test plot")
    parser.add_argument("--out", type=str, required=False,
                        help="path to saving source CSV for the plot")

    arguments = parser.parse_args()
    return arguments


def plot(dataframe):
        lines = dataframe.plot.line()
        plt.show()


def main():
    args = cli()
    # Test which perplexity type should be plotted (and saved)
    if args.type == 'v':
        ppl_type = "validation_perplexity"    
    elif args.type == 't':
        ppl_type = "training_perplexity"
    else:
        raise KeyError(f"Type argument unsopported: {args.type}. Choose either 'v' or 't'")

    temp_dict = {}

    # read each models logfile into a dataframe
    for file in args.logfiles:
        df = pd.read_csv(file)

        # this substitution removes everything from the file path name except the dropout amount
        dropout_amount = re.sub(r'.*/log_(\d\.?\d?).csv', r'Dropout \1', file)

        # add the log data of the chosen perplexity type to the temporary dictionary with the current dropout amount as key
        temp_dict[dropout_amount] = df[ppl_type]
    
    # create new aggregate dataframe out of all the chosen perplexity types values stored in the temporary dictionary
    plot_df = pd.DataFrame(temp_dict)
    plot(plot_df)

    # write the aggregate dataframe to a csv if specified
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as out_csv:
            epochs_column = [i+1 for i in range(40)]
            plot_df.insert(0, 'Epoch', epochs_column)
            plot_df.to_csv(out_csv, index=False)
            print("CSV saved")


if __name__ == "__main__":
    main()

