"""
App's main
"""
import argparse
import csv
import os
import shutil
import sys
import traceback

from ssllabsscan.report_template import REPORT_HTML
from ssllabsscan.ssllabs_client import SUMMARY_COL_NAMES, SSLLabsClient

SUMMARY_CSV = "summary.csv"
SUMMARY_HTML = "summary.html"
VAR_TITLE = "{{VAR_TITLE}}"
VAR_DATA = "{{VAR_DATA}}"
DEFAULT_TITLE = "SSL Labs Analysis Summary Report"
DEFAULT_STYLES = "styles.css"


def output_summary_html(input_csv, output_html):
    print(f"Creating {output_html} ...")

    data = ""
    with open(input_csv, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].startswith("#"):
                data += "  <tr>\n\t<th>{}</th>\n  </tr>".format('</th>\n\t<th>'.join(row))
            else:
                data += '\n  <tr class="{}">\n\t<td>{}</td>\n  </tr>'.format(row[2][:1], '</td>\n\t<td>'.join(row))

    # Replace the target string
    content = REPORT_HTML
    content = content.replace(VAR_TITLE, DEFAULT_TITLE)
    content = content.replace(VAR_DATA, data)

    # Write the file out again
    with open(output_html, "w") as file:
        file.write(content)

    # copy styles.css
    styles_css = os.path.join(os.path.dirname(output_html), DEFAULT_STYLES)
    if not os.path.exists(styles_css):
        shutil.copyfile(os.path.join(os.path.dirname(__file__), DEFAULT_STYLES), styles_css)


def process(
    server_list_file,
    email,
    check_progress_interval_secs=30,
    summary_csv=SUMMARY_CSV,
    summary_html=SUMMARY_HTML
):
    ret = 0
    # read from input file
    with open(server_list_file) as f:
        content = f.readlines()
    servers = [x.strip() for x in content if x.strip()]

    with open(summary_csv, "w") as outfile:
        # write column names to file
        outfile.write("#{}\n".format(",".join(str(s) for s in SUMMARY_COL_NAMES)))

    for server in servers:
        try:
            print(f"Start analyzing {server}...")
            SSLLabsClient(email, check_progress_interval_secs).analyze(server, summary_csv)
        except Exception as e:
            traceback.print_exc()
            ret = 1

    output_summary_html(summary_csv, summary_html)
    return ret

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="SSL Labs Scan")
    parser.add_argument(
        "inputfile",
        help="Input file containing list of servers to scan",
    )
    parser.add_argument(
        "-e",
        "--email",
        dest="email",
        help="Registered-email required for Qualys SSLLabs API v4",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        default=SUMMARY_HTML,
        help="Output file containing summary of scan results",
    )
    parser.add_argument(
        "-s",
        "--summary",
        dest="summary",
        default=SUMMARY_CSV,
        help="Output file containing summary of scan results",
    )
    parser.add_argument(
        "-p",
        "--progress",
        dest="progress",
        default=30,
        help="Progress check interval in seconds",
    )
    return parser.parse_args()

def main():
    """
    Entry point of the app.
    """
    args = parse_args()
    return process(
        server_list_file=args.inputfile,
        email=args.email,
        check_progress_interval_secs=args.progress,
        summary_csv=args.summary,
        summary_html=args.output,
    )


if __name__ == "__main__":
    sys.exit(main())
