from pdf2image import convert_from_path

root = 'product_reviews/pdfs/'


def split_pdf(pdf_filename, export_dir):
    path = root + pdf_filename
    print('Loading PDF: ' + path)
    pages = convert_from_path(path, 500)

    count = 0
    for page in pages:
        count += 1
        export_file = '../' + export_dir + '/' + str(count) + '.png'
        page.save(root + export_file, 'PNG')
        print('Exporting ' + export_file)


# split_pdf('PR_10_2023_05.pdf', 'PR_10')
# split_pdf('PR_09_2023_03.pdf', 'PR_09')
# split_pdf('PR_08_2023_01.pdf', 'PR_08')
# split_pdf('PR_07_2022_11.pdf', 'PR_07')
# split_pdf('PR_06_2022_09.pdf', 'PR_06')
# split_pdf('PR_05_2022_06.pdf', 'PR_05')
# split_pdf('PR_04_2022_03.pdf', 'PR_04')
# split_pdf('PR_03_2021_12.pdf', 'PR_03')
# split_pdf('PR_11_1.pdf', 'PR_11')
# split_pdf('PR_11_2.pdf', 'PR_11')
# split_pdf('PR_01_2021_07.pdf', 'PR_01')
split_pdf('PR_12_2023_10.pdf', 'PR_12')
