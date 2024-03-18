

corrected_code = '''static void free_suffix(bfuncinfo *finfo, bexpdesc *e)
{
    int idx = e->v.ss.idx;
    int nlocal = be_list_count(finfo->local);
    /* release suffix register */
    if (!isK(idx) && idx >= nlocal) {
        be_code_freeregs(finfo, 1);
    }
    /* release object register */
    if (e->v.ss.tt == ETREG && (int)e->v.ss.obj >= nlocal && (e->v.ss.obj + 1 >= finfo->freereg)) {
        be_code_freeregs(finfo, 1);
    }
}'''


def demo_1():
    buggy_repo = 'berry-5'

    # download repo data
    dataset_api.download_buggy_data_by_repo(buggy_repo)

    # get buggy code
    buggy_functions = dataset_api.get_buggy_function_by_repo(buggy_repo)
    print(f'{buggy_repo} buggy_function: {buggy_functions}')

    complete_codes = dataset_api.get_complete_buggy_codes_by_repo(buggy_repo)
    print(f'{buggy_repo} buggy_codes: {complete_codes}')

    # test
    # output initial test result
    print('-' * 20 + 'Initial' + '-' * 20)
    result = dataset_api.test_default_buggy_codes(buggy_repo)
    print('test_result:')
    print(f'{result.repo_name}: ')
    print(f'  build_result: {result.build_result}')
    print(f'  test_cases_result: ')
    print(f'    pass_rate: {result.test_cases_result.pass_rate}')
    print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
    print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')

    print('-' * 20 + 'Fixed' + '-' * 20)
    fixed_code = ' '
    # fixed_code = corrected_code
    result = dataset_api.test_buggy_codes(buggy_repo, fixed_code)
    print('test_result:')
    print(f'{result.repo_name}: ')
    print(f'  build_result: {result.build_result}')
    print(f'  test_cases_result: ')
    print(f'    pass_rate: {result.test_cases_result.pass_rate}')
    print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
    print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')


def demo_2():
    # search repair scenario 2 buggy repositories
    rs_2__repos = dataset_api.search_repositories_by_rs(RepairScenario.REPAIR_SCENARIO_2)

    # download repair scenario 2 buggy repositories
    dataset_api.download_buggy_data_by_rs(RepairScenario.REPAIR_SCENARIO_2)

    for buggy_repo in rs_2__repos:
        # get buggy function
        buggy_functions = dataset_api.get_buggy_function_by_repo(buggy_repo)
        print(f'{buggy_repo} buggy_function: {buggy_functions}')

        # test default buggy code
        print('-' * 20 + 'Initial' + '-' * 20)
        result = dataset_api.test_default_buggy_codes(buggy_repo)
        print('test_result:')
        print(f'{result.repo_name}: ')
        print(f'  build_result: {result.build_result}')
        print(f'  test_cases_result: ')
        print(f'    pass_rate: {result.test_cases_result.pass_rate}')
        print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
        print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')

        # test fixed code
        print('-' * 20 + 'Fixed' + '-' * 20)
        fixed_code = ' '
        result = dataset_api.test_buggy_codes(buggy_repo, fixed_code)
        print('test_result:')
        print(f'{result.repo_name}: ')
        print(f'  build_result: {result.build_result}')
        print(f'  test_cases_result: ')
        print(f'    pass_rate: {result.test_cases_result.pass_rate}')
        print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
        print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')


def get_safe_repair_scenario_list(index: int) -> list:
    # RS_1: single-line - invalid-condition: , num: 13
    repair_scenarios_1_safe = ['berry-5', 'cpp_peglib-4', 'cppcheck-8',
                               'cppcheck-9', 'cppcheck-11', 'cppcheck-25', 'exiv2-13', 'exiv2-15',
                               'libtiff-1', 'openssl-14', 'openssl-24', 'yara-1', 'yara-2']

    # RS_2: single-line - invalid-format-string: , num: 3
    repair_scenarios_2_safe = ['dlt_daemon-1', 'exiv2-20', 'yaml_cpp-6']

    # RS_3: single-line - memory-error: , num: 3
    repair_scenarios_3_safe = ['dlt_daemon-1', 'libtiff-1', 'ndpi-1']

    if index == 1:
        return repair_scenarios_1_safe
    elif index == 2:
        return repair_scenarios_2_safe
    elif index == 3:
        return repair_scenarios_3_safe
    else:
        raise RuntimeError("Hi Kid! You want to get something dangerous...")


def demo_3():
    rp1_list = get_safe_repair_scenario_list(1)  # get safe repair scenario 1
    rp2_list = get_safe_repair_scenario_list(2)  # get safe repair scenario 2
    rp3_list = get_safe_repair_scenario_list(3)  # get safe repair scenario 3

    for repo in rp3_list:
        result = dataset_api.test_default_buggy_codes_with_failed_tcs('cpp_peglib-8')
        print('test_result:')
        print(f'{result.repo_name}: ')
        print(f'  build_result: {result.build_result}')
        print(f'  test_cases_result: ')
        print(f'    pass_rate: {result.test_cases_result.pass_rate}')
        print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
        print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')
        print(f'    fail_test_cases_info: {result.test_cases_result.fail_test_cases_info}')

def demo_4():
    result = dataset_api.test_default_buggy_codes_with_failed_tcs('berry-5')
    print('test_result:')
    print(f'{result.repo_name}: ')
    print(f'  build_result: {result.build_result}')
    if not result.build_result:
        print(f'  build_output: {result.build_output}')
    print(f'  test_cases_result: ')
    print(f'    pass_rate: {result.test_cases_result.pass_rate}')
    print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
    print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')
    print(f'    fail_test_cases_info: {result.test_cases_result.fail_test_cases_info}')

    print('*' * 20)

    result = dataset_api.test_buggy_codes_with_failed_tcs('berry-5', 'abddww')
    print('test_result:')
    print(f'{result.repo_name}: ')
    print(f'  build_result: {result.build_result}')
    if not result.build_result:
        print(f'  build_output: {result.build_output}')
    print(f'  test_cases_result: ')
    print(f'    pass_rate: {result.test_cases_result.pass_rate}')
    print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
    print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')
    print(f'    fail_test_cases_info: {result.test_cases_result.fail_test_cases_info}')


def demo_rq3():
    rq3_repos = ['libtiff-1', 'libtiff-2', 'libtiff-3', 'libtiff-4', 'libtiff-5', 'berry-1', 'berry-2', 'berry-3',
                 'berry-4', 'berry-5', 'libucl-1', 'libucl-2', 'libucl-3', 'libucl-4', 'libucl-5', 'libucl-6']
    for repo in rq3_repos:
        print(dataset_api.get_buggy_function_by_repo_rq3(repo))
        print(dataset_api.get_buggy_function_with_label_repo_rq3(repo))
        result = dataset_api.test_buggy_codes_with_failed_tcs_rq3(repo, 'abcdedjelsjlje')
        print('test_result:')
        print(f'{result.repo_name}: ')
        print(f'  build_result: {result.build_result}')
        if not result.build_result:
            print(f'  build_output: {result.build_output}')
        print(f'  test_cases_result: ')
        print(f'    pass_rate: {result.test_cases_result.pass_rate}')
        print(f'    pass_test_cases: {result.test_cases_result.pass_test_cases}')
        print(f'    fail_test_cases: {result.test_cases_result.fail_test_cases}')
        print(f'    fail_test_cases_info: {result.test_cases_result.fail_test_cases_info}')


def main():
    demo_4()
    # demo_rq3()


if __name__ == "__main__":
    import dataset_api
    from dataset_api import RepairScenario
    main()