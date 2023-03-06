import json

from boto3.dynamodb.conditions import Key

from decimal import Decimal

from src.shared.infra.external.dynamo.dynamo_table import DynamoTable


class DynamoDatasource:
    """
    Docs:
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table
    """
    dynamo_table: DynamoTable
    partition_key: str
    sort_key: str
    RESERVED_WORDS = ["ABORT", "ABSOLUTE", "ACTION", "ADD", "AFTER", "AGENT", "AGGREGATE", "ALL", "ALLOCATE", "ALTER", "ANALYZE", "AND", "ANY", "ARCHIVE", "ARE", "ARRAY", "AS", "ASC", "ASCII", "ASENSITIVE", "ASSERTION", "ASYMMETRIC", "AT", "ATOMIC", "ATTACH", "ATTRIBUTE", "AUTH", "AUTHORIZATION", "AUTHORIZE", "AUTO", "AVG", "BACK", "BACKUP", "BASE", "BATCH", "BEFORE", "BEGIN", "BETWEEN", "BIGINT", "BINARY", "BIT", "BLOB", "BLOCK", "BOOLEAN", "BOTH", "BREADTH", "BUCKET", "BULK", "BY", "BYTE", "CALL", "CALLED", "CALLING", "CAPACITY", "CASCADE", "CASCADED", "CASE", "CAST", "CATALOG", "CHAR", "CHARACTER", "CHECK", "CLASS", "CLOB", "CLOSE", "CLUSTER", "CLUSTERED", "CLUSTERING", "CLUSTERS", "COALESCE", "COLLATE", "COLLATION", "COLLECTION", "COLUMN", "COLUMNS", "COMBINE", "COMMENT", "COMMIT", "COMPACT", "COMPILE", "COMPRESS", "CONDITION", "CONFLICT", "CONNECT", "CONNECTION", "CONSISTENCY", "CONSISTENT", "CONSTRAINT", "CONSTRAINTS", "CONSTRUCTOR", "CONSUMED", "CONTINUE", "CONVERT", "COPY", "CORRESPONDING", "COUNT", "COUNTER", "CREATE", "CROSS", "CUBE", "CURRENT", "CURSOR", "CYCLE", "DATA", "DATABASE", "DATE", "DATETIME", "DAY", "DEALLOCATE", "DEC", "DECIMAL", "DECLARE", "DEFAULT", "DEFERRABLE", "DEFERRED", "DEFINE", "DEFINED", "DEFINITION", "DELETE", "DELIMITED", "DEPTH", "DEREF", "DESC", "DESCRIBE", "DESCRIPTOR", "DETACH", "DETERMINISTIC", "DIAGNOSTICS", "DIRECTORIES", "DISABLE", "DISCONNECT", "DISTINCT", "DISTRIBUTE", "DO", "DOMAIN", "DOUBLE", "DROP", "DUMP", "DURATION", "DYNAMIC", "EACH", "ELEMENT", "ELSE", "ELSEIF", "EMPTY", "ENABLE", "END", "EQUAL", "EQUALS", "ERROR", "ESCAPE", "ESCAPED", "EVAL", "EVALUATE", "EXCEEDED", "EXCEPT", "EXCEPTION", "EXCEPTIONS", "EXCLUSIVE", "EXEC", "EXECUTE", "EXISTS", "EXIT", "EXPLAIN", "EXPLODE", "EXPORT", "EXPRESSION", "EXTENDED", "EXTERNAL", "EXTRACT", "FAIL", "FALSE", "FAMILY", "FETCH", "FIELDS", "FILE", "FILTER", "FILTERING", "FINAL", "FINISH", "FIRST", "FIXED", "FLATTERN", "FLOAT", "FOR", "FORCE", "FOREIGN", "FORMAT", "FORWARD", "FOUND", "FREE", "FROM", "FULL", "FUNCTION", "FUNCTIONS", "GENERAL", "GENERATE", "GET", "GLOB", "GLOBAL", "GO", "GOTO", "GRANT", "GREATER", "GROUP", "GROUPING", "HANDLER", "HASH", "HAVE", "HAVING", "HEAP", "HIDDEN", "HOLD", "HOUR", "IDENTIFIED", "IDENTITY", "IF", "IGNORE", "IMMEDIATE", "IMPORT", "IN", "INCLUDING", "INCLUSIVE", "INCREMENT", "INCREMENTAL", "INDEX", "INDEXED", "INDEXES", "INDICATOR", "INFINITE", "INITIALLY", "INLINE", "INNER", "INNTER", "INOUT", "INPUT", "INSENSITIVE", "INSERT", "INSTEAD", "INT", "INTEGER", "INTERSECT", "INTERVAL", "INTO", "INVALIDATE", "IS", "ISOLATION", "ITEM", "ITEMS", "ITERATE", "JOIN", "KEY", "KEYS", "LAG", "LANGUAGE", "LARGE", "LAST", "LATERAL", "LEAD", "LEADING", "LEAVE", "LEFT", "LENGTH", "LESS", "LEVEL", "LIKE", "LIMIT", "LIMITED", "LINES", "LIST", "LOAD", "LOCAL", "LOCALTIME", "LOCALTIMESTAMP", "LOCATION", "LOCATOR", "LOCK", "LOCKS", "LOG", "LOGED", "LONG", "LOOP", "LOWER", "MAP", "MATCH", "MATERIALIZED", "MAX", "MAXLEN", "MEMBER", "MERGE", "METHOD", "METRICS", "MIN", "MINUS", "MINUTE", "MISSING", "MOD", "MODE", "MODIFIES", "MODIFY", "MODULE", "MONTH", "MULTI", "MULTISET", "NAME", "NAMES", "NATIONAL", "NATURAL", "NCHAR", "NCLOB", "NEW", "NEXT", "NO", "NONE", "NOT", "NULL", "NULLIF", "NUMBER", "NUMERIC", "OBJECT", "OF", "OFFLINE", "OFFSET", "OLD", "ON", "ONLINE", "ONLY", "OPAQUE", "OPEN", "OPERATOR", "OPTION", "OR", "ORDER", "ORDINALITY", "OTHER", "OTHERS", "OUT", "OUTER", "OUTPUT", "OVER", "OVERLAPS", "OVERRIDE", "OWNER", "PAD", "PARALLEL", "PARAMETER", "PARAMETERS", "PARTIAL", "PARTITION", "PARTITIONED", "PARTITIONS", "PATH", "PERCENT", "PERCENTILE", "PERMISSION", "PERMISSIONS", "PIPE", "PIPELINED", "PLAN", "POOL", "POSITION", "PRECISION", "PREPARE", "PRESERVE", "PRIMARY", "PRIOR", "PRIVATE", "PRIVILEGES", "PROCEDURE", "PROCESSED", "PROJECT", "PROJECTION", "PROPERTY", "PROVISIONING", "PUBLIC", "PUT", "QUERY", "QUIT", "QUORUM", "RAISE", "RANDOM", "RANGE", "RANK", "RAW", "READ", "READS", "REAL", "REBUILD", "RECORD", "RECURSIVE", "REDUCE", "REF", "REFERENCE", "REFERENCES", "REFERENCING", "REGEXP", "REGION", "REINDEX", "RELATIVE", "RELEASE", "REMAINDER", "RENAME", "REPEAT", "REPLACE", "REQUEST", "RESET", "RESIGNAL", "RESOURCE", "RESPONSE", "RESTORE", "RESTRICT", "RESULT", "RETURN", "RETURNING", "RETURNS", "REVERSE", "REVOKE", "RIGHT", "ROLE", "ROLES", "ROLLBACK", "ROLLUP", "ROUTINE", "ROW", "ROWS", "RULE", "RULES", "SAMPLE", "SATISFIES", "SAVE", "SAVEPOINT", "SCAN", "SCHEMA", "SCOPE", "SCROLL", "SEARCH", "SECOND", "SECTION", "SEGMENT", "SEGMENTS", "SELECT", "SELF", "SEMI", "SENSITIVE", "SEPARATE", "SEQUENCE", "SERIALIZABLE", "SESSION", "SET", "SETS", "SHARD", "SHARE", "SHARED", "SHORT", "SHOW", "SIGNAL", "SIMILAR", "SIZE", "SKEWED", "SMALLINT", "SNAPSHOT", "SOME", "SOURCE", "SPACE", "SPACES", "SPARSE", "SPECIFIC", "SPECIFICTYPE", "SPLIT", "SQL", "SQLCODE", "SQLERROR", "SQLEXCEPTION", "SQLSTATE", "SQLWARNING", "START", "STATE", "STATIC", "STATUS", "STORAGE", "STORE", "STORED", "STREAM", "STRING", "STRUCT", "STYLE", "SUB", "SUBMULTISET", "SUBPARTITION", "SUBSTRING", "SUBTYPE", "SUM", "SUPER", "SYMMETRIC", "SYNONYM", "SYSTEM", "TABLE", "TABLESAMPLE", "TEMP", "TEMPORARY", "TERMINATED", "TEXT", "THAN", "THEN", "THROUGHPUT", "TIME", "TIMESTAMP", "TIMEZONE", "TINYINT", "TO", "TOKEN", "TOTAL", "TOUCH", "TRAILING", "TRANSACTION", "TRANSFORM", "TRANSLATE", "TRANSLATION", "TREAT", "TRIGGER", "TRIM", "TRUE", "TRUNCATE", "TTL", "TUPLE", "TYPE", "UNDER", "UNDO", "UNION", "UNIQUE", "UNIT", "UNKNOWN", "UNLOGGED", "UNNEST", "UNPROCESSED", "UNSIGNED", "UNTIL", "UPDATE", "UPPER", "URL", "USAGE", "USE", "USER", "USERS", "USING", "UUID", "VACUUM", "VALUE", "VALUED", "VALUES", "VARCHAR", "VARIABLE", "VARIANCE", "VARINT", "VARYING", "VIEW", "VIEWS", "VIRTUAL", "VOID", "WAIT", "WHEN", "WHENEVER", "WHERE", "WHILE", "WINDOW", "WITH", "WITHIN", "WITHOUT", "WORK", "WRAPPED", "WRITE", "YEAR", "ZONE"]

    def __init__(self, dynamo_table_name: str, partition_key: str, region: str,
                 endpoint_url: str = None, sort_key: str = None):

        self.dynamo_table = DynamoTable(dynamo_table_name=dynamo_table_name, region=region,
                                        endpoint_url=endpoint_url)

        self.partition_key = partition_key
        self.sort_key = sort_key

    @staticmethod
    def _parse_float_to_decimal(item):
        """
        Parse float to Decimal
        @param item: dict with the keys (Partition and Sort) and data to insert
        """
        item_parsed = json.loads(json.dumps(item), parse_float=Decimal)
        return item_parsed

    def put_item(self, item: dict, partition_key: str, sort_key: str = None, **kwargs):
        """
        Insert a new item into the table or hard update an existing one.
        Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.put_item
        @param item: dict with the keys (Partition and Sort) and data to insert
        @param partition_key: string with the partition key
        @param sort_key: string with the sort key (optional)
        @return: dict with the response from DynamoDB
        """

        item = DynamoDatasource._parse_float_to_decimal(item) if not kwargs.get("is_decimal", False) else item

        with self.dynamo_table as table:
            item[self.partition_key] = partition_key
            if sort_key:
                item[self.sort_key] = sort_key
            return table.put_item(Item=item)

    def get_item(self, partition_key: str, sort_key: str = None):
        """
        Get an item from the table from its keys (Partition and Sort).
        @param partition_key: string with the partition key
        @param sort_key: string with the sort key (optional)
        @return: dict with the response from DynamoDB
        """

        with self.dynamo_table as table:
            resp = table.get_item(
                Key={self.partition_key: partition_key, self.sort_key: sort_key if sort_key else None}
            )
            return resp

    def hard_update_item(self, partition_key: str, sort_key: str, item: dict):
        """
        Hard update an item in the table (must have its keys - Partition and Sort).
        @param partition_key: string with the partition key
        @param sort_key: string with the sort key (optional)
        @param item: dict with data to insert
        @return: dict with the response from DynamoDB
        """

        item[self.partition_key] = partition_key

        if sort_key:
            item[self.sort_key] = sort_key

        with self.dynamo_table as table:
            resp = table.put_item(Item=DynamoDatasource._parse_float_to_decimal(item))
            return resp

    def update_item(self, partition_key: str, sort_key: str, update_dict: dict):
        """
        Update an item in the table with its keys (Partition and Sort) and attributes to update
        If the attribute does not exist, it will be created. It won't change attributes not mentioned.
        @param key: dict with the keys (Partition and Sort)
        @param update_attributes: dict with the attributes to update
        @return: dict with the response from DynamoDB
        """

        data_key_value_pairs = list(update_dict.items())

        update_expression = "SET " + ", ".join([f"#attr{i} = :val{i}" for i in range(len(data_key_value_pairs))]) # SET attribute1=:value1, attribute2=:value2
        expression_attribute_names = {f"#attr{i}": data_key_value_pairs[i][0] for i in range(len(data_key_value_pairs))} # {"_attribute1": "attribute1", ":_attribute2": "attribute2"}
        expression_value_names = {f":val{i}": data_key_value_pairs[i][1] for i in range(len(data_key_value_pairs))} # {":value1": "value1", ":value2": "value2"}

        with self.dynamo_table as table:
            resp = table.update_item(
                Key={
                    self.partition_key: partition_key,
                    self.sort_key: sort_key
                },
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expression_attribute_names,
                ExpressionAttributeValues=expression_value_names,
                ReturnValues="ALL_NEW"
            )
            return resp

    def delete_item(self, partition_key: str, sort_key: str = None):
        """
        Delete an item from the table from its keys (Partition and Sort).
        @param partition_key: string with the partition key
        @param sort_key: string with the sort key (optional)
        @return: dict with the response from DynamoDB
        """

        with self.dynamo_table as table:
            resp = table.delete_item(
                Key={
                    self.partition_key: partition_key,
                    self.sort_key: sort_key if sort_key else None
                },
                ReturnValues='ALL_OLD'
            )
            return resp

    def get_all_items(self):
        """
        Get all items from the table.
        @return: dict with the response from DynamoDB
        """

        with self.dynamo_table as table:
            resp = table.scan(Select='ALL_ATTRIBUTES')
            return resp

    def scan_items(self, filter_expression, **kwargs):
        """
        Scan items from the table.
        @return: dict with the response from DynamoDB
        """

        with self.dynamo_table as table:
            resp = table.scan(
                FilterExpression=filter_expression,
                **kwargs
            )
            return resp

    def query(self, key_condition_expression, **kwargs):
        """
        Query the table with the KeyConditionExpression.
        Example: KeyConditionExpression=Key('Partition').eq('partition') & Key('Sort').gte('sort')
        Obs: Key de boto3.dynamodb.conditions.Key
        Ref:https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/dynamodb.html#ref-dynamodb-conditions
        @param key_condition_expression: string with the KeyConditionExpression
        @return: dict with the response from DynamoDB
        """

        with self.dynamo_table as table:
            resp = table.query(
                KeyConditionExpression=key_condition_expression,

                **kwargs
            )
            return resp

    def batch_write_items(self, items):
        """
        Write a list of items to the table. Each item must have the keys (Partition and Sort).
        @param items: list of dicts with the keys (Partition and Sort) and data to insert
        """

        with self.dynamo_table as table:
            with table.batch_writer() as batch:
                for i in items:
                    batch.put_item(Item=DynamoDatasource._parse_float_to_decimal(i))

    def batch_delete_items(self, keys):
        """
        Delete a list of items from the table. Each item must have only the keys (Partition and Sort).
        @param keys: list of dicts with the keys (Partition and Sort)
        Example: keys=[ {'Partition': 'partition1', 'Sort': 'sort2'}, {'Partition': 'partition1', 'Sort': 'sort2'} ]
        """

        with self.dynamo_table as table:
            with table.batch_writer() as batch:
                for k in keys:
                    batch.delete_item(Key=k)


if __name__ == '__main__':
    dynamo = DynamoDatasource(endpoint_url="http://localhost:8000",
                              dynamo_table_name="selfie_mss_student-table", region="foobar",
                              partition_key="PK", sort_key="SK")

    print(dynamo.get_item("student#21002088", "21002088"))

    dynamo.update_item("student#21002088", "21002088", {"name": "Maluzinha", "ra": "21002088"})
