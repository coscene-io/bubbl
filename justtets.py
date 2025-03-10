print("hello world 123")
print("666")
# 九九乘法表
def multiplication_table():
    for i in range(1, 10):
        for j in range(1, i + 1):
            print(f"{j}*{i}={i * j}", end="\t")
        print()

# 调用函数打印九九乘法表
multiplication_table()
