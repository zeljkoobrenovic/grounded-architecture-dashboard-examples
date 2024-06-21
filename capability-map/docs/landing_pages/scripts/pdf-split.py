from pdf2image import convert_from_path

root = '/Users/user1/'


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



split_pdf('File1.pdf', 'Folder_1')
