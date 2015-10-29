import argparse

def create_parser():

    description = ["A GUI for makeing changes to the OpSim version 4 confiiguration system."]

    parser = argparse.ArgumentParser(usage="opsim4_config_ui [options]",
                                     description=" ".join(description),
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-s", "--save-dir", dest="save_dir", help="Set the save directory for the "
                        "configuration override files. Default is the current directory.")

    return parser
