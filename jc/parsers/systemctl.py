"""jc - JSON CLI output utility systemctl Parser

Usage:
    specify --systemctl as the first argument if the piped input is coming from systemctl

Examples:

    $ systemctl -a | jc --systemctl -p
    [
      {
        "unit": "proc-sys-fs-binfmt_misc.automount",
        "load": "loaded",
        "active": "active",
        "sub": "waiting",
        "description": "Arbitrary Executable File Formats File System Automount Point"
      },
      {
        "unit": "dev-block-8:2.device",
        "load": "loaded",
        "active": "active",
        "sub": "plugged",
        "description": "LVM PV 3klkIj-w1qk-DkJi-0XBJ-y3o7-i2Ac-vHqWBM on /dev/sda2 2"
      },
      {
        "unit": "dev-cdrom.device",
        "load": "loaded",
        "active": "active",
        "sub": "plugged",
        "description": "VMware_Virtual_IDE_CDROM_Drive"
      },
      ...
    ]
"""
import jc.utils


def process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (dictionary) raw structured data to process

    Returns:

        dictionary   structured data with the following schema:

        [
          {
            "unit":          string,
            "load":          string,
            "active":        string,
            "sub":           string,
            "description":   string
          }
        ]
    """
    # nothing more to process
    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) output preprocessed JSON if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        dictionary   raw or processed structured data
    """

    # compatible options: linux, darwin, cygwin, win32, aix, systemctlbsd
    compatible = ['linux']

    if not quiet:
        jc.utils.compatibility(__name__, compatible)

    linedata = data.splitlines()
    # Clear any blank lines
    linedata = list(filter(None, linedata))
    # clean up non-ascii characters, if any
    cleandata = []
    for entry in linedata:
        cleandata.append(entry.encode('ascii', errors='ignore').decode())

    header_text = cleandata[0]
    header_list = header_text.lower().split()

    raw_output = []

    for entry in cleandata[1:]:
        if entry.find('LOAD   = ') != -1:
            break

        else:
            entry_list = entry.split(maxsplit=4)
            output_line = dict(zip(header_list, entry_list))
            raw_output.append(output_line)

    if raw:
        return raw_output
    else:
        return process(raw_output)
