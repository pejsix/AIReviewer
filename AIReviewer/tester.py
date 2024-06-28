def apply_change_to_file(selected_file, line_index_start, line_index_end, new_block):
    with open(selected_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        # Split the new block into lines
        new_lines = new_block.split('\n')
        # Replace the old block with the new block
        updated_lines = lines[:line_index_start] + new_lines + lines[line_index_end + 1:]
        # Write the updated content back to the file
        with open(selected_file, 'w', encoding='utf-8') as file:
            file.writelines('\n'.join(updated_lines) + '\n')

if __name__ == "__main__":
    selected_file = "C:\\Users\\trusi\\OneDrive\\Počítač\\test_file.txt"
    line_index_start = 3
    line_index_end = 6
    new_block = "Line Replaced\nLineReplaced"
    apply_change_to_file(selected_file, line_index_start, line_index_end, new_block)
