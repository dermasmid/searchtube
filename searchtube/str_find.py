def list_find(heystack: list, needle: list):
    heystack_index = 0
    needle_index = 0
    results = []
    for i in heystack:
        heystack_index +=1
        if i == needle[needle_index]:
            needle_index += 1
        else:
            needle_index = 0
        if needle_index == len(needle):
            results.append(list(range(heystack_index - needle_index, heystack_index)))
            needle_index = 0

    return results



def split_find(heystack: str, needle: str):
    results = []
    global_index = 0
    needle_space_len = needle.count(' ')
    needle_word_len = len(needle.split(' '))
    data = heystack.split(needle)
    data_len = len(data)
    for i, result in enumerate(data):
        global_index += result.count(' ')
        if (not result.endswith(' ') and result) or (not data_len == i + 1 and not data[i + 1].startswith(' ')):
            continue
        results.append(list(range(global_index, global_index + needle_word_len)))
        global_index += needle_space_len
    return results
