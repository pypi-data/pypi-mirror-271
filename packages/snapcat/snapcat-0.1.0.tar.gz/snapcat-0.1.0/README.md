# SnapCAT

**snapcat** is a Python command-line tool that helps manage Chia Address Tokens (CATs). The tool communicates locally with the Chia Full Node RPC. The tool also leverages code from [chia-network](https://twitter.com/chia_project)'s [CAT-addresses](https://github.com/Chia-Network/CAT-addresses).

```
❯ snapcat --help

 Usage: snapcat [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────────╮
│ --version              Show the version and exit.                                  │
│ --file-name  -f  TEXT  The name of the database file (default: <tail_hash>.db)     │
│ --help                 Show this message and exit.                                 │
╰────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────╮
│ export     Export the CAT holder as csv or json.                                   │
│ show       Display the CAT db information.                                         │
│ sync       Sync or create (if not exist) the CAT holder database.                  │
╰────────────────────────────────────────────────────────────────────────────────────╯
```

### Sync (i.e., generate CAT database)
```
❯ snapcat sync --help

 Usage: snapcat sync [OPTIONS]

 Sync or create (if not exist) the CAT holder database.

╭─ Options ──────────────────────────────────────────────────────────────────────────╮
│ *  --tail-hash  -t  TEXT  The TAIL hash of CAT [required]                          │
│    --help                 Show this message and exit.                              │
╰────────────────────────────────────────────────────────────────────────────────────╯

❯ snapcat -f dbx.db sync -t "db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20"
press Ctrl+C to exit.
tail hash: db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
database file name: dbx.db
Full Node is synced
Processed all blocks from 0 to 5320121
```

### Export
```
❯ snapcat export --help

 Usage: snapcat export [OPTIONS]

 Export the CAT holder as csv or json.

╭─ Options ──────────────────────────────────────────────────────────────────────────╮
│ --output  -o  TEXT  The name of the output file (default: <tail_hash>-<block>.csv  │
│                     or .json)                                                      │
│ --coins   -c        Show individual coins in output rather than collapsing on      │
│                     puzzle hash                                                    │
│ --json    -j        Export as JSON instead of CSV                                  │
│ --help              Show this message and exit.                                    │
╰────────────────────────────────────────────────────────────────────────────────────╯


❯ snapcat -f dbx.db export --json -o dbx.json
Exporting CAT holders
Tail Hash: db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
Last Block Height: 5319876
```

### Show 
```
❯ snapcat show --help

 Usage: snapcat show [OPTIONS]

 Display the CAT db information.

╭─ Options ──────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                            │
╰────────────────────────────────────────────────────────────────────────────────────╯

❯ snapcat -f dbx.db show
Tail Hash: db1a9020d48d9d4ad22631b66ab4b9ebd3637ef7758ad38881348c5d24c38f20
# of Coins Spent: 152873
# of Coins Created: 158309
Last Block Height: 5319876
```