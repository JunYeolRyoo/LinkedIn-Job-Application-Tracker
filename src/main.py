from LinkedIn import LinkedIn

def main():
    linkedin = LinkedIn()
    linkedin.get_updated_data()
    while True:
        user_inp = input("Enter a company name you want to search in (press q to quit): ").strip().lower()
        if user_inp in "qQ": break
        linkedin.get_application_info(user_inp)

if __name__ == "__main__":
    main()