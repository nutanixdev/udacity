#!/usr/bin/env python3

import sys
import os
from datetime import datetime
import glob
import json
import humanize
from dotty_dict import dotty
from EvaluationItem import EvaluationItem
from EnvironmentOptions import EnvironmentOptions
from Messages import Messages


def pretty_time():
    '''
    display the current time
    '''
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def search_json(data, target):
    '''
    recursive function to search for a specific key
    with matching value in the BP JSON
    '''
    if isinstance(data, list):
        for elem in data:
            yield from search_json(elem, target)
    if isinstance(data, dict):
        if target in data.keys():
            yield data
        for key, value in data.items():
            yield from search_json(value, target)


def eval_criteria(EvalCriteria: EvaluationItem):
    '''
    function to evaluate a specific set of blueprint criteria
    '''

    '''
    for each set of criteria passed, we need to check
    what type of check we are doing.  this dictates how the
    found value is compared to the expected value
    e.g. 'instances' will expect the criteria to be a list
    or dict, and so on
    '''
    passed = False
    found_message = ''
    if EvalCriteria.eval_type == 'instances':
        if len(EvalCriteria.criteria) == EvalCriteria.expected:
            passed = True
            found_message = len(EvalCriteria.criteria)
        else:
            passed = False
            found_message = len(EvalCriteria.criteria)
    elif EvalCriteria.eval_type == 'number':
        pass
    elif EvalCriteria.eval_type == 'string':
        if EvalCriteria.match_type == 'exact':
            if EvalCriteria.criteria == EvalCriteria.expected:
                passed = True
                found_message = 'matches'
            else:
                passed = False
                found_message = 'no matches'
        else:
            if EvalCriteria.expected in EvalCriteria.criteria:
                passed = True
                found_message = 'matches'
            else:
                passed = False
                found_message = 'no matches'

    if passed:
        prefix = messages.passed
        summary = True
    else:
        prefix = messages.fail
        summary = True

    '''
    now that the evaluation item has been processed,
    we can display the results
    '''
    if summary:
        if environment_options.debug:
            print(f'{prefix} '
                  + f'{EvalCriteria.eval_type} | '
                  + f'{EvalCriteria.match_type} | '
                  + f'{EvalCriteria.description} | '
                  + 'Expected '
                  + f'{EvalCriteria.expected} '
                  + f'| Found {found_message}')
        else:
            print(f'{prefix} '
                  + f'{EvalCriteria.eval_type} | '
                  + f'{EvalCriteria.match_type} | '
                  + f'{EvalCriteria.description} | '
                  + 'Expected '
                  + f'{EvalCriteria.expected} ')


def show_result(passed: bool, title: str,
                expected: str = None,
                found: str = None):
    '''
    simple function to show the results of a specific
    evaluation pass
    '''
    if environment_options.debug:
        print(f'{messages.passed} | '
              + f'{title} | '
              + f'{expected} | '
              + f'{found}' if passed
              else f'{messages.fail} | '
              + f'{title} | '
              + f'{expected} | '
              + f'{found}')
    else:
        print(f'{messages.passed} | '
              + f'{title}' if passed
              else
              f'{messages.fail} | '
              + f'{title}')


def process_json(bp: str):
    '''
    process the blueprint
    '''
    print(f'{messages.line}')
    # verify the specified blueprint exists
    if os.path.exists(f'{bp}'):
        print(f'{messages.info} Blueprint found.  Continuing.')
        # with the blueprint found, verify that it is valid JSON
        print(f'{messages.info} Validating JSON content of {bp}.')
        try:
            with open(f'{bp}', 'r') as json_file:
                bp_json = json.loads(json_file.read())

                '''
                test listcomp on the processed JSON file
                please leave this line here for now
                '''
                '''
                vcpus = ([[x["create_spec"]["resources"]["num_sockets"]
                         for x in
                         bp_json["spec"]["resources"]
                         ["substrate_definition_list"]
                         if "num_sockets" in
                         x["create_spec"]["resources"]]])
                '''

                # the specified JSON file has been opened and parsed as JSON
                # it can now be processed
                print(f'{messages.info} {bp} parsed successfully.  '
                      + 'Processing.')
                # cleanup file handles
                json_file.close()

                '''
                ----------------------
                evaluation starts here
                ----------------------
                '''

                with open(f'{environment_options.criteria}', 'r') as criteria_file:
                    json_criteria = json.loads(criteria_file.read())
                    bp_dot = dotty(bp_json)
                    try:
                        for eval_key in json_criteria["criteria"]:
                            # entity lists
                            if eval_key['type'] == 'entity_lists':
                                for entity in eval_key['lists']:
                                    correct = len(bp_dot[entity['key']])
                                    if correct == entity['expected']:
                                        show_result(True, entity['key_desc'],
                                                    'Expected '
                                                    f'{entity["expected"]}',
                                                    f'Found {correct}')
                                    else:
                                        show_result(False, entity['key_desc'],
                                                    'Expected '
                                                    f'{entity["expected"]}',
                                                    f'Found {correct}')
                            # disk images
                            if eval_key['type'] == 'source_uri':
                                for image in bp_dot[eval_key['key']]:
                                    if 'options' in image:
                                        image_dot = dotty(image)
                                        if 'resources' in image_dot['options']:
                                            if ('source_uri' in image_dot['options.resources']):
                                                if eval_key['match'] == 'contains':
                                                    if eval_key['expected'] in image_dot['options.resources.source_uri']:
                                                        show_result(True, eval_key['description'],
                                                                    f'Expected {eval_key["expected"]}',
                                                                    'Found match')
                                                    else:
                                                        show_result(False, eval_key['description'],
                                                                    f'Expected {eval_key["expected"]}',
                                                                    'Found match')
                                                else:
                                                    if eval_key['expected'] == image_dot['options.resources.source_uri']:
                                                        show_result(True, eval_key['description'],
                                                                    f'Expected {eval_key["expected"]}',
                                                                    'Found match')
                                                    else:
                                                        show_result(False, eval_key['description'],
                                                                    f'Expected {eval_key["expected"]}',
                                                                    'Found match')
                            # aws ami and aws instance type
                            elif eval_key['type'] == 'image_id' or eval_key['type'] == 'instance_type':
                                for package in search_json(bp_json, eval_key['type']):
                                    correct = package[eval_key['type']]
                                    if correct in eval_key['expected']:
                                        show_result(True, eval_key['description'],
                                                    'Expected match in list',
                                                    f'Found {correct}')
                                    else:
                                        show_result(False, eval_key['description'],
                                                    'Expected match in list',
                                                    'No matches found')
                            # ahv vm names
                            elif eval_key['type'] == 'ahv_server_names':
                                for vm in search_json(bp_json, 'create_spec'):
                                    if 'name' in vm:
                                        if vm['type'].lower() == 'ahv_vm':
                                            vm_dot = dotty(vm)
                                            correct = vm_dot['create_spec.name'].lower()
                                            if correct in eval_key['expected']:
                                                show_result(True, eval_key['description'],
                                                            'Expected match in list',
                                                            f'Found {correct}')
                                            else:
                                                show_result(False, eval_key['description'],
                                                            'Expected match in list',
                                                            f'Found {correct}')
                            # aws vm names
                            elif eval_key['type'] == 'aws_server_names':
                                for vm in search_json(bp_json, 'create_spec'):
                                    if 'name' in vm:
                                        if vm['type'].lower() == 'aws_vm':
                                            vm_dot = dotty(vm)
                                            correct = vm_dot['create_spec.name'].lower()
                                            if correct in eval_key['expected']:
                                                show_result(True, eval_key['description'],
                                                            'Expected match in list',
                                                            f'Found {correct}')
                                            else:
                                                show_result(False, eval_key['description'],
                                                            'Expected match in list',
                                                            f'Found {correct}')
                            # web max replicas
                            elif eval_key['type'] == 'web_max_replicas':
                                for vm in search_json(bp_json, 'max_replicas'):
                                    vm_dot = dotty(vm)
                                    for each in eval_key['names']:
                                        if vm_dot['substrate_local_reference.name'].lower() == each:
                                            if int(vm_dot['max_replicas']) == eval_key['expected']:
                                                show_result(True, eval_key['description'],
                                                            f'Expected {eval_key["expected"]}',
                                                            f'Found {vm_dot["max_replicas"]}')
                                            else:
                                                show_result(False, eval_key['description'],
                                                            f'Expected {eval_key["expected"]}',
                                                            f'Found {vm_dot["max_replicas"]}')
                            # web min replicas
                            elif eval_key['type'] == 'web_min_replicas':
                                for vm in search_json(bp_json, 'min_replicas'):
                                    vm_dot = dotty(vm)
                                    for each in eval_key['names']:
                                        if vm_dot['substrate_local_reference.name'].lower() == each:
                                            if int(vm_dot['min_replicas']) == eval_key['expected']:
                                                show_result(True, eval_key['description'],
                                                            f'Expected {eval_key["expected"]}',
                                                            f'Found {vm_dot["min_replicas"]}')
                                            else:
                                                show_result(False, eval_key['description'],
                                                            f'Expected {eval_key["expected"]}',
                                                            f'Found {vm_dot["min_replicas"]}')
                            # cloud-init data status
                            elif eval_key['type'] == "cloud_init":
                                for vm in search_json(bp_json, "user_data"):
                                    vm_dot = dotty(vm)
                                    # aws vm
                                    if "instance_type" in vm_dot:
                                        if eval_key['expected']['aws_data'] in vm_dot['user_data']:
                                            show_result(True, f'AWS: {eval_key["description"]}',
                                                        f'Expected {eval_key["expected"]["aws_data"].encode(encoding="UTF-8")}',
                                                        'Found match')
                                        else:
                                            show_result(False, f'AWS: {eval_key["description"]}',
                                                        f'Expected {eval_key["expected"]["aws_data"].encode(encoding="UTF-8")}',
                                                        'Found no matching data')
                                    # ahv vm
                                    else:
                                        if eval_key['expected']['ahv_data'] in vm_dot['user_data']:
                                            show_result(True, f'AHV: {eval_key["description"]}',
                                                        f'Expected {eval_key["expected"]["ahv_data"].encode(encoding="UTF-8")}',
                                                        'Found match')
                                        else:
                                            show_result(False, f'AHV: {eval_key["description"]}',
                                                        f'Expected {eval_key["expected"]["ahv_data"].encode(encoding="UTF-8")}',
                                                        'Found no matching data')
                            # credentials
                            elif eval_key['type'] == 'credentials':
                                for credential in bp_dot[eval_key['key']]:
                                    cred_type = credential['type'].lower()
                                    username = credential['username'].lower()
                                    if cred_type in eval_key['expected']['types'] and username in eval_key['expected']['usernames']:
                                        show_result(True, f'{eval_key["description"]}',
                                                    'Expected matches in list',
                                                    f'Found credential of type {cred_type} and username as {username}')
                                    else:
                                        show_result(False, f'{eval_key["description"]}',
                                                    'Expected matches in list',
                                                    f'Found credential of type {cred_type} and username as {username}')
                            # course 2 vm sizing
                            elif eval_key['type'] == 'c2_sizing':
                                for substrate in bp_dot[eval_key['key']]:
                                    for size in eval_key['vm_sizes']:
                                        if substrate['create_spec']['name'].lower() == size['specs']['name'].lower():
                                            if substrate['create_spec']['resources']['num_vcpus_per_socket'] == size['specs']['vm_spec']['num_vcpus_per_socket']:
                                                show_result(True, f'{eval_key["description"]} - '
                                                            + f'{size["specs"]["spec_desc"]} num vCPUS Per Socket',
                                                            f'Expected {size["specs"]["vm_spec"]["num_vcpus_per_socket"]}',
                                                            f'Found {substrate["create_spec"]["resources"]["num_vcpus_per_socket"]}')
                                            else:
                                                show_result(False, f'{eval_key["description"]} - '
                                                            + f'{size["specs"]["spec_desc"]} num vCPUS Per Socket',
                                                            f'Expected {size["specs"]["vm_spec"]["num_vcpus_per_socket"]}',
                                                            f'Found {substrate["create_spec"]["resources"]["num_vcpus_per_socket"]}')
                                            if substrate['create_spec']['resources']['num_sockets'] == size['specs']['vm_spec']['num_sockets']:
                                                show_result(True, f'{eval_key["description"]} - '
                                                            + f'{size["specs"]["spec_desc"]} Num Sockets',
                                                            f'Expected {size["specs"]["vm_spec"]["num_sockets"]}',
                                                            f'Found {substrate["create_spec"]["resources"]["num_sockets"]}')
                                            else:
                                                show_result(False, f'{eval_key["description"]} - '
                                                            + f'{size["specs"]["spec_desc"]} Num Sockets',
                                                            f'Expected {size["specs"]["vm_spec"]["num_sockets"]}',
                                                            f'Found {substrate["create_spec"]["resources"]["num_sockets"]}')
                                            if substrate['create_spec']['resources']['memory_size_mib'] == size['specs']['vm_spec']['memory_size_mib']:
                                                show_result(True, f'{eval_key["description"]} - '
                                                            + f'{size["specs"]["spec_desc"]} Memory MiB',
                                                            f'Expected {size["specs"]["vm_spec"]["memory_size_mib"]}',
                                                            f'Found {substrate["create_spec"]["resources"]["memory_size_mib"]}')
                                            else:
                                                show_result(False, f'{eval_key["description"]} - '
                                                            + f'{size["specs"]["spec_desc"]} Memory MiB',
                                                            f'Expected {size["specs"]["vm_spec"]["memory_size_mib"]}',
                                                            f'Found {substrate["create_spec"]["resources"]["memory_size_mib"]}')
                            # course 3 vm sizing and specs
                            elif eval_key['type'] == 'c3_sizing':
                                for size in eval_key['vm_sizes']:

                                    # vm count per profile
                                    vms = ([x for x in
                                            bp_dot[eval_key['key']]
                                            if size['size'] in x["name"].lower()
                                            and "num_sockets" in
                                            x["create_spec"]["resources"]])
                                    if len(vms) == size['count']:
                                        show_result(True, f'{eval_key["description"]} - {size["specs"]["spec_desc"]} ({size["size"]})',
                                                    f'Expected {size["count"]}',
                                                    f'Found {len(vms)}')
                                    else:
                                        show_result(False, f'{eval_key["description"]} - {size["specs"]["spec_desc"]} ({size["size"]})',
                                                    f'Expected {size["count"]}',
                                                    f'Found {len(vms)}')

                                    # credential verification/security standards
                                    cred_checks = ([x for x in
                                                   bp_dot[eval_key['key']]
                                                   if x["readiness_probe"]['login_credential_local_reference']['name'].lower() == size["specs"]["credential_name"]
                                                   and size["specs"]["partial_name"] in x["create_spec"]["name"].lower()])
                                    if len(cred_checks) > 0:
                                        show_result(True, f'{size["specs"]["spec_desc"]} Security Standards',
                                                    f'Expected credential named {size["specs"]["credential_name"]}',
                                                    'Found matches')

                                '''
                                for substrate in bp_dot[eval_key['key']]:
                                    if 'mysql' in substrate['name'].lower():
                                        if str(substrate['readiness_probe']['login_credential_local_reference']['name']).lower() == 'teccdba':
                                            show_result(True, f'{eval_key["description"]} (MySQL Credential Name)',
                                                        f'Expected "teccdba"',
                                                        f'Found "{substrate["readiness_probe"]["login_credential_local_reference"]["name"]}"')
                                        else:
                                            show_result(False, f'{eval_key["description"]} (MySQL Credential Name)',
                                                        f'Expected "teccdba"',
                                                        f'Found "{substrate["readiness_probe"]["login_credential_local_reference"]["name"]}"')
                                    elif 'web' in substrate['name'].lower():
                                        if str(substrate['readiness_probe']['login_credential_local_reference']['name']).lower() == 'teccadmin':
                                            show_result(True, f'{eval_key["description"]} (Web Server Credential Name)',
                                                        f'Expected "teccadmin"',
                                                        f'Found "{substrate["readiness_probe"]["login_credential_local_reference"]["name"]}"')
                                        else:
                                            show_result(False, f'{eval_key["description"]} (Web Server Credential Name)',
                                                        f'Expected "teccadmin"',
                                                        f'Found "{substrate["readiness_probe"]["login_credential_local_reference"]["name"]}"')
                                    elif 'haproxy' in substrate['name'].lower():
                                        if str(substrate['readiness_probe']['login_credential_local_reference']['name']).lower() == 'teccadmin':
                                            show_result(True, f'{eval_key["description"]} (Load Balancer Credential Name)',
                                                        f'Expected "teccadmin"',
                                                        f'Found "{substrate["readiness_probe"]["login_credential_local_reference"]["name"]}"')
                                        else:
                                            show_result(False, f'{eval_key["description"]} (Load Balancer Credential Name)',
                                                        f'Expected "teccadmin"',
                                                        f'Found "{substrate["readiness_probe"]["login_credential_local_reference"]["name"]}"')
                                '''
                    except Exception as e:
                        print(e)

                '''
                ----------------------
                evaluation ends here
                ----------------------
                '''

        except KeyError as e:
            print(f'{messages.error} The {e} JSON key was not found'
                  + 'in the specified Blueprint spec.  Please check'
                  + 'the key, then try again.')
            if environment_options.debug:
                print(f'{messages.error} Exception details: {e}')
        except json.decoder.JSONDecodeError as e:
            print(f'{messages.error} The {bp} JSON file could not be parsed.  '
                  + 'Is it a valid Nutanix Calm Blueprint?')
            if environment_options.debug:
                print(f'{messages.error} Exception details: {e}')
    else:
        print(f'{messages.error} Blueprint not found.  Exiting.')
        sys.exit()
    print(f'{messages.info} Evaluation of {bp} completed.  '
          + 'Please see results above.')


def main():
    '''
    main entry point into the script
    '''

    # store the start time
    # used for duration stats later
    start_time = datetime.now()

    global environment_options
    global messages
    environment_options = EnvironmentOptions()
    environment_options.get_options()
    messages = Messages().prefixes

    if environment_options.debug:
        print(f'{environment_options}\n')

    print(f'{messages.info} Evaluation script started at {pretty_time()}.')

    print(f'{messages.info} Checking environment.')
    # check the environment, first
    environment_options.check_environment(messages)
    print(f'{messages.ok} Environment OK.')

    # verify the specified blueprint directory exists
    if os.path.exists(environment_options.directory):
        print(f'{messages.info} Blueprint directory found.  Continuing.')
    else:
        print(f'{messages.error} Blueprint directory not found.  Exiting.')
        sys.exit()

    # verify the specified criteria file exists
    if os.path.exists(f'{environment_options.criteria}'):
        print(f'{messages.info} Evaluation criteria file found.  Continuing.')
        # validate the specified criteria as valid JSON
        try:
            with open(f'{environment_options.criteria}', 'r') as criteria_file:
                json.loads(criteria_file.read())
                print(f'{messages.info} Criteria file '
                      + f'{environment_options.criteria} successfully parsed '
                      + 'as JSON.  Continuing.')
                criteria_file.close()
        except json.decoder.JSONDecodeError as e:
            print(f'{messages.error} The {environment_options.criteria} JSON '
                  + 'file could not be parsed.  Is it valid JSON?')
            if environment_options.debug:
                print(f'{messages.error} Exception details: {e}')

    else:
        print(f'{messages.error} Evaluation criteria file not found.  '
              + 'Exiting.')
        sys.exit()

    # keep track of how many blueprints have been processed
    processed_ok = 0

    '''
    check to see if the user has indicated they want to parse all blueprints
    in the specified blueprint directory
    '''
    if environment_options.blueprint.lower() == 'all':
        print(f'{messages.info} All blueprints in '
              + f'{environment_options.directory} '
              + 'will be processed.')
        bp_list = glob.iglob(f'{environment_options.directory}/*.json')
        for bp in bp_list:
            process_json(bp)
            processed_ok += 1
    else:
        print(f'{messages.info} Only {environment_options.blueprint} in '
              + f'{environment_options.directory} will be processed.')
        process_json(f'{environment_options.directory}/'
                     + f'{environment_options.blueprint}')
        processed_ok += 1

    # store the finish time
    finish_time = datetime.now()

    # calculate how long the script took to run
    duration = finish_time - start_time

    # clean up
    print(f'{messages.line}')
    print(f'{messages.info} Cleaning up.')
    print(f'{messages.info} Processed {processed_ok} blueprints.')
    print(f'{messages.info} Evaluation completed in '
          + f'{humanize.precisedelta(duration, minimum_unit="seconds")}.')
    print(f'{messages.info} Evaluation script finished at {pretty_time()}.\n')


if __name__ == '__main__':
    main()
