import argparse
import os 
from datetime import datetime , timedelta  
from ._subdora import subdora_parse , subdora_encode_file_cli



def main():
    parser = argparse.ArgumentParser(description="8")

    parser.add_argument("--obfuscate", type=str, help="python file going to be obfuscated")
    parser.add_argument("--run",type=str,help=".myst file to run")
    parser.add_argument("--itr",type=int,help="iteration counter")
    parser.add_argument("--time",type=str,help="time of expiry")

    args = parser.parse_args()

    py_file_arg , myst_file_arg , itr_arg , time_arg = args.obfuscate , args.run , args.itr , args.time 

    if py_file_arg!=None and py_file_arg[-3:]==".py" and os.path.exists(os.path.abspath(py_file_arg)):
        py_file = py_file_arg 
        #going to obfuscate the fule usign func 1
        if itr_arg==None:
            itr = -100
        if time_arg==None:
            expiry_time = "INF"
        if itr_arg!=None and isinstance(itr_arg,int):
            itr = itr_arg 
        if time_arg!=None and isinstance(time_arg, str) and (time_arg[-1] in ['m','h']) and isinstance(int(time_arg[:-1]), int):
            current_time = datetime.now()
            if time_arg[-1]=='m':
                current_time += timedelta(minutes=int(time_arg[:-1]))
            elif time_arg[-1]=='h':
                current_time += timedelta(hours=int(time_arg[:-1]))
            expiry_time = current_time.strftime("%a %b %d %H:%M:%S %Y")
        
        subdora_encode_file_cli(py_file,int(itr),expiry_time)
        return

    if myst_file_arg!=None and myst_file_arg[-5:]==".myst" and os.path.exists(myst_file_arg):
        myst_file = myst_file_arg
        # goint to run the myst file func 2
        # dont care about other arguments 
        subdora_parse(myst_file)
        return

