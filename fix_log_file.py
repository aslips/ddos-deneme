input_file = "loglar.csv"
output_file = "loglar_cleaned.csv"


header = "timestamp;ip;endpoint;response_time_ms;label;hour;ip_class;user_agent_type\n"

with open(input_file, "r") as file:
    lines = file.readlines()


cleaned_lines = [line for line in lines if line.count(";") == 7]

with open(output_file, "w") as file:
    file.write(header)  
    file.writelines(cleaned_lines)

print(f" Temiz dosya '{output_file}' olarak oluşturuldu. Satır sayısı: {len(cleaned_lines)}")
