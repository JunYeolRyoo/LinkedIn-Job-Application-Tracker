from openpyxl import Workbook
from openpyxl.styles import Alignment
from linkedin import LinkedIn

class MakeExcelFile():
    """
    A class to create an Excel file from job application data.
    """

    def __init__(self, data):
        """
        Initialize the MakeExcelFile class with the given data.

        Parameters:
        - data: An object that has an 'appliedJobs' attribute containing job application details
        """
        self.applied_jobs = data.appliedJobs
        self.companies_name = data.companyNames
    
    def make_excel(self):
        """
        Create an Excel file with job application data.

        The method performs the following:
        - Merges header cells for better readability.
        - Applies alignment for better readability.
        - Iterates over job application data, merges cells for each job application, and populates them.
        - Saves the workbook as 'job_applications.xlsx'.
        """
        wb = Workbook()
        ws = wb.active

        # Merge header cells
        ws.merge_cells("A1:C1")
        ws.merge_cells("D1:E1")
        ws.merge_cells("F1:I1")
        ws.merge_cells("J1:M1")

        # Set the header names
        ws["A1"] = "Company"
        ws["D1"] = "Applied Time"
        ws["F1"] = "Role"
        ws["J1"] = "Location"

        # Apply alignment to header cells for center alignment
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
        ws['D1'].alignment = Alignment(horizontal='center', vertical='center')
        ws['F1'].alignment = Alignment(horizontal='center', vertical='center')
        ws['J1'].alignment = Alignment(horizontal='center', vertical='center')
        
        ind = 2
        try:
            for comp in self.applied_jobs:
                ws.merge_cells(f"A{ind}:C{ind+len(self.applied_jobs[comp])-1}")
                ws[f"A{ind}"] = self.companies_name[comp]
                for detail in self.applied_jobs[comp]:
                    ws.merge_cells(f"D{ind}:E{ind}")    # Merge 2 columns
                    ws.merge_cells(f"F{ind}:I{ind}")    # Merge 4 columns
                    ws.merge_cells(f"J{ind}:M{ind}")    # Merge 4 columns
                    ws[f"D{ind}"] = detail[1]   # applied_date
                    ws[f"F{ind}"] = detail[0]   # role element
                    ws[f"J{ind}"] = detail[2]   # location

                    # Apply alignment to the data cells for center alignment
                    ws[f"A{ind}"].alignment = Alignment(horizontal='center', vertical='center')
                    ws[f"D{ind}"].alignment = Alignment(horizontal='center', vertical='center')
                    ws[f"F{ind}"].alignment = Alignment(horizontal='center', vertical='center')
                    ws[f"J{ind}"].alignment = Alignment(horizontal='center', vertical='center')
                    ind += 1

            wb.save("job_applications.xlsx") # Save the workbook to a file
        except Exception as e:
            print("Exception occured: ", e)
        else:
            print("Excel file has been created.\n")
