#TODO generally make formatting better to fit the quality of the source material
#TODO see the entire file for todos on various assumptions that need to be fixed, this code is not reliable in edge cases (like an empty table)
import subprocess
import sys

import libzfs
zfsr = libzfs.ZFS()

#A halfassed table implementation
transpose = lambda m: zip(*m)
def dict_table(obj, default_cols=None):
    #https://github.com/freenas/py-libzfs/issues/63
    obj = list(obj)
    if len(obj) == 0:
      return []
    header = obj[0].properties.keys()
    rows = [ [ v.value for v in o.properties.values()] for o in obj ]
    #TODO ugh
    _table = [header] + rows
    _table = list(transpose(sorted([c for c in transpose(_table) if c[0] in default_cols], key=lambda i: i[0] != "name" ))) #sort columns; name needs to be first so interactions work right
    header, rows = _table[0], _table[1:]
    return table(header, rows)

##
def prop_table(obj):
    return table(["NAME", "PROPERTY", "VALUE", "SOURCE"], obj ) #why is .properties a dict but .features a list generator

def prop(obj):
    return [ [obj.name,k,v.value,v.source.name] for k,v in obj.properties.items() ]

def feat(obj): #TODO source column	
    return [ [obj.name,"feature@" + f.name,f.state.name,"-"] for f in obj.features ]

##
def table(header, rows):
    table = [header] + rows
    padding = "  "
    col_widths = [max(len(cell) + len(padding) for cell in wascolumn) for wascolumn in transpose(table)]
    return ["".join((cell + padding).ljust(w) for cell,w in zip(row, col_widths)) for row in table]

##
def readCommand(cmd):
    stdout = subprocess.check_output(cmd, universal_newlines=True)
    return stdout.splitlines()

######
## Via API
def zfsListVolumes(): #TODO consider readding the unfiltered #TODO forgot what this means
    return dict_table(filter(lambda i: i.type.name == "VOLUME", zfsr.datasets), default_cols=["name", "used", "available", "referenced", "compressratio", "quota", "reservation", "mountpoint"])

def zfsListFilesystems():
    return dict_table(filter(lambda i: i.type.name == "FILESYSTEM", zfsr.datasets), default_cols=["name", "used", "available", "referenced", "compressratio", "quota", "reservation", "mountpoint"])

def zfsListSnapshots():
    return dict_table(zfsr.snapshots, default_cols=["name", "used", "compressratio", "referenced", "written"])

def zfsListSnapshotsOf(dataset):
    return dict_table(filter(lambda i: i.parent.name == dataset, zfsr.snapshots), default_cols=["name", "creation", "used", "compressratio", "referenced", "written"])

def zfsListPools():
    # TODO assuming that all pools have the same set of properties, and that we have at least one pool
    #TODO too wide and header doesnt scroll
    return dict_table(zfsr.pools, default_cols=["name", "size", "allocated", "free", "capacity", "fragmentation", "dedupratio" , "health"]) #alloc cap frag dedup

def zfsPoolProperties(poolname):
    return prop_table(prop(next(filter(lambda i: i.name == poolname, zfsr.pools))) + feat(next(filter(lambda i: i.name == poolname, zfsr.pools))))

def zfsDatasetProperties(datasetname):
    return prop_table(prop(next(filter(lambda i: i.name == datasetname, zfsr.datasets))))

def zfsSnapshotProperties(snapshotname): #TODO fix inherited to show source of inherit like in original
    return prop_table(next(filter(lambda i: i.name == snapshotname, zfsr.snapshots)))

## Via CLI

def zfsPoolHistory(poolname): #Note needs sudo
    return readCommand(["zpool", "history", poolname])

def zfsPoolIostat(poolname): #TODO add histogram thingies
    return readCommand(["zpool", "iostat", "-v", poolname])

#####

def check_zfs_executables():
    try:
        cmd = ["zpool", "list"]
        stdout = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
    except FileNotFoundError as e:
        sys.exit("zpool command not found in path")
    except subprocess.CalledProcessError as e:
        sys.exit(e.output)

    try:
        cmd = ["zfs", "list"]
        stdout = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT)
    except FileNotFoundError as e:
        sys.exit("zfs command not found in path")
    except subprocess.CalledProcessError as e:
        sys.exit(e.output)
