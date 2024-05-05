"""
███████████████████████████client_usage of cloudpy_org███████████████████████████
Copyright © 2023-2024 Cloudpy.org

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
Find documentation at https://www.cloudpy.org
"""
from cloudpy_org import aws_framework_manager_client
import os
import awswrangler as wr
import pandas as pd
import re

class cloudpy_org_aws_framework_client:
    def __init__(self,aws_namespace:str,env:str='dev',region:str="us-east-2",token_path:str=None):
        self.aws_namespace = aws_namespace
        self.sufix = env
        self.region = region
        self.token_path = token_path
        self.current_path = os.getcwd() + '/'
        if self.token_path == None:
            self.token_path = self.current_path + aws_namespace + '.txt'
        self.aws = None
        self.errors = {}
        self.errors[1] = 'Invalid service token.'
        self.errors[2] = 'No aws framework client has been initialized yet.'
        self.errors[3] = 'Provided data format cannot be converted to json.'
        self._catalog_base_description = """GLUE Data Catalog '@catalog_name'.
        Created programmatically with cloudpy_org_aws_framework_client under the following criteria:
        cloudpy.org_aws_namespace = '@namespace', cloudpy.org_aws_env = '@env', region = '@region', creation_date='@creation_date'.
        Visit https://www.cloudpy.org/documentation.
        Additional custom description:@desc"""
        self.set_user_authentication_minutes_to_expire(30,print_res=False)
        self.aws_framework()
    #_________________________________________________________________________
    def set_user_authentication_minutes_to_expire(self,minutes:int,print_res:bool=True):
        self.user_authentication_minutes_to_expire = minutes
        if print_res:
            print('Temporal authentication token expiration for framework users has been set to ' + str(minutes) + ' minutes.')
    #_________________________________________________________________________
    def get_full_path(self,relative_path:str):
        relative_path = relative_path.replace('\\','/').replace('//','/').replace('//','')
        l = len(relative_path)
        if relative_path[l-1:l] == '/':
            relative_path = relative_path[0:l-1]
            l = len(relative_path)
        if relative_path[0:1] == '/':
            relative_path = relative_path[1:l]
        return self.s3_root_path + relative_path + '/'
    #_________________________________________________________________________
    def aws_framework(self):
        try:
            with open(self.token_path, 'r') as f:
                self.aws = aws_framework_manager_client(service_token=f.read(),aws_namespace=self.aws_namespace)
            self.bucket_name = self.aws.get_bucket_name(self.sufix,self.region)
            self.s3_root_path = 's3://' + self.bucket_name + '/'
            self._secrets_relative_path = '/settings/secrets/'
            self._users_relative_path = self._secrets_relative_path + 'users'
            self.__gen_key = self.get_s3_file_content(file_name='general_key.txt',relative_path=self._secrets_relative_path)
            self.athena = self.aws.ypt.b3session.client('athena')
            self.data_catalog_sufix = self.bucket_name.replace('cloudpy.org-','')
            banned_relative_paths = ['settings/','settings/secrets/users/','metadata/']
            self.banned_paths = [self.get_full_path(i) for i in banned_relative_paths]
        except Exception as e:
            print(self.errors[1])
    #_________________________________________________________________________
    def get_s3_file_content(self,file_name:str,relative_path:str):
        if self.aws != None:
            file_name,ext = self.__treat_file_name(file_name)
            s3FullFolderPath = self.get_full_path(relative_path)
            rslt = None
            if ext == 'json':
                try:
                    rslt = self.aws.ypt.get_s3_file_content(referenceName=file_name,s3FullFolderPath=s3FullFolderPath,exceptionCase=False)
                except:
                    try:
                        rslt = self.aws.ypt.get_s3_file_content(referenceName=file_name,s3FullFolderPath=s3FullFolderPath,exceptionCase=True)
                    except Exception as e:
                        print(str(e))
            else:
                rslt = self.aws.ypt.get_s3_file_content(referenceName=file_name,s3FullFolderPath=s3FullFolderPath,exceptionCase=True)
            return rslt
        else:
            print(self.errors[2])
            return None
    #_________________________________________________________________________
    def __treat_file_name(self,file_name:str):
        file_name = file_name.lower()\
        .replace('  ',' ')\
        .replace('  ',' ')\
        .replace('  ','')\
        .replace(' ','_')\
        .replace('__','_')\
        .replace('__','_')\
        .replace('__','')
        ext = file_name[::-1].split('.')[0][::-1]
        file_name = file_name.replace('.' + file_name[::-1].split('.')[0][::-1],'') + '.' + ext
        return file_name,ext
    #_________________________________________________________________________    
    def write_in_s3_folder(self,data:object,file_name:str,relative_path:str,print_res:bool=True):
        if self.aws != None:
            file_name,ext = self.__treat_file_name(file_name)
            s3FullFolderPath = self.get_full_path(relative_path)
            if ext == 'txt':
                if type(data) != str:
                    data = str(data)
                self.aws.ypt.store_str_as_file_in_s3_folder(
                    strInput=data
                    ,fileName=file_name
                    ,s3FullFolderPath=s3FullFolderPath
                    ,region_name=self.region
                    ,print_res=print_res)
            elif ext == 'json':
                cont = True
                if type(data) != dict:
                    data = str(data)
                    try:
                        data = self.aws.dictstr_to_dict(data)
                    except:
                        cont = False
                        print(self.errors[3])
                if cont:
                    try:
                        self.aws.ypt.standard_dict_to_json(jsonOrDictionary=data,fileName=file_name,folderPath=s3FullFolderPath,print_res=print_res)
                    except Exception as e:
                        print(str(e))
        else:
            print(self.errors[2])
    #_________________________________________________________________________        
    def create_user(self,username:str,email:str,pwd:str):
        rslt = self.aws.create_new_user(sufix=self.sufix,region=self.region,username=username,email=email,pwd=pwd)
        return rslt
    #_________________________________________________________________________
    def check_user(self,username_or_email:str):
        rslt = self.aws.check_if_user_exists_and_was_confirmed(username_or_email=username_or_email,sufix=self.sufix,region=self.region)
        return rslt
    #_________________________________________________________________________
    def confirm_user(self,username_or_email:str):
        user_check = self.check_user(username_or_email)
        uck = set(user_check.keys())
        if 'exists' in uck and 'confirmed' in uck and 'file_name' in uck:
            if user_check['confirmed'] == 0:
                rslt = self.get_s3_file_content(file_name=user_check['file_name'],relative_path=self._users_relative_path)
                rslt['confirmed_email'] = 1
                self.write_in_s3_folder(data=rslt,file_name=user_check['file_name'],relative_path=self._users_relative_path,print_res=False)
    #_________________________________________________________________________            
    def get_user_temp_token(self,username_or_email:str,pwd:str=None,email_notification:bool=False,temp_token:str=None):
        if email_notification:
            return self.__gut(username_or_email=username_or_email,email_notification=email_notification,temp_token=temp_token)
        else:
            return self.__gut(username_or_email=username_or_email,pwd=pwd)
    #_________________________________________________________________________
    def __gut(self,username_or_email:str,pwd:str=None,email_notification:bool=False,temp_token:str=None):
        user_check = self.check_user(username_or_email)
        uck = set(user_check.keys())
        if 'exists' in uck and 'confirmed' in uck and 'file_name' in uck:
            if user_check['exists']:
                if user_check['confirmed'] == 1:
                    f = user_check['file_name']
                    r = self._users_relative_path
                    data = self.get_s3_file_content(file_name=f,relative_path=r)
                    this_key = 'temp_token'
                    minutes_to_expire = self.user_authentication_minutes_to_expire
                    cont = False
                    if email_notification:
                        this_key = 'email_notification_token'
                        minutes_to_expire = 30
                        if self.user_token_authentication(username_or_email=username_or_email,temp_token=temp_token,email_notification=False):
                            cont = True
                    elif pwd == self.aws.ypt.decrypt(data['encrypted_pwd'],self.__gen_key):
                        cont = True
                    if cont:
                        temp_token = self.aws.ypt.encrypt(f,self.aws.ypt.gen_enc_key())
                        data[this_key] = self.aws.ypt.gen_encrypted_data_with_expiration(original_message=temp_token,minutes_to_expire=minutes_to_expire)
                        self.write_in_s3_folder(data=data,file_name=f,relative_path=r,print_res=False)
                        return temp_token
                    else:
                        return 'Wrong password.'
                else:
                    return 'User has not been confirmed.'
            else:
                return 'User does not exist.'
    #_________________________________________________________________________        
    def user_token_authentication(self,username_or_email:str,temp_token:str,email_notification:bool=False):
        return self.__uta(username_or_email=username_or_email,temp_token=temp_token,email_notification=email_notification)
    #_________________________________________________________________________
    def __uta(self,username_or_email:str,temp_token:str,email_notification:bool=False):
        user_check = self.check_user(username_or_email)
        uck = set(user_check.keys())
        if 'exists' in uck and 'confirmed' in uck and 'file_name' in uck:
            if user_check['exists']:
                if user_check['confirmed'] == 1:
                    f = user_check['file_name']
                    r = self._users_relative_path
                    data = self.get_s3_file_content(file_name=f,relative_path=r)
                    this_key = 'temp_token'
                    what = 'Token'
                    minutes_to_expire = self.user_authentication_minutes_to_expire
                    if email_notification:
                        this_key = 'email_notification_token'
                        what = 'Link'
                        minutes_to_expire = 30
                    try:
                        enc_data = data[this_key]
                        stored_token = self.aws.ypt.decrypt_before_expiration(data=enc_data)
                        if stored_token.lower().replace('.','').strip() == 'encryption expired':
                            print(what + ' expired.')
                    except Exception as e:
                        stored_token = None
                    if temp_token == stored_token:
                        return True
                    else:
                        new_temp_token = self.aws.ypt.encrypt(f,self.aws.ypt.gen_enc_key())
                        new_enc_data = self.aws.ypt.gen_encrypted_data_with_expiration(original_message=new_temp_token,minutes_to_expire=minutes_to_expire)
                        data[this_key] = new_enc_data
                        self.write_in_s3_folder(data=data,file_name=f,relative_path=r,print_res=False)
                        return False
                else:
                    return 'User has not been confirmed.'
            else:
                return 'User does not exist.'
    #__________________________________________________________________________
    def update_user_password(self,username_or_email:str,email_temp_token:str,new_pwd:str):
        self.__up(username_or_email=username_or_email,email_temp_token=email_temp_token,new_pwd=new_pwd)
    #__________________________________________________________________________
    def __up(self,username_or_email:str,email_temp_token:str,new_pwd:str):
        if self.user_token_authentication(username_or_email=username_or_email,temp_token=email_temp_token,email_notification=True):
            try:
                user_check = self.check_user(username_or_email)
                f = user_check['file_name']
                r = self._users_relative_path
                data = self.get_s3_file_content(file_name=f,relative_path=r)
                data['encrypted_pwd'] = self.aws.ypt.encrypt(new_pwd,self.__gen_key)
                self.write_in_s3_folder(data=data,file_name=f,relative_path=r,print_res=False)
                print('Password successfully updated')
                return True
            except:
                print('Error while trying to modify password.')
                return False
        else:
            print('Could not modify password.')
            return  False
    #__________________________________________________________________________
    def df_to_big_data_hive(self,df_input:pd.DataFrame,table_name:str,sink_relative_path:str='sinks',partition_cols:list=None):
        path = self.get_full_path(relative_path=sink_relative_path + table_name)
        wr.s3.to_parquet(
            df=df_input
            ,dataset=True
            ,path=path
            ,boto3_session=aws.aws.ypt.b3session
            ,partition_cols=partition_cols
        )
    #__________________________________________________________________________
    def create_data_catalog(self,catalog_name:str=None,description:str='',include_environment_tag:bool=True,catalog_id:str=None):
        if catalog_name == None:
            catalog_name = self.data_catalog_sufix + '-data-catalog'
        else:
            catalog_name = self._treat_name(catalog_name)
            if include_environment_tag:
                catalog_name = self.data_catalog_sufix + '-' + catalog_name
        
        date_id,time_id = self.aws.ypt.date_time_id(local=True)
        creation_date = self.aws.ypt.date_time_str(date_id,time_id)
        new_description = self._catalog_base_description\
        .replace('@catalog_name',catalog_name)\
        .replace('@namespace',self.aws_namespace)\
        .replace('@env',self.sufix)\
        .replace('@region',self.region)\
        .replace('@creation_date',creation_date)\
        .replace('@desc',description)
        try:
            if catalog_id == None:
                account_id = wr.sts.get_account_id(boto3_session=self.aws.ypt.b3session)
                catalog_id = account_id
            self.athena.create_data_catalog(
                Name=catalog_name
                ,Type='GLUE'
                ,Description=new_description
                ,Parameters={'catalog-id': catalog_id}
            )
            print('catalog_name: ',catalog_name)
            print('description: ',new_description)
        except Exception as e:
            r = str(e)
            if ': DataCatalog' in r:
                r = 'DataCatalog' + r.split(': DataCatalog')[1]
            print(r)
    #__________________________________________________________________________
    def _treat_name(self,name:str):
        name = name.lower().strip()\
        .replace('  ',' ')\
        .replace('  ',' ')\
        .replace('  ','')\
        .replace(' ','_')\
        .replace('__','_')\
        .replace('__','_')\
        .replace('__','')\
        .replace('--','-')\
        .replace('--','-')\
        .replace('--','')
        return name
    #__________________________________________________________________________
    def create_big_data_db(self,db_name:str,description:str):
        db_name = self._treat_name(db_name)
        try:
            wr.catalog.create_database(name=db_name,description=description,boto3_session=self.aws.ypt.b3session)
            return 'Database ' + db_name + ' succesfully created.'
        except Exception as e:
            return str(e).split('already exists')[0] + 'already exists.'
    #__________________________________________________________________________   
    def _update_get_datasources_schemas(self):
        catalogs = self.athena.list_data_catalogs()
        cats = {}
        for this_cat in [i['CatalogName'] for i in catalogs['DataCatalogsSummary']]:
            d = self.athena.list_databases(CatalogName=this_cat)
            cats[this_cat] = {}
            databases = {j['Name'] for j in d['DatabaseList']}
            for this_db in databases:
                cats[this_cat][this_db] = {}
                dd = self.athena.list_table_metadata(CatalogName=this_cat,DatabaseName=this_db)
                these_tables = [i['Name'] for i in dd['TableMetadataList']]
                for this_table in these_tables:
                    cats[this_cat][this_db][this_table] = {}
                    for m in dd['TableMetadataList']:
                        if m['Name'] == this_table:
                            this_metadata = m
                            these_keys = [x for x in set(this_metadata.keys()) if x != 'Name']
                            for this_key in these_keys:
                                cats[this_cat][this_db][this_table][self.aws.ypt.camel_to_snake(this_key)] = this_metadata[this_key]
                            break
        rslt = {}
        rslt['simple'] = {}
        rslt['complete'] = {}
        version = ['simple','complete']
        for a,b in cats.items():
            for u in version:
                rslt[u][a] = {}
            for c,d in b.items():
                for u in version:
                    rslt[u][a][c] = {}
                for e,f in d.items():
                    for u in version:
                        rslt[u][a][c][e] = {}
                    for g,h in f.items():
                        if g == 'columns':
                            for u in version:
                                rslt[u][a][c][e][g] = {hh['Name']:hh['Type'] for hh in h}
                        else:
                            rslt['complete'][a][c][e][g] = h
        self._datasources_schemas = rslt
    def show_datasources_schemas(self,version:bool='simple'):
        self._update_get_datasources_schemas()
        rslt = {}
        for k,v in self._datasources_schemas[version].items():
            if self.data_catalog_sufix in k:
                rslt[k] = v
        return rslt
    #__________________________________________________________________________    
    def create_athena_table(self,sink_path:str,db_name:str,table_name,columns_schema:dict,partition_cols:list):
        wr.athena.create_table(
            database=db_name,
            table=table_name,
            path=sink_path,
            columns_types=columns_schema,
            partition_cols=partition_cols
        )
    #__________________________________________________________________________
    def list_s3_object(self,relative_path:str=''):
        try:
            fp = self.get_full_path(relative_path)
            l = wr.s3.list_objects(path=fp,boto3_session=self.aws.ypt.b3session)
            rslt = [i.replace(fp,'') for i in l if '/' not in i.replace(fp,'')]
            rslt = set(rslt)
            rslt = list(rslt)
            rslt.sort()
        except Exception as e:
            print(str(e))
            rslt = []
        return rslt
    #__________________________________________________________________________
    def delete_s3_objects(self,relative_path:str,file_names:list=[],clear_all_directory:bool=False):
        folder_path = self.get_full_path(relative_path)
        if folder_path not in self.banned_paths:
            existing_files = self.list_s3_object(relative_path)
            if clear_all_directory:
                file_names = [folder_path + i for i in existing_files]
            else:
                file_names = [folder_path + i for i in file_names if i in existing_files]
            try:
                wr.s3.delete_objects(file_names,boto3_session=self.aws.ypt.b3session)
                print(str(len(file_names)) + ' objects deleted.')
            except Exception as e:
                print(str(e))
        else:
            m = "The directory path: '@folder_path' \n"\
            "constitutes an integral component of the foundational framework structure, thus precluding direct programmatic deletion.\n"\
            "While manual removal of objects within this directory is feasible within your AWS account, we strongly advise against such "\
            "action, as it may compromise the functionalities of your cloudpy.org environment framework.\n"\
            "For comprehensive guidelines on the proper deletion procedure for a cloudpy.org framework, we "\
            "recommend consulting our documentation at https://www.cloudpy.org/documentation."
            m = m.replace('@folder_path',folder_path)
            print(m)  
    #__________________________________________________________________________        
    def delete_user(self,username_or_email:str):
        folder_path = self.get_full_path(self._users_relative_path)
        this_check = self.check_user(username_or_email=username_or_email)
        if 'file_name' in set(this_check.keys()):
            file_names = [folder_path + this_check['file_name']]
            try:
                wr.s3.delete_objects(file_names,boto3_session=self.aws.ypt.b3session)
                print(this_check, ' objects deleted.')
            except Exception as e:
                print(str(e))
        else:
            print(this_check)