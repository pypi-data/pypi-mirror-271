This package is designed for internal use only. Should you have any questions, please contact Zachary Yang via Teams or zachary.yang@tradeup.com

Release note 0.0.2   2023/10/18 13:55
Added Previous_BDay(), return previous business day
Added db_insert(), insert dataframes into database
Added data_pull, pull data from MySQL DB including original column names


Release note 0.0.3   2023/10/30 15:18
Added clear_table(), clear records based on customized conditions
Added last_business_day()

Release note 0.0.4   2023/11/09 15:37
Added to_float(), used mainly in BR parsing, e.g. change string '9,000,154.91-' to float -9000154.91

Release note 0.0.5   2023/11/29 16:43
Created function create_partition(), automatically create partition of next month for each table, with hard coded user name and password

Release note 0.1.1   2024/05/02 10:59
Defined all functions under class Amazon as static method, no need to include argument 'self' when calling functions

Release note 0.1.2   2024/05/02 15:20
Excluded all 'self' under class amazon