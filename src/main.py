from LinkedIn import LinkedIn

def main():
    link = LinkedIn()
    link.get_updated_data()
    while True:
        user_inp = input("Enter a company name you want to search in: ").strip().lower()
        link.get_application_info(user_inp)

if __name__ == "__main__":
    main()



