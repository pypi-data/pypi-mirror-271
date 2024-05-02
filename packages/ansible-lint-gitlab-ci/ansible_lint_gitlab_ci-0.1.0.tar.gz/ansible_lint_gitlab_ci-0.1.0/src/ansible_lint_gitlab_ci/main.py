import re
import os
import sys
import json
import signal
import argparse
from  .version import __version__
from junit_reporter import TestCase, TestSuite, JUnitReporter

def signal_handler(signal, frame):
    exit(0)

"""This stops ctrl+c from rendering typical Python stack trace and cleanly exits program."""
signal.signal(signal.SIGINT, signal_handler)

def version():
    return __version__

def parse_args(argv: list[str]) -> argparse.Namespace:
    # Build parser object
    parser = argparse.ArgumentParser(description='Process ansible-lint JSON output into GitLab friendly JUnit XML')
    # Setup script arguments
    parser.add_argument(dest="input", action="store", nargs='*', help="output from 'ansible-lint -f json -q' command.", type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument("-o", "--output", dest="output_file", default="ansible-lint-gitlab-ci.xml", action="store", help="print ansible-lint JSON to GitLab CI JUnit output file")
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="print ansible-lint JSON to GitLab CI JUnit to console as command output", default=False)
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=version()))
    # Instantiate parser object
    args = parser.parse_args(argv)
    # args.output = str(Path(args.output).absolute())

    # if args.config_file:
    #     args.config_file = str(Path(args.config_file).absolute())

    return args

def main() -> None:

    # Build parser object
    arguments = parse_args(sys.argv[1:])

    if isinstance(arguments.input, list):
        arguments.input = arguments.input[0]
    # Read stdin output (should be json format)
    ansible_lint_json = json.loads(arguments.input.read())
    # Build test suite object
    test_suite = TestSuite('ansible-lint-gitlab-ci')
    # Setup error count tracking
    error_count = 0
    # Cycle through each issue
    for issue in ansible_lint_json:
        # Setup syntax issue tracker
        syntax_issue = False
        # Check if issue is syntax issue
        if re.match(r'^syntax-check.*$',issue["check_name"]):
            syntax_issue = True
        # Setup test case name
        if syntax_issue:
            test_case_name = f"{os.path.basename(issue['location']['path'])}:L{issue['location']['positions']['begin']['line']}:I1"
        else:
            test_case_name = f"{os.path.basename(issue['location']['path'])}:L{issue['location']['lines']['begin']}:I1"
        # Check for existing names, must be unique
        for tc in test_suite.test_cases:
            if tc.name == test_case_name:
                test_case_name = test_case_name.replace(f"{tc.name.split(':')[2]}",f"I{int(tc.name.split(':')[2].replace('I','')) + 1}")
        # Build test case object
        if syntax_issue:
            test_case = TestCase(test_case_name, classname=issue['check_name'], filename=f"./{issue['location']['path']}#L{issue['location']['positions']['begin']['line']}", stdout=issue["description"])
        else:
            test_case = TestCase(test_case_name, classname=issue['check_name'], filename=f"./{issue['location']['path']}#L{issue['location']['lines']['begin']}", stdout=issue["description"])
        # Set default failure type
        failure_type = "failed"
        # Check if severity is "error"
        if issue["severity"] == "minor":
            failure_type = "error"
            error_count += 1
        # Start building output
        output = issue["description"]
        # Look for extra output details
        if 'content' in issue.keys():
            output += f"\n\n{issue['content']['body']}"
        # Add issue information to output
        output += f"\n\nSEVERITY: {issue['severity']}"
        output += f"\nCATEGORY: {issue['check_name']}"
        output += f"\nURL: {issue['url']}"
        output += f"\nFILE: {issue['location']['path']}"
        # Add specific issue type info
        if syntax_issue:
            output += f"\nLINE: {issue['location']['positions']['begin']['line']}"
            output += f"\nCOLUMN: {issue['location']['positions']['begin']['column']}"
        else:
            output += f"\nLINE: {issue['location']['lines']['begin']}"
        # Add failure to test case
        test_case.add_failure(issue["description"],output=output)
        # Add test case to test suite
        test_suite.add_test_case(test_case)

    # results = test_suite.attributes 
    # results['errors'] = str(error_count)
    # results['failures'] = str(int(results['failures']) - error_count)
    # results.update()
    # Set testsuite to xml
    xml = JUnitReporter.report_to_string([test_suite])
    # Write output to file
    with open(arguments.output_file, "w") as file:
        file.write(xml)
    # Look for verbose argument, output to console if found
    if arguments.verbose:
        print(xml)
    
    # sys.exit(0)

# Main
if __name__== "__main__" :
    main()
