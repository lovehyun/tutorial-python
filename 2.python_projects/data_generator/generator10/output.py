import csv


def save_to_csv(data):
    filename = None
    header = None
    rows = []
    
    for item in data:
        if filename is None:  # 첫 번째 항목의 경우에만 파일명 설정
            filename = item.get_csv_filename()
            header = item.get_csv_header()
        rows.append(item.get_row())  # 중복된 작업 대신 rows 리스트에 항목 추가
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(rows)
        
    print(f"데이터가 {filename} 파일로 저장되었습니다.")


def print_data_item(item):
    item.print_data()

def print_data(data, output_format):
    if output_format == "stdout":
        for item in data:
            # print(item)
            print(", ".join([str(getattr(item, attr)) for attr in item.__dict__.keys()]))
    elif output_format == "console":
        for item in data:
            print_data_item(item)
    elif output_format == "csv":
        save_to_csv(data)
    else:
        print("지원되지 않는 아웃풋 형태입니다.")
