import os
import ctypes
from sys import platform
from datetime import datetime, timedelta

current_time = datetime.now()


if platform == "linux" or platform=="linux2":
        path = os.path.join(os.path.dirname(__file__))
        path += "/corex64/linux/Subdora.so"
        subdora_core = ctypes.CDLL(path)
elif platform == "win32":
        path = os.path.join(os.path.dirname(__file__))
        path += "/corex64/win/Subdora.dll"
        subdora_core = ctypes.CDLL(path)


mystique_encode_file_with_itr = subdora_core.Encode
mystique_encode_file_with_itr.argtypes = [ctypes.c_char_p,
                                              ctypes.c_size_t,
                                              ctypes.c_char_p,
                                              ctypes.c_char_p]
mystique_encode_file_with_itr.restype = None 

def subdora_encode_file(input_file_path:str,iterations:int=-100,exp_time = "INF"):
        if isinstance(input_file_path,str) and input_file_path[-3:]==".py" and os.path.exists(input_file_path):
            output_file_path = input_file_path[:-3]+".myst"
            if not isinstance(iterations,int):
                  print("[ERROR] invalid arguments")
                  return
            if exp_time != "INF":
                  if not (isinstance(exp_time,str) and (exp_time[-1] in ['m','h']) and isinstance(int(exp_time[:-1]),int)):
                        print("[ERROR] invalid arguments")
                        return 
                  if exp_time[-1]=='m':
                        current_time += timedelta(minutes=int(exp_time[:-1]))
                  elif exp_time[-1]=='h':
                        current_time += timedelta(hours=int(exp_time[:-1]))
                  exp_time = current_time.strftime("%a %b %d %H:%M:%S %Y")
            mystique_encode_file_with_itr(input_file_path.encode(),iterations,exp_time.encode(),output_file_path.encode())
        else:
            print("[ERROR] invalid arguments")


def subdora_encode_file_cli(input_file_path:str,iterations:int=-100,exp_time = "INF"):
            output_file_path = input_file_path[:-3]+".myst"
            mystique_encode_file_with_itr(input_file_path.encode(),iterations,exp_time.encode(),output_file_path.encode())
      

mystique_parse_file = subdora_core.Parse
mystique_parse_file.argtypes=[ctypes.c_char_p]

def subdora_parse(mystique_file_path:str):
        if isinstance(mystique_file_path,str) and os.path.exists(mystique_file_path):
            mystique_parse_file(mystique_file_path.encode())
        else:
              print("[ERROR] invalid arguments")
      
    


