import os
import time


class ErrorHandler:
    def __init__(self,dir_path):
        path=dir_path+"/Err_Msg.txt"
        self.err_msgs=[]
        self.dir_path=dir_path
        self.txt_path=path
        if os.path.isdir(dir_path) and os.path.isfile(path):
            os.remove(path)

    def addErr(self,err_msgs):
        self.err_msgs.append(err_msgs)

    def getErrs(self):
        return self.err_msgs

    def to_txt(self):
        if len(self.err_msgs)!=0:
            if not os.path.isdir(self.dir_path):
                os.makedirs(self.dir_path)
            file = open(self.txt_path, "a+")
            file.write("["+time.asctime(time.localtime(time.time()))+"]")
            for err in self.err_msgs:
                file.write('\n\t> '+err)
            file.write("\n")
            file.close()
            self.err_msgs=[]