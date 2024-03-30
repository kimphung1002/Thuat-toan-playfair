import tkinter as tk
from tkinter import ttk

def generate_matrix(key):
    matrix = [[''] * 5 for _ in range(5)]
    key = key.replace('j', 'i')
    key = ''.join(sorted(set(key), key=key.index))
    letters = 'abcdefghiklmnopqrstuvwxyz'

    row, col = 0, 0
    for char in key:
        matrix[row][col] = char
        col += 1
        if col == 5:
            col = 0
            row += 1

    for char in letters:
        if char not in key:
            matrix[row][col] = char
            col += 1
            if col == 5:
                col = 0
                row += 1

    return matrix

def format_message(msg):
    msg = msg.lower().replace('j', 'i')
    formatted = []
    for i in range(0, len(msg), 2):
        chunk = msg[i:i+2]
        if len(chunk) == 2 and chunk[0] == chunk[1]:
            chunk = chunk[0] + 'x' + chunk[1]
        formatted.append(chunk)
    if len(msg) % 2 != 0:
        formatted.append('x')
    return ''.join(formatted)

def get_position(char, matrix):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col

def encrypt(message, matrix):
    ciphertext = []
    for i in range(0, len(message), 2):
        char1, char2 = message[i], message[i+1]
        row1, col1 = get_position(char1, matrix)
        row2, col2 = get_position(char2, matrix)

        if row1 == row2:
            ciphertext.append(matrix[row1][(col1 + 1) % 5])
            ciphertext.append(matrix[row2][(col2 + 1) % 5])
        elif col1 == col2:
            ciphertext.append(matrix[(row1 + 1) % 5][col1])
            ciphertext.append(matrix[(row2 + 1) % 5][col2])
        else:
            ciphertext.append(matrix[row1][col2])
            ciphertext.append(matrix[row2][col1])

    return ''.join(ciphertext)

def decrypt(ciphertext, matrix):
    plaintext = []
    for i in range(0, len(ciphertext), 2):
        char1, char2 = ciphertext[i], ciphertext[i+1]
        row1, col1 = get_position(char1, matrix)
        row2, col2 = get_position(char2, matrix)

        if row1 == row2:
            plaintext.append(matrix[row1][(col1 - 1) % 5])
            plaintext.append(matrix[row2][(col2 - 1) % 5])
        elif col1 == col2:
            plaintext.append(matrix[(row1 - 1) % 5][col1])
            plaintext.append(matrix[(row2 - 1) % 5][col2])
        else:
            plaintext.append(matrix[row1][col2])
            plaintext.append(matrix[row2][col1])

    return ''.join(plaintext)

def process():
    message = message_entry.get().strip()
    key = key_entry.get().strip()

    matrix = generate_matrix(key)
    formatted_msg = format_message(message)

    if operation_var.get() == 'Encrypt':
        result = encrypt(formatted_msg, matrix)
    else:
        result = decrypt(formatted_msg, matrix)

    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, result)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Playfair Cipher")

# Tạo frame cho đầu vào
input_frame = ttk.LabelFrame(root, text="Input")
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Nhãn và trường nhập liệu cho văn bản
message_label = ttk.Label(input_frame, text="Message:")
message_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
message_entry = ttk.Entry(input_frame, width=30)
message_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Nhãn và trường nhập liệu cho khóa
key_label = ttk.Label(input_frame, text="Key:")
key_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
key_entry = ttk.Entry(input_frame, width=30)
key_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Lựa chọn phép thực hiện
operation_label = ttk.Label(input_frame, text="Operation:")
operation_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
operation_var = tk.StringVar(value="Encrypt")
operation_combobox = ttk.Combobox(input_frame, textvariable=operation_var, values=["Encrypt", "Decrypt"])
operation_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Nút xử lý
process_button = ttk.Button(root, text="Process", command=process)
process_button.grid(row=1, column=0, padx=10, pady=10)

# Khu vực hiển thị kết quả
result_text = tk.Text(root, width=40, height=10)
result_text.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()
