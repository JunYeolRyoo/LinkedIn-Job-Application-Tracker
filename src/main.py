from linkedin import LinkedIn
from make_excel import MakeExcelFile

def main():
    linkedin = LinkedIn()
    linkedin.get_updated_data()
    while True:
        user_inp = input("Enter a company name you want to search in (press q to quit, press f to make as an Excel file): ").strip().lower()
        if user_inp in "qQ": break
        if user_inp == "f":
            make_file = MakeExcelFile(linkedin)
            make_file.make_excel()
            continue
        linkedin.get_application_info(user_inp)

if __name__ == "__main__":
    main()