# Copyright (c) 2024 Snowflake Computing Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import codecs
import os
import time
import uuid

import botocore
import pytest
import boto3
from urllib.parse import unquote

from iceberg_spark import IcebergSparkSession
from polaris.catalog.api.iceberg_catalog_api import IcebergCatalogAPI
from polaris.catalog.api.iceberg_o_auth2_api import IcebergOAuth2API
from polaris.catalog.api_client import ApiClient as CatalogApiClient
from polaris.catalog.configuration import Configuration
from polaris.management import PolarisDefaultApi, Principal, PrincipalRole, CatalogRole, \
  CatalogGrant, CatalogPrivilege, ApiException, CreateCatalogRoleRequest, CreatePrincipalRoleRequest, \
  CreatePrincipalRequest, AddGrantRequest, GrantCatalogRoleRequest, GrantPrincipalRoleRequest
from polaris.management import ApiClient as ManagementApiClient


@pytest.fixture
def snowman(polaris_url, polaris_catalog_url, root_client, snowflake_catalog):
  """
  create the snowman principal with full table/namespace privileges
  :param root_client:
  :param snowflake_catalog:
  :return:
  """
  snowman_name = "snowman"
  table_writer_rolename = "table_writer"
  snowflake_writer_rolename = "snowflake_writer"
  try:
    snowman = create_principal(polaris_url, polaris_catalog_url, root_client, snowman_name)
    writer_principal_role = create_principal_role(root_client, table_writer_rolename)
    writer_catalog_role = create_catalog_role(root_client, snowflake_catalog, snowflake_writer_rolename)
    root_client.assign_catalog_role_to_principal_role(principal_role_name=writer_principal_role.name,
                                                      catalog_name=snowflake_catalog.name,
                                                      grant_catalog_role_request=GrantCatalogRoleRequest(
                                                        catalog_role=writer_catalog_role))
    root_client.add_grant_to_catalog_role(snowflake_catalog.name, writer_catalog_role.name,
                                          AddGrantRequest(grant=CatalogGrant(catalog_name=snowflake_catalog.name,
                                                                             type='catalog',
                                                                             privilege=CatalogPrivilege.TABLE_FULL_METADATA)))
    root_client.add_grant_to_catalog_role(snowflake_catalog.name, writer_catalog_role.name,
                                          AddGrantRequest(grant=CatalogGrant(catalog_name=snowflake_catalog.name,
                                                                             type='catalog',
                                                                             privilege=CatalogPrivilege.VIEW_FULL_METADATA)))
    root_client.add_grant_to_catalog_role(snowflake_catalog.name, writer_catalog_role.name,
                                          AddGrantRequest(grant=CatalogGrant(catalog_name=snowflake_catalog.name,
                                                                             type='catalog',
                                                                             privilege=CatalogPrivilege.TABLE_WRITE_DATA)))
    root_client.add_grant_to_catalog_role(snowflake_catalog.name, writer_catalog_role.name,
                                          AddGrantRequest(grant=CatalogGrant(catalog_name=snowflake_catalog.name,
                                                                             type='catalog',
                                                                             privilege=CatalogPrivilege.NAMESPACE_FULL_METADATA)))

    root_client.assign_principal_role(snowman.principal.name,
                                      grant_principal_role_request=GrantPrincipalRoleRequest(
                                        principal_role=writer_principal_role))
    yield snowman
  finally:
    root_client.delete_principal(snowman_name)
    root_client.delete_principal_role(principal_role_name=table_writer_rolename)
    root_client.delete_catalog_role(catalog_role_name=snowflake_writer_rolename, catalog_name=snowflake_catalog.name)


@pytest.fixture
def reader(polaris_url, polaris_catalog_url, root_client, snowflake_catalog):
  """
  create the test_reader principal with table/namespace list and read privileges

  :param root_client:
  :param snowflake_catalog:
  :return:
  """
  reader_principal_name = 'test_reader'
  reader_principal_role_name = "table_reader"
  reader_catalog_role_name = 'snowflake_reader'
  try:
    reader = create_principal(polaris_url, polaris_catalog_url, root_client, reader_principal_name)
    reader_principal_role = create_principal_role(root_client, reader_principal_role_name)
    reader_catalog_role = create_catalog_role(root_client, snowflake_catalog, reader_catalog_role_name)

    root_client.assign_catalog_role_to_principal_role(principal_role_name=reader_principal_role.name,
                                                      catalog_name=snowflake_catalog.name,
                                                      grant_catalog_role_request=GrantCatalogRoleRequest(
                                                        catalog_role=reader_catalog_role))
    root_client.assign_principal_role(reader.principal.name,
                                      grant_principal_role_request=GrantPrincipalRoleRequest(
                                        principal_role=reader_principal_role))
    root_client.add_grant_to_catalog_role(snowflake_catalog.name, reader_catalog_role.name,
                                          AddGrantRequest(grant=CatalogGrant(catalog_name=snowflake_catalog.name,
                                                                             type='catalog',
                                                                             privilege=CatalogPrivilege.TABLE_READ_DATA)))
    root_client.add_grant_to_catalog_role(snowflake_catalog.name, reader_catalog_role.name,
                                          AddGrantRequest(grant=CatalogGrant(catalog_name=snowflake_catalog.name,
                                                                             type='catalog',
                                                                             privilege=CatalogPrivilege.TABLE_LIST)))
    root_client.add_grant_to_catalog_role(snowflake_catalog.name, reader_catalog_role.name,
                                          AddGrantRequest(grant=CatalogGrant(catalog_name=snowflake_catalog.name,
                                                                             type='catalog',
                                                                             privilege=CatalogPrivilege.TABLE_READ_PROPERTIES)))
    root_client.add_grant_to_catalog_role(snowflake_catalog.name, reader_catalog_role.name,
                                          AddGrantRequest(grant=CatalogGrant(catalog_name=snowflake_catalog.name,
                                                                             type='catalog',
                                                                             privilege=CatalogPrivilege.NAMESPACE_LIST)))
    root_client.add_grant_to_catalog_role(snowflake_catalog.name, reader_catalog_role.name,
                                          AddGrantRequest(grant=CatalogGrant(catalog_name=snowflake_catalog.name,
                                                                             type='catalog',
                                                                             privilege=CatalogPrivilege.NAMESPACE_READ_PROPERTIES)))
    yield reader
  finally:
    root_client.delete_principal(reader_principal_name)
    root_client.delete_principal_role(principal_role_name=reader_principal_role_name)
    root_client.delete_catalog_role(catalog_role_name=reader_catalog_role_name, catalog_name=snowflake_catalog.name)


@pytest.fixture
def snowman_catalog_client(polaris_catalog_url, snowman):
  """
  Create an iceberg catalog client with snowman credentials
  :param polaris_catalog_url:
  :param snowman:
  :return:
  """
  client = CatalogApiClient(Configuration(username=snowman.principal.client_id,
                                          password=snowman.credentials.client_secret,
                                          host=polaris_catalog_url))
  oauth_api = IcebergOAuth2API(client)
  token = oauth_api.get_token(scope='PRINCIPAL_ROLE:ALL', client_id=snowman.principal.client_id,
                              client_secret=snowman.credentials.client_secret,
                              grant_type='client_credentials',
                              _headers={'realm': 'default-realm'})

  return IcebergCatalogAPI(CatalogApiClient(Configuration(access_token=token.access_token,
                                                          host=polaris_catalog_url)))


@pytest.fixture
def reader_catalog_client(polaris_catalog_url, reader):
  """
  Create an iceberg catalog client with test_reader credentials
  :param polaris_catalog_url:
  :param reader:
  :return:
  """
  client = CatalogApiClient(Configuration(username=reader.principal.client_id,
                                          password=reader.credentials.client_secret,
                                          host=polaris_catalog_url))
  oauth_api = IcebergOAuth2API(client)
  token = oauth_api.get_token(scope='PRINCIPAL_ROLE:ALL', client_id=reader.principal.client_id,
                              client_secret=reader.credentials.client_secret,
                              grant_type='client_credentials',
                              _headers={'realm': 'default-realm'})

  return IcebergCatalogAPI(CatalogApiClient(Configuration(access_token=token.access_token,
                                                          host=polaris_catalog_url)))


@pytest.mark.skipif(os.environ.get('AWS_TEST_ENABLED', 'False').lower() != 'true', reason='AWS_TEST_ENABLED is not set or is false')
def test_spark_credentials(root_client, snowflake_catalog, polaris_catalog_url, snowman, reader):
  """
  Basic spark test - using snowman, create namespaces and a table. Insert into the table and read records back.

  Using the reader principal's credentials verify read access. Validate the reader cannot insert into the table.
  :param root_client:
  :param snowflake_catalog:
  :param polaris_catalog_url:
  :param snowman:
  :param reader:
  :return:
  """
  with IcebergSparkSession(credentials=f'{snowman.principal.client_id}:{snowman.credentials.client_secret}',
                           catalog_name=snowflake_catalog.name,
                           polaris_url=polaris_catalog_url) as spark:
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('CREATE NAMESPACE db1')
    spark.sql('CREATE NAMESPACE db1.schema')
    spark.sql('SHOW NAMESPACES')
    spark.sql('USE db1.schema')
    spark.sql('CREATE TABLE iceberg_table (col1 int, col2 string)')
    spark.sql('SHOW TABLES')
    spark.sql("""INSERT INTO iceberg_table VALUES 
        (10, 'mystring'),
        (20, 'anotherstring'),
        (30, null)
        """)
    count = spark.sql("SELECT * FROM iceberg_table").count()
    assert count == 3

  # switch users to the reader. we can query, show namespaces, but we can't insert
  with IcebergSparkSession(credentials=f'{reader.principal.client_id}:{reader.credentials.client_secret}',
                           catalog_name=snowflake_catalog.name,
                           polaris_url=polaris_catalog_url) as spark:
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('SHOW NAMESPACES')
    spark.sql('USE db1.schema')
    count = spark.sql("SELECT * FROM iceberg_table").count()
    assert count == 3
    try:
      spark.sql("""INSERT INTO iceberg_table VALUES 
            (10, 'mystring'),
            (20, 'anotherstring'),
            (30, null)
            """)
      pytest.fail("Expected exception when trying to write without permission")
    except:
      print("Exception caught attempting to write without permission")

  # switch back to delete stuff
  with IcebergSparkSession(credentials=f'{snowman.principal.client_id}:{snowman.credentials.client_secret}',
                           catalog_name=snowflake_catalog.name,
                           polaris_url=polaris_catalog_url) as spark:
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('USE db1.schema')
    spark.sql('DROP TABLE iceberg_table')
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('DROP NAMESPACE db1.schema')
    spark.sql('DROP NAMESPACE db1')


@pytest.mark.skipif(os.environ.get('AWS_TEST_ENABLED', 'False').lower() != 'true', reason='AWS_TEST_ENABLED is not set or is false')
def test_spark_credentials_can_delete_after_purge(root_client, snowflake_catalog, polaris_catalog_url, snowman,
                                                  snowman_catalog_client, test_bucket):
  """
  Using snowman, create namespaces and a table. Insert into the table in multiple operations and update existing records
  to generate multiple metadata.json files and manfiests. Drop the table with purge=true. Poll S3 and validate all of
  the files are deleted.

  Using the reader principal's credentials verify read access. Validate the reader cannot insert into the table.
  :param root_client:
  :param snowflake_catalog:
  :param polaris_catalog_url:
  :param snowman:
  :param reader:
  :return:
  """
  with IcebergSparkSession(credentials=f'{snowman.principal.client_id}:{snowman.credentials.client_secret}',
                           catalog_name=snowflake_catalog.name,
                           polaris_url=polaris_catalog_url) as spark:
    table_name = f'iceberg_test_table_{str(uuid.uuid4())[-10:]}'
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('CREATE NAMESPACE db1')
    spark.sql('CREATE NAMESPACE db1.schema')
    spark.sql('SHOW NAMESPACES')
    spark.sql('USE db1.schema')
    spark.sql(f'CREATE TABLE {table_name} (col1 int, col2 string)')
    spark.sql('SHOW TABLES')

    # several inserts and an update, which should cause earlier files to show up as deleted in the later manifests
    spark.sql(f"""INSERT INTO {table_name} VALUES 
        (10, 'mystring'),
        (20, 'anotherstring'),
        (30, null)
        """)
    spark.sql(f"""INSERT INTO {table_name} VALUES 
        (40, 'mystring'),
        (50, 'anotherstring'),
        (60, null)
        """)
    spark.sql(f"""INSERT INTO {table_name} VALUES 
        (70, 'mystring'),
        (80, 'anotherstring'),
        (90, null)
        """)
    spark.sql(f"UPDATE {table_name} SET col2='changed string' WHERE col1 BETWEEN 20 AND 50")
    count = spark.sql(f"SELECT * FROM {table_name}").count()

    assert count == 9

    # fetch aws credentials to examine the metadata files
    response = snowman_catalog_client.load_table(snowflake_catalog.name, unquote('db1%1Fschema'), table_name,
                                                 "true")
    assert response.config is not None
    assert 's3.access-key-id' in response.config
    assert 's3.secret-access-key' in response.config
    assert 's3.session-token' in response.config

    s3 = boto3.client('s3',
                      aws_access_key_id=response.config['s3.access-key-id'],
                      aws_secret_access_key=response.config['s3.secret-access-key'],
                      aws_session_token=response.config['s3.session-token'])

    objects = s3.list_objects(Bucket=test_bucket, Delimiter='/',
                              Prefix=f'polaris_test/snowflake_catalog/db1/schema/{table_name}/data/')
    assert objects is not None
    assert 'Contents' in objects
    assert len(objects['Contents']) >= 4  # idk, it varies - at least one file for each inser and one for the update
    print(f"Found {len(objects['Contents'])} data files in S3 before drop")

    objects = s3.list_objects(Bucket=test_bucket, Delimiter='/',
                              Prefix=f'polaris_test/snowflake_catalog/db1/schema/{table_name}/metadata/')
    assert objects is not None
    assert 'Contents' in objects
    assert len(objects['Contents']) == 15  # 5 metadata.json files, 4 manifest lists, and 6 manifests
    print(f"Found {len(objects['Contents'])} metadata files in S3 before drop")

    # use the api client to ensure the purge flag is set to true
    snowman_catalog_client.drop_table(snowflake_catalog.name,
                                      codecs.decode("1F", "hex").decode("UTF-8").join(['db1', 'schema']), table_name,
                                      purge_requested=True)
    spark.sql('DROP NAMESPACE db1.schema')
    spark.sql('DROP NAMESPACE db1')
    print("Dropped table with purge - waiting for files to be deleted")
    attempts = 0

    # watch the data directory. metadata will be deleted first, so if data directory is clear, we can expect
    # metadatat diretory to be clear also
    while 'Contents' in objects and len(objects['Contents']) > 0 and attempts < 60:
      time.sleep(1)  # seconds, not milliseconds ;)
      objects = s3.list_objects(Bucket=test_bucket, Delimiter='/',
                                Prefix=f'polaris_test/snowflake_catalog/db1/schema/{table_name}/data/')
      attempts = attempts + 1

    if 'Contents' in objects and len(objects['Contents']) > 0:
      pytest.fail(f"Expected all data to be deleted, but found metadata files {objects['Contents']}")

    objects = s3.list_objects(Bucket=test_bucket, Delimiter='/',
                              Prefix=f'polaris_test/snowflake_catalog/db1/schema/{table_name}/data/')
    if 'Contents' in objects and len(objects['Contents']) > 0:
      pytest.fail(f"Expected all data to be deleted, but found data files {objects['Contents']}")


@pytest.mark.skipif(os.environ.get('AWS_TEST_ENABLED', 'False').lower() != 'true', reason='AWS_TEST_ENABLED is not set or is false')
# @pytest.mark.skip(reason="This test is flaky")
def test_spark_credentials_can_create_views(snowflake_catalog, polaris_catalog_url, snowman):
  """
  Using snowman, create namespaces and a table. Insert into the table in multiple operations and update existing records
  to generate multiple metadata.json files and manifests. Create a view on the table. Verify the state of the view
  matches the state of the table.

  Using the reader principal's credentials verify read access. Validate the reader cannot insert into the table.
  :param snowflake_catalog:
  :param polaris_catalog_url:
  :param snowman:
  :return:
  """
  with IcebergSparkSession(credentials=f'{snowman.principal.client_id}:{snowman.credentials.client_secret}',
                           catalog_name=snowflake_catalog.name,
                           polaris_url=polaris_catalog_url) as spark:
    table_name = f'iceberg_test_table_{str(uuid.uuid4())[-10:]}'
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('CREATE NAMESPACE db1')
    spark.sql('CREATE NAMESPACE db1.schema')
    spark.sql('SHOW NAMESPACES')
    spark.sql('USE db1.schema')
    spark.sql(f'CREATE TABLE {table_name} (col1 int, col2 string)')
    spark.sql('SHOW TABLES')

    # several inserts
    spark.sql(f"""INSERT INTO {table_name} VALUES 
        (10, 'mystring'),
        (20, 'anotherstring'),
        (30, null)
        """)
    spark.sql(f"""INSERT INTO {table_name} VALUES 
        (40, 'mystring'),
        (50, 'anotherstring'),
        (60, null)
        """)
    spark.sql(f"""INSERT INTO {table_name} VALUES 
        (70, 'mystring'),
        (80, 'anotherstring'),
        (90, null)
        """)
    # verify the view reflects the current state of the table
    spark.sql(f"CREATE VIEW {table_name}_view AS SELECT col2 FROM {table_name} where col1 > 30 ORDER BY col1 DESC")
    view_records = spark.sql(f"SELECT * FROM {table_name}_view").collect()
    assert len(view_records) == 6
    assert len(view_records[0]) == 1
    assert view_records[1][0] == 'anotherstring'
    assert view_records[5][0] == 'mystring'

    # Update some records. Assert the view reflects the new state
    spark.sql(f"UPDATE {table_name} SET col2='changed string' WHERE col1 BETWEEN 20 AND 50")
    view_records = spark.sql(f"SELECT * FROM {table_name}_view").collect()
    assert len(view_records) == 6
    assert view_records[5][0] == 'changed string'


@pytest.mark.skipif(os.environ.get('AWS_TEST_ENABLED', 'False').lower() != 'true', reason='AWS_TEST_ENABLED is not set or is false')
def test_spark_credentials_s3_direct_with_write(root_client, snowflake_catalog, polaris_catalog_url,
                                                snowman, snowman_catalog_client, test_bucket):
  """
  Create two tables using Spark. Then call the loadTable api directly with snowman token to fetch the vended credentials
  for the first table.
  Verify that the credentials returned to snowman can read and write to the table's directory in S3, but don't allow
  reads or writes to the other table's directory
  :param root_client:
  :param snowflake_catalog:
  :param polaris_catalog_url:
  :param snowman_catalog_client:
  :param reader_catalog_client:
  :return:
  """
  with IcebergSparkSession(credentials=f'{snowman.principal.client_id}:{snowman.credentials.client_secret}',
                           catalog_name=snowflake_catalog.name,
                           polaris_url=polaris_catalog_url) as spark:
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('CREATE NAMESPACE db1')
    spark.sql('CREATE NAMESPACE db1.schema')
    spark.sql('USE db1.schema')
    spark.sql('CREATE TABLE iceberg_table (col1 int, col2 string)')
    spark.sql('CREATE TABLE iceberg_table_2 (col1 int, col2 string)')

  table2_metadata = snowman_catalog_client.load_table(snowflake_catalog.name, unquote('db1%1Fschema'),
                                                      "iceberg_table_2",
                                                      "s3_direct_with_write_table2").metadata_location
  response = snowman_catalog_client.load_table(snowflake_catalog.name, unquote('db1%1Fschema'), "iceberg_table",
                                               "s3_direct_with_write")
  assert response.config is not None
  assert 's3.access-key-id' in response.config
  assert 's3.secret-access-key' in response.config
  assert 's3.session-token' in response.config

  s3 = boto3.client('s3',
                    aws_access_key_id=response.config['s3.access-key-id'],
                    aws_secret_access_key=response.config['s3.secret-access-key'],
                    aws_session_token=response.config['s3.session-token'])

  objects = s3.list_objects(Bucket=test_bucket, Delimiter='/',
                            Prefix='polaris_test/snowflake_catalog/db1/schema/iceberg_table/metadata/')
  assert objects is not None
  assert 'Contents' in objects
  assert len(objects['Contents']) > 0

  metadata_file = next(f for f in objects['Contents'] if f['Key'].endswith('metadata.json'))
  assert metadata_file is not None

  metadata_contents = s3.get_object(Bucket=test_bucket, Key=metadata_file['Key'])
  assert metadata_contents is not None
  assert metadata_contents['ContentLength'] > 0

  put_object = s3.put_object(Bucket=test_bucket, Key=f"{metadata_file['Key']}.bak",
                             Body=metadata_contents['Body'].read())
  assert put_object is not None
  assert 'VersionId' in put_object
  assert put_object['VersionId'] is not None

  # list files in the other table's directory. The access policy should restrict this
  try:
    objects = s3.list_objects(Bucket=test_bucket, Delimiter='/',
                              Prefix='polaris_test/snowflake_catalog/db1/schema/iceberg_table_2/metadata/')
    pytest.fail('Expected exception listing file outside of table directory')
  except botocore.exceptions.ClientError as error:
    print(error)

  try:
    metadata_contents = s3.get_object(Bucket=test_bucket, Key=table2_metadata)
    pytest.fail("Expected exception reading file outside of table directory")
  except botocore.exceptions.ClientError as error:
    print(error)

  with IcebergSparkSession(credentials=f'{snowman.principal.client_id}:{snowman.credentials.client_secret}',
                           catalog_name=snowflake_catalog.name,
                           polaris_url=polaris_catalog_url) as spark:
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('USE db1.schema')
    spark.sql('DROP TABLE iceberg_table')
    spark.sql('DROP TABLE iceberg_table_2')
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('DROP NAMESPACE db1.schema')
    spark.sql('DROP NAMESPACE db1')


@pytest.mark.skipif(os.environ.get('AWS_TEST_ENABLED', 'false').lower() != 'true', reason='AWS_TEST_ENABLED is not set or is false')
def test_spark_credentials_s3_direct_without_write(root_client, snowflake_catalog, polaris_catalog_url,
                                                   snowman, reader_catalog_client, test_bucket):
  """
  Create two tables using Spark. Then call the loadTable api directly with test_reader token to fetch the vended
  credentials for the first table.
  Verify that the credentials returned to test_reader allow reads, but don't allow writes to the table's directory
  and don't allow reads or writes anywhere else on S3. This verifies that Polaris's authz model does not only prevent
  users from updating metadata to enforce read-only access, but uses credential scoping to enforce restrictions at
  the storage layer.
  :param root_client:
  :param snowflake_catalog:
  :param polaris_catalog_url:
  :param reader_catalog_client:
  :return:
  """
  with IcebergSparkSession(credentials=f'{snowman.principal.client_id}:{snowman.credentials.client_secret}',
                           catalog_name=snowflake_catalog.name,
                           polaris_url=polaris_catalog_url) as spark:
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('CREATE NAMESPACE db1')
    spark.sql('CREATE NAMESPACE db1.schema')
    spark.sql('USE db1.schema')
    spark.sql('CREATE TABLE iceberg_table (col1 int, col2 string)')
    spark.sql('CREATE TABLE iceberg_table_2 (col1 int, col2 string)')

  table2_metadata = reader_catalog_client.load_table(snowflake_catalog.name, unquote('db1%1Fschema'),
                                                     "iceberg_table_2",
                                                     "s3_direct_with_write_table2").metadata_location

  response = reader_catalog_client.load_table(snowflake_catalog.name, unquote('db1%1Fschema'), "iceberg_table",
                                              "s3_direct_without_write")
  assert response.config is not None
  assert 's3.access-key-id' in response.config
  assert 's3.secret-access-key' in response.config
  assert 's3.session-token' in response.config

  s3 = boto3.client('s3',
                    aws_access_key_id=response.config['s3.access-key-id'],
                    aws_secret_access_key=response.config['s3.secret-access-key'],
                    aws_session_token=response.config['s3.session-token'])

  objects = s3.list_objects(Bucket=test_bucket, Delimiter='/',
                            Prefix='polaris_test/snowflake_catalog/db1/schema/iceberg_table/metadata/')
  assert objects is not None
  assert 'Contents' in objects
  assert len(objects['Contents']) > 0

  metadata_file = next(f for f in objects['Contents'] if f['Key'].endswith('metadata.json'))
  assert metadata_file is not None

  metadata_contents = s3.get_object(Bucket=test_bucket, Key=metadata_file['Key'])
  assert metadata_contents is not None
  assert metadata_contents['ContentLength'] > 0

  # try to write. Expect it to fail
  try:
    put_object = s3.put_object(Bucket=test_bucket, Key=f"{metadata_file['Key']}.bak",
                               Body=metadata_contents['Body'].read())
    pytest.fail("Expect exception trying to write to table directory")
  except botocore.exceptions.ClientError as error:
    print(error)

  # list files in the other table's directory. The access policy should restrict this
  try:
    objects = s3.list_objects(Bucket=test_bucket, Delimiter='/',
                              Prefix='polaris_test/snowflake_catalog/db1/schema/iceberg_table_2/metadata/')
    pytest.fail('Expected exception listing file outside of table directory')
  except botocore.exceptions.ClientError as error:
    print(error)

  try:
    metadata_contents = s3.get_object(Bucket=test_bucket, Key=table2_metadata)
    pytest.fail("Expected exception reading file outside of table directory")
  except botocore.exceptions.ClientError as error:
    print(error)

  with IcebergSparkSession(credentials=f'{snowman.principal.client_id}:{snowman.credentials.client_secret}',
                           catalog_name=snowflake_catalog.name,
                           polaris_url=polaris_catalog_url) as spark:
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('USE db1.schema')
    spark.sql('DROP TABLE iceberg_table')
    spark.sql('DROP TABLE iceberg_table_2')
    spark.sql(f'USE {snowflake_catalog.name}')
    spark.sql('DROP NAMESPACE db1.schema')
    spark.sql('DROP NAMESPACE db1')


def create_principal(polaris_url, polaris_catalog_url, api, principal_name):
  principal = Principal(name=principal_name, type="SERVICE")
  try:
    principal_result = api.create_principal(CreatePrincipalRequest(principal=principal))

    token_client = CatalogApiClient(Configuration(username=principal_result.principal.client_id,
                                                  password=principal_result.credentials.client_secret,
                                                  host=polaris_catalog_url))
    oauth_api = IcebergOAuth2API(token_client)
    token = oauth_api.get_token(scope='PRINCIPAL_ROLE:ALL', client_id=principal_result.principal.client_id,
                                client_secret=principal_result.credentials.client_secret,
                                grant_type='client_credentials',
                                _headers={'realm': 'default-realm'})
    rotate_client = ManagementApiClient(Configuration(access_token=token.access_token,
                                                      host=polaris_url))
    rotate_api = PolarisDefaultApi(rotate_client)

    rotate_credentials = rotate_api.rotate_credentials(principal_name=principal_name)
    return rotate_credentials
  except ApiException as e:
    if e.status == 409:
      return rotate_api.rotate_credentials(principal_name=principal_name)
    else:
      raise e


def create_catalog_role(api, catalog, role_name):
  catalog_role = CatalogRole(name=role_name)
  try:
    api.create_catalog_role(catalog_name=catalog.name,
                            create_catalog_role_request=CreateCatalogRoleRequest(catalog_role=catalog_role))
    return api.get_catalog_role(catalog_name=catalog.name, catalog_role_name=role_name)
  except ApiException as e:
    return api.get_catalog_role(catalog_name=catalog.name, catalog_role_name=role_name)
  else:
    raise e


def create_principal_role(api, role_name):
  principal_role = PrincipalRole(name=role_name)
  try:
    api.create_principal_role(CreatePrincipalRoleRequest(principal_role=principal_role))
    return api.get_principal_role(principal_role_name=role_name)
  except ApiException as e:
    return api.get_principal_role(principal_role_name=role_name)
