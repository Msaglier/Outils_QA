def clean_lines_in_file(file):
    # remove empty lines from a file
    with open(file, 'r') as f:
        lines = f.readlines()
        clean_lines = [l.strip() for l in lines if l.strip()]

    with open(file, 'w') as f:
        f.writelines('\n'.join(clean_lines))

    print('>>>> Blank lines removed from {}.'.format(file))
