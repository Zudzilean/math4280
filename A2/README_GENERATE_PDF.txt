生成 PDF 的说明
================

我已经创建了一个独立的 Python 脚本：generate_assignment_pdf.py

使用方法：
----------
直接运行：
    python generate_assignment_pdf.py

脚本会：
1. 自动执行所有代码
2. 生成所有图片（保存在 assignment_images/ 文件夹）
3. 生成 Markdown 文件：Assignment2_Solutions.md
4. 生成 HTML 文件：Assignment2_Solutions.html

转换为 PDF：
-----------
方法1（推荐）：在浏览器中打开 HTML 并打印为 PDF
1. 双击打开 Assignment2_Solutions.html
2. 按 Ctrl+P 打开打印对话框
3. 选择 "另存为 PDF" 或 "Microsoft Print to PDF"
4. 点击保存

方法2：如果安装了 LaTeX，可以使用 jupyter nbconvert
    jupyter nbconvert --to pdf --execute A2_Complete_Solutions.ipynb

生成的文件：
-----------
- Assignment2_Solutions.md  (Markdown 格式)
- Assignment2_Solutions.html (HTML 格式，可直接打印为 PDF)
- assignment_images/ (所有图片文件夹)
