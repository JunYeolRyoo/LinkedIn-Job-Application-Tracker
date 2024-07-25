from linkedin import LinkedIn
from make_excel import MakeExcelFile

def main():
    linkedin = LinkedIn()
    linkedin.get_updated_data()
    while True:
        user_inp = input("Enter the company name you want to search (press 'Q' to quit, 'F' to save as an Excel file): ").strip()
        if user_inp == "Q": break
        if user_inp == "F":
            make_file = MakeExcelFile(linkedin)
            make_file.make_excel()
            continue
        linkedin.get_application_info(user_inp)

if __name__ == "__main__":
    main()