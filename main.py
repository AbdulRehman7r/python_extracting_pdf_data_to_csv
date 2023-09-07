from pdfquery import PDFQuery
import re
import csv

pdf = PDFQuery("g.pdf")
pdf.load()

res = pdf.extract(
    [
        ("with_formatter", "text"),
        (
            "reg_no",
            "LTTextLineHorizontal:in_bbox('124.91, 845.83, 196.57, 865.83')",
        ),
        (
            "roll_no",
            "LTTextLineHorizontal:in_bbox('23.2, 909.745, 169.91, 924.745')",
        ),
        ("cr#No", 'LTTextLineHorizontal:contains("CR#:")'),
    ],
    as_dict=False,
)

reg_no_list = re.findall("([0-9]{5})-([0-9]{4})-([0-9]{4})", res[0][1])
roll_no_list = re.findall("[0-9]{6}", res[1][1])
cr_no_list = re.findall("[0-9]+", res[2][1])

if (
    reg_no_list.__len__() == roll_no_list.__len__()
    and roll_no_list.__len__() == cr_no_list.__len__()
):
    print("Writing CSV File")
    # Writting Data to CSV FILE
    with open("result.csv", "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        # CSV FILE Header
        headers = ["Registration No", "Roll No", "CR No"]
        csv_writer.writerow(headers)
        # CSV FILE ENTRIES
        for index in range(len(reg_no_list)):
            f_reg_no = f"{reg_no_list[index][0]}-{reg_no_list[index][1]}-{reg_no_list[index][2]}"
            csv_writer.writerow([f_reg_no, roll_no_list[index], cr_no_list[index]])

else:
    print("Something went wrong when Extracting Data Debug it.....")
