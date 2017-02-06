import sys,re,openpyxl,os


def get_current_dir():
    global filename
    filename = "House Things to do.xlsx"
    global filename_dir
    filename_dir = r"C:\CSI"
    global current_dir
    current_dir = os.getcwd()
    print("The current working directory is %s " % current_dir)


def get_set_working_dir():
    if current_dir != filename_dir:
        os.chdir(filename_dir)
        working_dir = os.getcwd()
        print("Changed the current directory to match the directory where the file is located: %s " % working_dir)
    else:
        print("Current directory matches the directory where the file is located: %s " % current_dir)


def read_excel():
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.get_sheet_by_name("Sheet1")
    print(sheet)


def main():
    get_current_dir()
    get_set_working_dir()
    read_excel()


main()

