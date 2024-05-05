# V3 继续使用jaydebeapi 实现多线程,完美实现
import jaydebeapi
from readscripts import read_multi_sql_file as rsql
from concurrent.futures import ProcessPoolExecutor, as_completed
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Semaphore
import jpype
import jpype.imports
from jpype.types import *
import os
from . import JAR_FILES

class DatabaseClient:
    def __init__(self, host, username, password, max_cursors=10,if_header_included = False):
        self.host = host
        self.username = username
        self.password = password
        self.connection = self.get_connection()
        self.cursor_semaphore = Semaphore(max_cursors)
        self.executor = ThreadPoolExecutor(max_workers=max_cursors)
        self.futures = []
        self.if_header_included = if_header_included
    def _java_to_python(self, value):
        """
        将 Java 类型转换为 Python 类型。
        """
        if isinstance(value,jpype.java.lang.Integer):
            return int(value)
        if isinstance(value, jpype.java.lang.Long):
            return int(value)
        if isinstance(value, jpype.java.lang.Double):
            return float(value)
        if isinstance(value, jpype.java.lang.Boolean):
            return bool(value)
        return value
        
    def get_connection(self):
        try:
            """
            建立与数据库的连接
            """
            driver = 'com.bonc.xcloud.jdbc.XCloudDriver'
            url = f'jdbc:xcloud:@{self.host}/SERVER_DATA?connectRetry=3&socketTimeOut=43200000&connectDirect=true&buffMemory=33554432'
            conn = jaydebeapi.connect(jclassname=driver, url=url, driver_args=[self.username, self.password], jars=JAR_FILES)
            return conn
        except jaydebeapi.DatabaseError as e:
            print(f'the connection was not consistent ,because of {e}')
            raise


    def execute_query(self, query):
        with self.cursor_semaphore:
            future = self.executor.submit(self.run_query, query)
            self.futures.append(future)
            return future

    def execute_queries_no_sequences(self, queries):
        with self.cursor_semaphore:  # 控制游标数量
            for query in queries:
                self.execute_query(query)  # 使用之前定义的方法提交查询
            return [future.result() for future in self.futures]
    
    def execute_queries(self, queries):
        with self.cursor_semaphore:  # 控制游标数量
            future_to_index = {}
            results = [None] * len(queries)  # 初始化结果列表为 None，长度与查询列表相同

            for i, query in enumerate(queries):
                future = self.executor.submit(self.run_query, query)
                self.futures.append(future)
                future_to_index[future] = i  # 将 future 与其对应的查询索引相关联

            for future in self.futures:
                index = future_to_index[future]  # 获取原始查询的索引
                try:
                    results[index] = future.result()  # 将结果放置在正确的位置
                except Exception as e:
                    results[index] = None  # 处理可能的异常
                    print(f"Error processing query at index {index}: {e}")

            return results


    def run_query(self, query):
        """
        执行查询并返回结果
        """
        if self.connection:
            header = []
            try:
                cursor = self.connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                header = [tuple([i[0] for i in cursor.description])]
                python_results = [
                    [self._java_to_python(value) for value in row] for row in result
                ]
                cursor.close()
            except jaydebeapi.Error as e:
                print(f"Error executing query: {e}")
                raise
            if self.if_header_included:
                return header+python_results 
            else:
                return python_results


    def close_connection(self):
        self.executor.shutdown(wait=True)
        if self.connection:
            self.connection.close()
            self.connection = None



def run_query_in_process(ip, username, password, queries,if_header_included = False):
    #DatabaseClient.start_jvm()  # 在每个进程中启动 JVM
    client = DatabaseClient(ip, username, password, 10,if_header_included)
    return client.execute_queries(queries)  # 修改为接收一个查询列表

class ClientManager:
    def __init__(self, client_configs, max_cursors=10):
        self.client_configs = client_configs
        self.max_cursors = max_cursors
        self.process_pool = ProcessPoolExecutor(max_workers=len(client_configs))

    def execute_queries(self, queries,if_header_included):
        num_clients = len(self.client_configs)
        queries_per_client = [queries[i::num_clients] for i in range(num_clients)]
        futures = []
        index_to_result = [None] * len(queries)  # 创建与 queries 等长的结果列表，初始化为 None

        # 分发查询到各个客户端
        for i, (config, query_set) in enumerate(zip(self.client_configs, queries_per_client)):
            future = self.process_pool.submit(run_query_in_process, config['ip'], config['username'], config['password'], query_set,if_header_included)
            start_index = i
            step = num_clients
            futures.append((future, start_index, step))  # 保存每个 future 以及其对应查询的开始索引和步长

        # 收集结果并按原始顺序存放
        for future, start_index, step in futures:
            try:
                result_set = future.result()
                for offset, result in enumerate(result_set):
                    index_to_result[start_index + offset * step] = result
            except Exception as e:
                print(f"Error retrieving results: {e}")

        # 过滤掉 None 值，如果有的话
        if len(index_to_result) != len(queries):
            raise 
        else:
            return [result for result in index_to_result if result is not None]

    def close_all_connections(self):
        self.process_pool.shutdown(wait=True)


#class ServerCongestionDetector:
    #def __init__(self, server_ips):
        #self.server_ips = server_ips
        #self.response_times = {ip: float('inf') for ip in server_ips}
    
    #def test_server_response_time(self, ip):
        #start_time = time.time()
        #try:
            ## 模拟建立连接和执行基准查询
            ## 实际中应该创建数据库连接并执行查询，这里仅为示例
            #time.sleep(0.1)  # 假设响应时间
            #response_time = time.time() - start_time
            #return ip, response_time
        #except Exception as e:
            #return ip, float('inf')  # 如果发生错误，返回无限大的响应时间
    
    #def update_server_response_times(self):
        #with ThreadPoolExecutor(max_workers=len(self.server_ips)) as executor:
            #futures = [executor.submit(self.test_server_response_time, ip) for ip in self.server_ips]
            #for future in as_completed(futures):
                #ip, response_time = future.result()
                #self.response_times[ip] = response_time
    
    #def get_least_congested_server(self):
        ##self.update_server_response_times()
        ### 选择响应时间最短的服务器
        ##least_congested_server = min(self.response_times, key=self.response_times.get)
        ##if self.response_times[least_congested_server] > 180:  # 超过3分钟
            ##time.sleep(300)  # 暂停5分钟
            ##return self.get_least_congested_server()  # 重新检测
        ##return least_congested_server
        #return '133.65.120.51:9005'

# 使用示例
#if __name__ == "__main__":
    #detector = ServerCongestionDetector(['192.168.1.1', '192.168.1.2', '192.168.1.3'])
    #best_server_ip = detector.get_least_congested_server()
    #print(f"Connect to the least congested server: {best_server_ip}")
