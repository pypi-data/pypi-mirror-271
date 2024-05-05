import asyncio
import atexit
import os.path
import subprocess
import re
import typing
import aiohttp
import inflection


class HubStudioAsync:
    def __init__(self, host: str = "localhost", port: int = 16000):
        self.__http_port = port
        self.__host = host

    @staticmethod
    async def start_local_server(
        app_id: str,
        app_secret: str,
        group_code: str,
        http_port: int = 16000,
        line_setting: int = None,
        timeout: int = 600,
        remote_debugging: bool = False,
        threads: int = 10,
        client_path: str = None,
        echo: bool = False,
    ):
        """
        启动HubStudio API服务
        :param echo:
        :param http_port: 服务端口
        :param app_id:
        :param app_secret:
        :param group_code:
        :param line_setting: 线路设置
        :param timeout: 请求的超时时间(秒)
        :param remote_debugging: 是否将API服务暴露到公网
        :param threads: API服务的线程数
        :param client_path: Hubstudio的客户端安装路径(包含 hubstudio_connector.exe 的目录)
        :return:
        """
        cmds = [
            "--server_mode", "http",
            f"--app_id={app_id}",
            f"--app_secret={app_secret}",
            f"--group_code={group_code}",
            f"--http_port={http_port}",
            f"--timeout={timeout}",
            f"--threads={threads}",
        ]
        if remote_debugging:
            cmds.append("--remote_debugging")
        if line_setting:
            cmds.append(f"--line_setting={line_setting}")

        p = await asyncio.create_subprocess_exec(
            os.path.join(client_path, "hubstudio_connector.exe"),
            *cmds,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
        atexit.register(p.kill)
        while True:
            output_line = await p.stdout.readline()
            output_line = output_line.decode().strip()
            if echo:
                print(output_line)
            if re.match(r'Program started: +{"\d+":"hubstudio_connector.exe"', output_line):
                break
            elif re.match(r'.*?starting http server at:', output_line):
                api_url = re.search(r"(\d+\.\d+\.\d+\.\d+:\d+)", output_line).group(1)
                return api_url
            elif output_line == 'Startup complete':
                break

    async def __request(self, url: str, payload: dict = None, camelize: bool = True):
        url = f"http://{self.__host}:{self.__http_port}{url}"
        if payload is not None:
            if camelize:
                payload.pop("self")
                payload = {inflection.camelize(k, False): v for k, v in payload.items()}
        headers = {"Content-Type": "application/json"}
        async with aiohttp.request("POST", url, json=payload, headers=headers) as resp:
            return await resp.json()

    async def login(self, app_id: str, app_secret: str, group_code: str):
        """
        帐号登录并打开客户端

        1. http模式需配合使用CLI命令行启动客户端，见【HTTP模式说明】
        2. 启动时已传入用户团队参数，可跳过此步骤
        3. 重新登录会重启客户端

        :param app_id: 用户凭证appId
        :param app_secret: 用户凭证appSecret
        :param group_code: 	团队id
        :return:
        """

        payload = locals()
        return await self.__request("/login", payload)

    async def quit(self):
        """
        退出并关闭客户端

        :return:
        """
        return await self.__request("/quit")

    async def list_environments(
        self,
        container_codes: list[str | int] = None,
        container_name: str = None,
        create_end_time: str = None,
        create_start_time: str = None,
        ip_address: str = None,
        proxy_type_names: list = None,
        remark: str = None,
        no_tag: int = None,
        tag_names: list = None,
        current: int = None,
        size: int = None,
        service_provider: str = None
    ):
        """
        获取环境列表

        :param container_codes: list, 指定环境ID查询环境
        :param container_name: str, 指定环境名称查询环境
        :param create_end_time: str, 创建时间-截止时间
        :param create_start_time: str, 创建时间-起始时间
        :param ip_address: str, IP地址查询
        :param proxy_type_names: list, 代理类型
        :param remark: str, 指定环境备注信息查询环境
        :param no_tag: int, 查询“未分组”的环境
        :param tag_names: list, 环境分组名称数组
        :param current: int, 分页第几页偏移量
        :param size: int, 分页条数，最多200条
        :param service_provider: str, 环境内代理所属服务商
        :return: JSON, 环境列表信息
        """
        payload = locals()
        return await self.__request("/api/v1/env/list", payload)

    async def create_environment(
            self,
            container_name: str,
            as_dynamic_type: int,
            proxy_type_name: str,
            remark: str = None,
            tag_name: str = None,
            cookie: str = None,
            ip_get_rule_type: int = None,
            link_code: str = None,
            proxy_server: str = None,
            proxy_port: int = None,
            proxy_account: str = None,
            proxy_password: str = None,
            reference_country_code: str = None,
            reference_ip: str = None,
            reference_city: str = None,
            reference_region_code: str = None,
            ip_database_channel: int = None,
            ip_protocol_type: int = None,
            type: str = None,
            phone_model: str = None,
            browser: str = None,
            core_version: int = None,
            video_throttle: int = None,
            img_throttle: int = None,
            advanced_bo: dict = None
    ):
        """
        创建环境

        :param container_name: str, 环境名称
        :param as_dynamic_type: int, IP变更提醒；1-静态 ，2-动态
        :param proxy_type_name: str, 代理类型: 	1、自定义代理类型：HTTP、HTTPS、SSH、Socks5、Oxylabsauto、Lumauto_HTTP 、Lumauto_HTTPS 、Luminati_HTTP、Luminati_HTTPS、 smartproxy、Iphtml_HTTP、Iphtml_Socks5、IPIDEA、不使用代理              2、API提取代理类型：  Socks5_ROLA_IP、HTTPS_ROLA_IP、 Socks5_922S5、HTTP_922S5、HTTPS_922S5、 Socks5_通用api、HTTP_通用api、HTTPS_通用api、Socks5_IPIDEA-API、HTTP_IPIDEA-API、HTTPS_IPIDEA-API
        :param remark: str, 环境备注信息
        :param tag_name: str, 环境所属分组名称
        :param cookie: str, JSON格式的cookie
        :param ip_get_rule_type: int, IP提取方式
        :param link_code: str, 提取链接
        :param proxy_server: str, 代理主机
        :param proxy_port: int, 代理端口
        :param proxy_account: str, 代理账号
        :param proxy_password: str, 代理密码
        :param reference_country_code: str, 环境内账号需要登录的指定的国家
        :param reference_ip: str, 根据IP自动填充环境内账号需要登录的指定的国家
        :param reference_city: str, 参考城市
        :param reference_region_code: str, 参考州
        :param ip_database_channel: int, 代理查询渠道
        :param ip_protocol_type: int, IP协议选项
        :param type: str, 操作系统参数
        :param phone_model: str, 手机型号
        :param browser: str, 浏览器类型
        :param core_version: int, 内核版本号
        :param video_throttle: int, 视频限流
        :param img_throttle: int, 图片限流
        :param advanced_bo: dict, 高级指纹参数配置
        :return: JSON, 创建后的环境信息
        """
        payload = locals()
        return await self.__request("/api/v1/env/create", payload)

    async def start_browser(
            self,
            container_code: str | int,
            is_webdriver_read_only_mode: bool = False,
            skip_system_resource_check: bool = False,
            container_tabs: list[str] = None,
            args: list[str] = None
    ):
        """
        启动浏览器

        :param container_code: str | int, 环境ID
        :param is_webdriver_read_only_mode: bool, 是否只读模式，默认False
        :param skip_system_resource_check: bool, 默认False不跳过系统资源检测(仅支持v3.6.0及以上版本)
        :param container_tabs: list[str], 启动URL，可选
        :param args: list[str], 启动参数，可选
        :return: dict, 包含浏览器信息的字典
        """
        payload = locals()
        return await self.__request("/api/v1/browser/start", payload)

    async def stop_browser(
            self,
            container_code: str | int
    ):
        """
        关闭环境

        :param container_code: str | int, 环境ID
        :return: dict, 包含操作信息的字典
        """
        payload = locals()
        return await self.__request("/api/v1/browser/stop", payload)

    async def get_browser_status(
            self,
            container_codes: list[str | int]
    ):
        """
        获取浏览器状态

        :param container_codes: list[str | int], 环境ID列表
        :return: dict, 包含环境状态信息的字典
        """
        payload = locals()
        return await self.__request("/api/v1/browser/all-browser-status", payload)

    async def switch_browser_window(
            self,
            container_code: str
    ):
        """
        切换浏览器窗口

        :param container_code: str, 环境ID
        :return: dict, 包含操作信息的字典
        """
        payload = locals()
        return await self.__request("/api/v1/browser/foreground", payload)

    async def update_environment(
            self,
            container_code: int,
            container_name: str,
            tag_name: typing.Optional[str],
            core_version: int,
            remark: str = None,
            video_throttle: int = None,
            img_throttle: int = None,
            advanced_bo: dict = None
    ):
        """
        更新环境

        :param container_code: int | str, 环境ID
        :param container_name: str, 环境名称
        :param core_version: int, 内核版本号
        :param remark: str, 环境备注信息
        :param tag_name: str, 环境所属分组信息
        :param video_throttle: int, 视频限流
        :param img_throttle: int, 图片限流
        :param advanced_bo: dict, 高级指纹参数配置
        :return: bool, 更新成功与否
        """
        payload = locals()
        return await self.__request("/api/v1/env/update", payload)

    async def update_environment_proxy(
            self,
            container_code: int | str,
            as_dynamic_type: int,
            proxy_type_name: str,
            ip_get_rule_type: int = None,
            link_code: str = None,
            proxy_host: str = None,
            proxy_port: int = None,
            proxy_account: str = None,
            proxy_password: str = None,
            reference_country_code: str = None,
            reference_ip: str = None,
            reference_city: str = None,
            reference_region_code: str = None,
            ip_database_channel: int = None,
            ip_protocol_type: int = None
    ):
        """
        更新环境代理

        :param container_code: int | str, 环境ID
        :param as_dynamic_type: int, IP使用方式 1-静态 ，2-动态
        :param proxy_type_name: str, 代理类型 1、自定义代理类型：HTTP、HTTPS、SSH、Socks5、Oxylabsauto、Lumauto_HTTP 、Lumauto_HTTPS 、Luminati_HTTP、Luminati_HTTPS、 smartproxy、Iphtml_HTTP、Iphtml_Socks5、IPIDEA、不使用代理              2、API提取代理类型：  Socks5_ROLA_IP、HTTPS_ROLA_IP、 Socks5_922S5、HTTP_922S5、HTTPS_922S5、 Socks5_通用api、HTTP_通用api、HTTPS_通用api、Socks5_IPIDEA-API、HTTP_IPIDEA-API、HTTPS_IPIDEA-API
        :param ip_get_rule_type: int, IP提取方式
        :param link_code: str, 提取链接
        :param proxy_host: str, 代理主机
        :param proxy_port: int, 代理端口
        :param proxy_account: str, 代理账号
        :param proxy_password: str, 代理密码
        :param reference_country_code: str, 环境内账号需要登录的指定的国家
        :param reference_ip: str, 根据IP自动填充环境内账号需要登录的指定的国家
        :param reference_city: str, 参考城市
        :param reference_region_code: str, 参考州
        :param ip_database_channel: int, 代理查询渠道
        :param ip_protocol_type: int, IP协议选项
        :return: bool, 更新成功与否
        """
        payload = locals()
        return await self.__request("/api/v1/env/proxy/update", payload)

    async def delete_environment(
            self,
            container_codes: list[int | str]
    ):
        """
        删除环境
        :param container_codes: list[int | str], 环境ID列表
        :return: bool, 删除成功与否
        """
        payload = locals()
        return await self.__request("/api/v1/env/del", payload)

    async def import_cookie(
            self,
            container_code: int | str,
            cookie: str
    ):
        """
        导入Cookie

        :param container_code: int | str, 环境ID
        :param cookie: str, JSON格式的cookie字符串
        :return: bool, 导入成功与否
        """
        payload = locals()
        return await self.__request("/api/v1/env/import-cookie", payload)

    async def export_cookie(
            self,
            container_code: int | str
    ):
        """
        导出Cookie

        :param container_code: int | str, 环境ID
        :return: str, Cookie的JSON串
        """
        payload = locals()
        return await self.__request("/api/v1/env/export-cookie", payload)

    async def get_random_ua(
            self,
            type: str = None,
            phone_model: str = None,
            version: list[int] = None
    ):
        """
        获取随机UA

        :param type: str, 操作系统参数
        :param phone_model: str, 手机型号
        :param version: list[int], 浏览器版本数组
        :return: str, 随机UA字符串
        """
        payload = locals()
        return await self.__request("/api/v1/env/random-ua", payload)

    async def clear_environment_cache(
            self,
            browser_oauths: list[str | int] = None
    ):
        """
        清除环境本地缓存

        :param browser_oauths: list[str], 环境ID列表
        :return: JSON, 操作结果
        """
        payload = locals()
        return await self.__request("/api/v1/cache/clear", payload)

    async def reset_environment_extension(
            self,
            browser_oauth: str,
            plugin_ids: list[str]
    ):
        """
        清理环境内插件缓存

        :param browser_oauth: str, 浏览器OAuth ID
        :param plugin_ids: list[str], 插件ID列表
        :return: JSON, 操作结果
        """
        payload = locals()
        return await self.__request("/api/v1/browser/reset-extension", payload)

    async def download_environment_core(self, *cores):
        """
        下载环境内核

        :param cores: list[dict]
        浏览器内核类型，1-Chrome，2-Firefox
            {
                "Cores":[
                    {
                        "BrowserType":1,
                        "Version":"109"
                    },
                    {
                        "BrowserType":2,
                        "Version":"110"
                    }
                ]
            }
        :return: JSON, 操作结果
        """
        return await self.__request("/api/v1/browser/download-core", {"Cores": cores}, camelize=False)

    async def get_environment_groups(self):
        """
        获取环境分组列表

        :return: list[dict], 分组名称和分组ID
        """
        return await self.__request("/api/v1/group/list")

    async def create_environment_group(self, tag_name: str):
        """
        新建环境分组

        :param tag_name: str, 命名环境分组
        :return: bool
        """
        payload = {"tagName": tag_name}
        return await self.__request("/api/v1/group/create", payload)

    async def delete_environment_group(self, tag_code: str):
        """
        删除环境分组
        :param tag_code: str, 删除指定名称的分组
        :return: bool
        """
        payload = {"tagCode": tag_code}
        return await self.__request("/api/v1/group/del", payload)


