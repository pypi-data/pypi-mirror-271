# ParamInfo 类表示设备需要执行的指令
class Commands:
    def __init__(self, param_name, param_value):
        self.paramName = param_name  # 指令名，与 JSON 键 "paramName" 匹配
        self.paramValue = param_value  # 指令值，与 JSON 键 "paramValue" 匹配

    # 这个方法将实例状态转化为jsonizable的dict
    def to_dict(self):
        return {
            'code': self.paramName,
            'value': self.paramValue
        }


# ControlDevice 类表示控制设备
class ControlDevice:
    def __init__(self, device_no, house_no):
        self.device_no = device_no  # 设备编号，与 JSON 键 "deviceNo" 匹配
        self.house_no = house_no  # 终端序列号，与 JSON 键 "terminalSequence" 匹配
        self.commands = []  # 设备需要执行的指令数组，与 JSON 键 "instructions" 匹配

    def add_param_info(self, code, value):
        commands = Commands(code, value)
        self.commands.append(commands)

    def remove_param_info(self):
        self.commands.clear()

    # 这个方法将实例状态转化为jsonizable的dict
    def to_dict(self):
        # Convert self.paramInfo to a list of dictionaries
        commands_list = [
            # Assuming that ParamInfo also has a to_dict method
            # You might need to create one
            command.to_dict()
            for command in self.commands
        ]

        return {
            'deviceNo': self.device_no,
            'houseNo': self.house_no,
            'commands': commands_list,
        }
