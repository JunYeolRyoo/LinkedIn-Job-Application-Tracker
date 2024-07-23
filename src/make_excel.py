from openpyxl import Workbook
from openpyxl.styles import Alignment
from linkedin import LinkedIn

class MakeExcelFile():
    def __init__(self, data):
        self.applied_jobs = data.appliedJobs
    
    def make_excel(self):
        wb = Workbook()
        ws = wb.active

        headers = ["Company", "Applied time", "Role", "Location"]
        ws.merge_cells("A1:C1")
        ws.merge_cells("D1:E1")
        ws.merge_cells("F1:I1")
        ws.merge_cells("J1:M1")

        ws["A1"] = "Company"
        ws["D1"] = "Date"
        ws["F1"] = "Role"
        ws["J1"] = "Location"
        ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
        ws['D1'].alignment = Alignment(horizontal='center', vertical='center')
        ws['F1'].alignment = Alignment(horizontal='center', vertical='center')
        ws['J1'].alignment = Alignment(horizontal='center', vertical='center')
        
        ind = 2
        for comp in self.applied_jobs:
            ws.merge_cells(f"A{ind}:C{ind+len(self.applied_jobs[comp])-1}")
            ws[f"A{ind}"] = comp
            for detail in self.applied_jobs[comp]:
                ws.merge_cells(f"D{ind}:E{ind}")
                ws.merge_cells(f"F{ind}:I{ind}")
                ws.merge_cells(f"J{ind}:M{ind}")
                ws[f"D{ind}"] = detail[1]
                ws[f"F{ind}"] = detail[0]   # role element
                ws[f"J{ind}"] = detail[2]
                ws[f"A{ind}"].alignment = Alignment(horizontal='center', vertical='center')
                ws[f"D{ind}"].alignment = Alignment(horizontal='center', vertical='center')
                ws[f"F{ind}"].alignment = Alignment(horizontal='center', vertical='center')
                ws[f"J{ind}"].alignment = Alignment(horizontal='center', vertical='center')
                ind += 1

        wb.save("job_applications.xlsx")
        print("Excel file has been created.\n")
        
