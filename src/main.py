from linkedin import LinkedIn
from make_excel import MakeExcelFile

def main():
    linkedin = LinkedIn()
    mkfile = MakeExcelFile()
    if mkfile.check_excel_existence():
        print("here")
        linkedin.set_applied_jobs(mkfile.load_excel())
    linkedin.get_updated_data()
    while True:
        user_inp = input("Enter the company name you want to search (press 'Q' to quit, 'F' to save as an Excel file): ").strip()
        if user_inp == "Q": break
        if user_inp == "F":
            # make_file = MakeExcelFile(linkedin)
            mkfile.make_excel(linkedin.get_applied_jobs(),linkedin.get_company_names())
            continue
        linkedin.get_application_info(user_inp)

if __name__ == "__main__":
    main()