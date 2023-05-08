import argparse
import juni_core
import prompts

def read_files(filepaths):
    content = []
    for filepath in filepaths:
        with open(filepath, 'r') as file:
            content.append((filepath, file.read()))
    return content

def concatenate(command, files_content):
    result = f"{command}\n"
    for filepath, content in files_content:
        result += f"\n;;;<{filepath}>\n{content}\n;;;<{filepath}>\n"
    return result

def juni_edit(concatenated_string):
    result = juni_core.send_single_message(prompts.code_editor, concatenated_string, creative=False)
    return result

def write_files(files_content):
    for filepath, content in files_content:
        with open(filepath, 'w') as file:
            file.write(content)

def parse_result(result):
    files_content = []
    comments = []
    lines = result.split('\n')
    i = 0
    while i < len(lines):
        if lines[i].startswith(';;;<') and lines[i].endswith('>'):
            filepath = lines[i][4:-1]
            i += 1
            content = []
            while i < len(lines) and not (lines[i].startswith(';;;<') and lines[i].endswith('>')):
                content.append(lines[i])
                i += 1
            files_content.append((filepath, '\n'.join(content)))
            i += 1
        else:
            comments.append(lines[i])
            i += 1
    return '\n'.join(comments), files_content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process command and filepaths.')
    parser.add_argument('command', type=str, help='A command string')
    parser.add_argument('filepaths', nargs='*', help='One or more filepaths')
    parser.add_argument('--explain', action='store_true', help='Prevent writing to files')
    args = parser.parse_args()

    files_content = read_files(args.filepaths)
    concatenated = concatenate(args.command, files_content)
    result = juni_edit(concatenated)
    comments, files = parse_result(result)

    print(comments)

    if not args.explain:
        write_files(files)