import os
import sys
from datetime import datetime
#
# _text=''
# _err=''


def writeRecords(_text, output_path,engine, total_count, actual_count, flag):
    if flag:
        if output_path:
            #writepath = "/Users/chandrayogyadav/Desktop/data.json"  ### define path to you desired location for file
            writepath = output_path
            mode = 'a' if os.path.exists(writepath) else 'w+'
            with open(writepath+"/records.txt", mode) as f:
                f.write("\n")
                f.write( "Logged at:" + str(datetime.now()) +" Total Records Returned by - " + engine  +":" + str(total_count))
                f.write("\n")
                f.write("Logged at:" + str(datetime.now()) + " Records Captured by - " + engine + ":" + str(actual_count))
                f.write("\n")
                f.close()
        else:
            try:
                if os.path.exists("records.txt"):
                    #os.remove("records.txt")
                    f = open("records.txt", "a")

                    f.write("\n")
                    f.write("Logged at:" + str(datetime.now()) + " Total Records Returned by - " + engine + ":" + str(total_count))
                    f.write("\n")
                    f.write("Logged at:" + str(datetime.now()) + " Records Captured by - " + engine + ":" + str(actual_count))
                    f.write("\n")
                    f.close()
                else:
                    f = open("records.txt", "x")
                    f.write("\n")
                    f.write("Logged at:" + str(datetime.now()) + " Total Records Returned by - " + engine + ":" + str(total_count))
                    f.write("\n")
                    f.write("Logged at:" + str(datetime.now()) + " Records Captured by - " + engine + ":" + str(actual_count))
                    f.write("\n")
                    f.close()
            except Exception as e:  # raise e
                #pass
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                writeError(e, None, engine, flag, filename, line_number)


def writeError(_err, output_path, engine, flag, *args):
    if flag:
        if output_path:
            # writepath = "/Users/chandrayogyadav/Desktop/data.json"  ### define path to you desired location for file
            writepath = output_path
            mode = 'a' if os.path.exists(writepath) else 'w+'
            with open(writepath + "/ErrorLog.txt", mode) as f:
                f.write("\n")
                for var in args:
                    f.write("Logged at:" + str(datetime.now()) + " Error returned by - " + engine + ":" + str(_err)+" location/line: "+  str(var))
                    f.write("\n")
                f.close()
        else:
            try:
                if os.path.exists("ErrorLog.txt"):
                    #os.remove("ErrorLog.txt")
                    f = open("ErrorLog.txt", "a")
                    f.write("\n")
                    if args:
                        for var in args:
                            f.write("\n")
                            f.write("Logged at:" + str(datetime.now()) + " Error returned by - " + engine + ":" + str(_err) + " location/line: " +
                                    str(var))
                            f.write("\n")
                        f.close()
                    else:
                        f.write("\n")
                        f.write("Logged at:" + str(datetime.now()) + " Error returned by - " + engine + ":" + str(
                            _err))
                        f.write("\n")
                        f.close()

                else:
                    f = open("ErrorLog.txt", "x")
                    f.write("\n")
                    if args:
                        for var in args:
                            f.write("\n")
                            f.write("Logged at:" + str(datetime.now()) + " Error returned by - " + engine + ":" + str(_err) + " location/line: "+
                                    str(var))
                            f.write("\n")
                        f.close()
                    else:
                        f.write("\n")
                        f.write("Logged at:" + str(datetime.now()) + " Error returned by - " + engine + ":" + str(
                            _err))
                        f.write("\n")
                        f.close()
            except Exception as e:  # raise e
                pass
                #print("Output file:", e)