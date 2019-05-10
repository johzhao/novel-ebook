import io


def typesetting(lines: list, indent: bool = True) -> str:
    dest = io.StringIO()
    for line in lines:
        line = typesetting_line(line, indent)
        dest.write(line)
    dest.seek(0)
    return dest.read()


def typesetting_line(line: str, first_indent: bool = True) -> str:
    line = line.strip()
    if first_indent:
        line = f'　　{line}\n'
    else:
        line = f'{line}\n'
    return line
