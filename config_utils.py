import os
import configparser
from typing import Dict, Any, Optional, Union, List

class ConfigParser:
	def __init__(
		self,
		env_var_name: Optional[str] = None,
		user_config_paths: Optional[Union[str, List[str]]] = None,
		system_config_paths: Optional[Union[str, List[str]]] = None,
		encoding: str = 'utf-8'
	):
		"""通用配置文件解析器
		
		Args:
			env_var_name: 环境变量名，用于指定配置文件路径
			user_config_paths: 用户配置文件路径(支持单个路径或路径列表)
				例如: '~/.config/myapp/config.ini'
			system_config_paths: 系统配置文件路径(支持单个路径或路径列表)
				例如: '/etc/myapp/config.ini'
			encoding: 配置文件编码，默认utf-8
		"""
		self.env_var_name = env_var_name
		self.user_config_paths = self._ensure_list(user_config_paths)
		self.system_config_paths = self._ensure_list(system_config_paths)
		self.encoding = encoding
		self.config = configparser.ConfigParser()
	
	@staticmethod
	def _ensure_list(paths: Optional[Union[str, List[str]]]) -> List[str]:
		"""确保路径参数为列表格式"""
		if paths is None:
			return []
		return [paths] if isinstance(paths, str) else paths
	
	def get_config_path(self) -> str:
		"""按优先级查找配置文件路径
		
		优先级顺序:
		1. 环境变量指定的路径
		2. 用户配置路径
		3. 系统配置路径
		
		Returns:
			str: 找到的第一个有效配置文件路径
			
		Raises:
			FileNotFoundError: 当所有路径都无效时抛出
		"""
		# 1. 检查环境变量
		if self.env_var_name:
			env_path = os.getenv(self.env_var_name)
			if env_path and os.path.exists(env_path):
				return env_path
		
		# 2. 检查用户配置路径
		for path in self.user_config_paths:
			user_path = os.path.expanduser(path)
			if os.path.exists(user_path):
				return user_path
		
		# 3. 检查系统配置路径
		for path in self.system_config_paths:
			system_path = os.path.expanduser(path)
			if os.path.exists(system_path):
				return system_path
		
		raise FileNotFoundError("No valid configuration file found")
	
	def parse(self, required_fields: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
		"""解析配置文件并返回字典格式的配置信息
		
		Args:
			required_fields: 必需的字段列表，如果指定，将检查每个section是否包含这些字段
		
		Returns:
			Dict[str, Dict[str, Any]]: 配置信息字典
			
		Raises:
			FileNotFoundError: 配置文件不存在时抛出
			configparser.Error: 配置文件格式错误时抛出
			ValueError: 缺少必需字段时抛出
		"""
		config_path = self.get_config_path()
		self.config.read(config_path, encoding=self.encoding)
		
		result = {}
		
		for section in self.config.sections():
			if section == 'DEFAULT':
				continue
			
			section_dict = dict(self.config[section])
			
			# 检查必需字段
			if required_fields:
				missing_fields = [
					field for field in required_fields 
					if field not in section_dict
				]
				if missing_fields:
					raise ValueError(
						f"Section '{section}' missing required fields: {missing_fields}"
					)
			
			result[section] = section_dict
		
		return result
	
	def get_value(
		self,
		section: str,
		key: str,
		default: Any = None,
		value_type: type = str
	) -> Any:
		"""获取指定配置项的值
		
		Args:
			section: 配置节名称
			key: 配置项名称
			default: 默认值
			value_type: 值类型转换函数
		
		Returns:
			转换后的配置值
		"""
		try:
			value = self.config.get(section, key)
			return value_type(value)
		except (configparser.Error, ValueError):
			return default 