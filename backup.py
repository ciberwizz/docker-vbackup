#!/usr/bin/env python3
import sys
import docker
from datetime import datetime
import tarfile

if __name__ == "__main__":
    client = docker.from_env()
    conts = {}
    now = datetime.now()
    mtime =  now.strftime("%Y-%m-%dT%H.%M.%S")

    for c in client.containers.list(filters={'status':'running'}):
        c_mounts = c.attrs["Mounts"]
        conts[c.id] = { 'name':c.name,'mounts':c_mounts}
        for m in c_mounts:
            bits, stat = c.get_archive(m['Destination'])#, encode_stream=True) #gzip
            print(stat)
            #mtime = stat["mtime"][0:19].replace(':','.')
            filename = c.name + '_' + stat["name"] + '_' + mtime +'.tar'
            with tarfile.open('./backups/' + filename +'.bz2','w:bz2') as tarf:
                tar_info = tarfile.TarInfo(filename)

                tarf.addfile(tar_info)

                for chunk in bits:
                    #print(chunk)
                    #f.write(chunk)
                    tarf.fileobj.write(chunk)
                

        
    