import os

BOHRIUM_ENV = os.getenv('BOHRIUM_ENV')
PROD_ENV = BOHRIUM_ENV not in ('test', 'uat')

if BOHRIUM_ENV == 'test':
    _LEBESGUE_ADDRESS = 'https://bohrium.test.dp.tech/'
elif BOHRIUM_ENV == 'uat':
    _LEBESGUE_ADDRESS = 'https://bohrium.uat.dp.tech/ '
else:
    _LEBESGUE_ADDRESS = 'https://bohrium.dp.tech/'


class ConfigKey:
    CURRENT_PROGRAM_ID = 'PROGRAM_CURRENT_PROGRAM_ID'
    DEFAULT_OUTPUT_FORMAT = 'DEFAULT_OUTPUT_FORMAT'
    ACCOUNT_EMAIL = 'ACCOUNT_EMAIL'
    ACCOUNT_PASSWORD = 'ACCOUNT_PASSWORD'
    ALI_OSS_ENDPOINT = 'ALI_OSS_ENDPOINT'
    LEBESGUE_ADDRESS = 'LEBESGUE_ADDRESS'
    CONFIG_FILE_DIR = 'CONFIG_FILE_DIR'
    STORAGE_BUCKET_NAME = 'STORAGE_BUCKET_NAME'
    CHECK_VERSION_LEVEL = "CHECK_VERSION_LEVEL"
    TIEFBLUE_BASE_URL = 'TIEFBLUE_BASE_URL'


class GlobalConfig:
    # LEBESGUE_ADDRESS = 'https://test.dp.tech/'
    # LEBESGUE_ADDRESS = 'http://172.16.8.21:8000/'
    LEBESGUE_ADDRESS = _LEBESGUE_ADDRESS
    STORAGE_ENDPOINT = 'oss-cn-shenzhen.aliyuncs.com'
    STORAGE_BUCKET_NAME = 'dpcloudserver' if PROD_ENV else 'dpcloudserver-test'
    CONFIG_ACTION_RECORD = 'lbg_action.csv'
    CONFIG_FILE_DIR_SECONDARY = '~/.lbg/'
    CONFIG_FILE_DIR_PRIMARY = '/personal/.lbg/'
    CONFIG_FILE_NAME = 'lbg_cli_context.json'
    CALLER_NAME = 'lbg'
    CHECK_VERSION_LEVEL = 1
    TIEFBLUE_BASE_URL = 'http://tiefblue.dp.tech'
    SOURCE_FROM = 'lbg-utility'
