import difflib


MATCH, DIFFER = True, False


def bitdiff(bits0, bits1):
    division_points = get_division_points(bits0, bits1)
    return split_bits(division_points, bits0, bits1)


def get_division_points(bits0, bits1):
    minlen = min(len(bits0), len(bits1))

    division_points = []
    state = MATCH
    for i in range(minlen):
        actual_state = bits0[i] == bits1[i]
        if actual_state == state:
            continue
        state = actual_state
        division_points.append(i)
    division_points.append(minlen)

    return division_points


def split_bits(division_points, *list_of_bits):
    results = [split_one_bit_sequence(division_points, bits)
               for bits in list_of_bits]
    return tuple(results)


def split_one_bit_sequence(division_points, bits):
    division_points = division_points[:]
    if not division_points or division_points[-1] != len(bits):
        division_points.append(len(bits))

    result = [bits[:division_points[0]]]
    for i in range(len(division_points)-1):
        result.append(bits[division_points[i]:division_points[i+1]])

    return tuple(result)


def diff(text0, text1):
    sm = difflib.SequenceMatcher(None, text0, text1)
    matching_blocks = list(sm.get_matching_blocks())[:-1]
    splitted0 = split_text(text0, matching_blocks, 0)
    splitted1 = split_text(text1, matching_blocks, 1)

    return splitted0, splitted1


def split_text(text, matching_blocks, index):
    pointer = 0
    splitted = []
    matching_blocks2 = [(mb[index], mb[2]) for mb in matching_blocks]
    for start, length in matching_blocks2:
        splitted.append(text[pointer:start])
        splitted.append(text[start:start+length])
        pointer = start + length
    if pointer != len(text):
        splitted.append(text[pointer:len(text)])
    normalize(splitted)
    return tuple(splitted)


def normalize(splitted):
    if splitted[0] == "":
        splitted.pop(0)
    else:
        splitted.insert(0, "")
