#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import re
from database import DatabaseConnection, dbutil


def makespec(connection: DatabaseConnection, method: str, schemaname: str, tablename: str):
    columns = dbutil.list_columns(connection=connection, schema=schemaname, table=tablename)

    return {
        f'/query/{schemaname}/{tablename}': {
            f'{method}': {
                'tags': [f"{format_name(schemaname)}/{format_name(tablename)}"],
                'summary': format_name(tablename),
                # 'description': f"{method} {format_name(tablename)}",
                'parameters': [
                    {
                        'in': "query",
                        'name': col.name,
                        'schema': POSTGRES2OPENAPI.get(col.data_type, col.data_type),
                        'description': format_name(col.name),
                    }
                    for col in columns
                ] + [
                    {
                        'in': "query",
                        'name': "__limit__",
                        'schema': {
                            'type': "number",
                        },
                        'description': "Maximum number of rows returned",
                    },
                    {
                        'in': "query",
                        'name': "__offset__",
                        'schema': {
                            'type': "number",
                        },
                        'description': "Number of rows to skip",
                    },
                ],
                'responses': {
                    '200': {
                        'description': "Successful operation",
                        'content': {
                            "application/json": {
                                'schema': {
                                    'type': "array",
                                    'items': {
                                        'type': "object",
                                        'properties': {
                                            col.name: POSTGRES2OPENAPI.get(col.data_type, col.data_type)
                                            for col in columns
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }


POSTGRES2OPENAPI = {
    'bigint': dict(type='integer'),
    'bigserial': dict(type='integer'),
    'boolean': dict(type='boolean'),
    'bytea': dict(type="string", format="byte"),
    'character': dict(type="string"),
    'character varying': dict(type="string"),
    'cidr': dict(type="string", format="ipv4"),
    'date': dict(type="string", format="date"),
    'double precision': dict(type="number"),
    'inet': dict(type="string", format="ipv4"),
    'integer': dict(type='integer'),
    'json': dict(type="string"),
    'jsonb': dict(type="string", format="byte"),
    'macaddr': dict(type="string"),
    'macaddr8': dict(type="string"),
    'numeric': dict(type="number"),
    'pg_lsn': dict(type='integer'),
    'pg_snapshot': dict(type='integer'),
    'real': dict(type='number'),
    'smallint': dict(type='integer'),
    'smallserial': dict(type='integer'),
    'serial': dict(type='integer'),
    'text': dict(type='string'),
    'time': dict(type='string'),
    'tsquery': dict(type='string'),
    'tsvector': dict(type='string'),
    'txid_snapshot': dict(type='integer'),
    'uuid': dict(type='integer'),
    'xml': dict(type='string', format='xml')
}


def format_name(name: str):
    return re.sub(r"[-_]", ' ', name).title()
