def ParseRunList(run_numbers):
    processed_list = []
    for run in run_numbers:
        processed_list.append(run * 10)
    return processed_list
