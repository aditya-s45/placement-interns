with open('src/intern_engine/telegram_notify.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith("    text = '") and "join(lines)" not in line:
        lines[i] = "    text = '\\n'.join(lines)\n"
    elif "'.join(lines)" in line and line.strip() == "'.join(lines)":
        lines[i] = ""

with open('src/intern_engine/telegram_notify.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
