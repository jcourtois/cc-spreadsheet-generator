class TestCase:
    def __init__(self, test_case):
        self.test_case = test_case

    @property
    def name(self):
        return self.test_case["@classname"] \
            if self.test_case["@classname"] != "setUpClass" else self.test_case["@name"]

    @property
    def result(self):
        return self.test_case["@result"]

    @property
    def failed(self):
        return self.test_case["@result"] == "FAILED"

    @property
    def errored(self):
        return self.test_case["@result"] == "ERROR"

    @property
    def passed(self):
        return self.test_case["@result"] == "PASSED"

    @property
    def skipped(self):
        return self.test_case["@result"] == "SKIPPED"


class ProductResults:
    results = {}

    def __init__(self, single_result):
        cases = [TestCase(test_case)
                 for test_case in single_result["testsuite"]["testcase"]]

        for case in cases:
            if case.name not in self.results:
                self.record_new_class_of_tests(case.name)
            self.record_results(case)

    def record_new_class_of_tests(self, case_name):
            self.results[case_name] = {"FAILED": 0,
                                       "PASSED": 0,
                                       "ERROR": 0,
                                       "SKIPPED": 0,
                                       "TOTAL": 0,
                                       "PERCENTAGE PASSING": "0.0%",
                                       "failed tests": [],
                                       "errored tests": []}

    def record_results(self, case):
        self.results[case.name][case.result] += 1
        if case.failed:
            self.record_failed_test_name(case)
        elif case.errored:
            self.record_errored_test_name(case)
        self.update(case)


    def record_failed_test_name(self, case):
        self.results[case.name]["failed tests"].append(case.name)

    def record_errored_test_name(self, case):
        self.results[case.name]["errored tests"].append(case.name)

    def update(self, case):
        self.results[case.name]["TOTAL"] = self.results[case.name]["FAILED"] + \
            self.results[case.name]["PASSED"] + \
            self.results[case.name]["ERROR"]

        if self.results[case.name]["TOTAL"] == 0:
            self.results[case.name]["PERCENTAGE PASSING"] = 0.0
        else:
            self.results[case.name]["PERCENTAGE PASSING"] = \
                float(self.results[case.name]["PASSED"]) / self.results[case.name]["TOTAL"]


    @property
    def to_dict(self):
        return self.results
