import boto3


class Glue:
    glue_client = {}

    def __init__(self):
        self.glue_client = boto3.client("glue")

    def get_glue_client(self):
        return self.glue_client

    def create_data_quality_ruleset(self, ruleset_data: dict = {}):
        client = self.get_glue_client()

        if (
            "Name" not in ruleset_data
            or "Ruleset" not in ruleset_data
            or "TableName" not in ruleset_data
            or "DatabaseName" not in ruleset_data
        ):
            raise "Name, Ruleset, TableName e DatabaseName precisam serem informados."

        try:
            response = client.create_data_quality_ruleset(
                Name=ruleset_data["Name"],
                Description=ruleset_data["Description"]
                if "Description" in ruleset_data
                else "",
                Ruleset=ruleset_data["Ruleset"],
                Tags=ruleset_data["Tags"] if "Tags" in ruleset_data else {},
                TargetTable={
                    "TableName": ruleset_data["TableName"],
                    "DatabaseName": ruleset_data["DatabaseName"],
                },
            )

            return response

        except Exception as e:
            raise e

    def list_data_quality_results(self, _filter: dict = {}):
        client = self.get_glue_client()

        if "DatabaseName" not in _filter or "TableName" not in _filter:
            raise "DatabaseName, TableName precisam serem informados."

        try:
            response = client.list_data_quality_results(
                Filter={
                    "DataSource": {
                        "GlueTable": {
                            "DatabaseName": _filter["DatabaseName"],
                            "TableName": _filter["TableName"],
                        }
                    }
                },
            )

            return response
        except Exception as e:
            raise e

    def list_data_quality_rulesets(self, _filter: dict = {}):
        client = self.get_glue_client()

        if "DatabaseName" not in _filter or "TableName" not in _filter:
            raise "DatabaseName, TableName precisam serem informados."

        try:
            response = client.list_data_quality_rulesets(
                Filter={
                    "TableName": _filter["TableName"],
                    "DatabaseName": _filter["DatabaseName"],
                }
            )

            return response
        except Exception as e:
            raise e

    def start_data_quality_ruleset_evaluation_run(self, _start_data_run: dict = {}):
        client = self.get_glue_client()

        if (
            "DatabaseName" not in _start_data_run
            or "TableName" not in _start_data_run
            or "Role" not in _start_data_run
            or "RulesetNames" not in _start_data_run
        ):
            raise "DatabaseName, TableName, Role e RulesetNames precisam serem informados."

        try:
            response = client.start_data_quality_ruleset_evaluation_run(
                DataSource={
                    "GlueTable": {
                        "DatabaseName": _start_data_run["DatabaseName"],
                        "TableName": _start_data_run["TableName"],
                    }
                },
                Role=_start_data_run["Role"],
                RulesetNames=_start_data_run["RulesetNames"],
            )

            return response
        except Exception as e:
            raise e

    def get_data_quality_result(self, _result_id: str = ""):
        client = self.get_glue_client()

        try:
            response = client.get_data_quality_result(ResultId=_result_id)

            return response
        except Exception as e:
            raise e
