from __future__ import annotations

import re
from typing import Any

from pygments import token
from pygments.lexer import bygroups
from pygments.lexer import RegexLexer


class CRBasicLexer(RegexLexer):
    """
    For CRBasic language source code
    """
    name = 'CRBasic'
    url = 'https://help.campbellsci.com/crbasic/landing/Content/crbasic-help-home.htm'  # noqa: E501
    aliases = ('crbasic',)
    filenames = ('*.crb', '*.CRB')

    flags = re.IGNORECASE | re.MULTILINE

    KEYWORDS = (
        'StationName', 'Status', 'Alias', 'Units', 'As', 'And', 'BeginProg',
        'EndProg', 'CallTable', 'Call', 'Case Is', 'Case Else', 'Case', 'Is',
        'ConstTable', 'EndConstTable', 'DebugBreak', 'Debug', 'DataTable',
        'EndTable', 'DisplayMenu', 'EndMenu', 'ExitDo', 'Do', 'Loop', 'ElseIf',
        'Else', 'For', 'To', 'Next', 'ExitFor', 'Exit', 'Step', 'Function',
        'EndFunction', 'Return', 'ExitFunction', 'If', 'Then', 'EndIf', '#If',
        '#ElseIf', '#Else', '#EndIf', '#IfDef', 'Or', 'NextScan', 'ExitScan',
        'Scan', 'ContinueScan', 'Select', 'Case', 'EndSelect',
        'SequentialMode', 'SlowSequence', 'EndSequence', 'EndSub', 'ExitSub',
        'SubScan', 'NextSubScan', 'SubMenu', 'EndSubMenu', 'Sub', 'While',
        'Wend', 'Xor', 'End',
    )

    BUILTINS = (
        'ACPower', 'AddPrecise', 'AM25T', 'Average', 'AvgRun', 'AvgSpa', 'ABS',
        'AcceptDataRecords', 'ACos', 'ASCII', 'ASin', 'Atn', 'Atn2',
        'AngleDegrees', 'ApplyandRestartSequence',
        'EndApplyandRestartSequence', 'ArgosData', 'ArgosDataRepeat',
        'ArgosError', 'ArgosSetup', 'ArgosTransmit', 'ArrayLength', 'AVW200',
        'ArrayIndex', 'Battery', 'BeginBurstTrigger', 'BrFull', 'BrFull6W',
        'BrHalf', 'BrHalf3W', 'BrHalf4W', 'Broadcast', 'CalFile', 'Calibrate',
        'CHR', 'CPIAddModule', 'CPIFileSend', 'CDM_ACPower', 'CDM_Battery',
        'CDM_BrFull', 'CDM_BrFull6W', 'CDM_BrHalf', 'CDM_BrHalf3W',
        'CDM_BrHalf4W', 'CDM_Delay', 'CDM_ExciteI', 'CDM_ExciteV',
        'CDM_MuxSelect', 'CDM_PanelTemp', 'CDM_PeriodAvg', 'CDM_PulsePort',
        'CDM_Resistance', 'CDM_Resistance3W', 'CDM_SW12', 'CDM_SW5',
        'CDM_SWPower', 'CDM_TCDiff', 'CDM_TCSe', 'CDM_Therm107',
        'CDM_Therm108', 'CDM_Therm109', 'CDM_VoltSE', 'CDM_VoltDiff',
        'CDM_CurrentDiff', 'CDM_VW300Config', 'CDM_VW300Dynamic',
        'CDM_VW300Static', 'CDM_VW300Rainflow', 'CDM_TCComp', 'CheckSum',
        'ClockChange', 'ClockReport', 'ComPortIsActive', 'Cos', 'CPISpeed',
        'Csgn', 'Cosh', 'CSAT3', 'CSAT3B', 'CSAT3BMonitor', 'CS616', 'CS7500',
        'CheckPort', 'ClockSet', 'Covariance', 'CovSpa', 'CardFlush',
        'CardOut', 'CTYPE', 'CWB100', 'CWB100Diagnostics', 'CWB100RSSI',
        'CWB100Routes', 'Data', 'DataLong', 'DataGram', 'DaylightSavingUS',
        'DaylightSaving', 'DataTime', 'DialVoice', 'DataEvent', 'DataInterval',
        'Delay', 'DewPoint', 'DHCPRenew', 'DialModem', 'DialSequence', 'DNP',
        'DNPUpdate', 'DNPVariable', 'EC100', 'EC100Configure', 'Eqv',
        'EncryptExempt', 'EmailSend', 'EmailRelay', 'EMailRecv', 'Encryption',
        'Erase', 'ESSInitialize', 'ESSVariables', 'EndDialSequence',
        'DisplayValue', 'DisplayLine', 'ExciteV', 'EndBurstTrigger', 'ExciteI',
        'ExciteCAO', 'Exp', 'EthernetPower', 'I2COpen', 'I2CRead', 'I2CWrite',
        'SPIOpen', 'SPIRead', 'SPIWrite', 'IPNetPower', 'ETsz', 'FFT',
        'FFTSpa', 'FileManage', 'FileMark', 'FillStop', 'FindSpa', 'Fix',
        'FieldNames', 'LoadFieldCal', 'LoggerType', 'IIF', 'SampleFieldCal',
        'NewFieldCal', 'NewFieldNames', 'FieldCal', 'FieldCalStrain',
        'FileOpen', 'FileClose', 'FileCopy', 'FileEncrypt', 'FileWrite',
        'FileRead', 'FileReadLine', 'FileRename', 'FileTime', 'FileSize',
        'FileList', 'Frac', 'FormatFloat', 'FormatLong', 'FormatLongLong',
        'FTPClient', 'GetRecord', 'GetDataRecord', 'GetFile', 'GetVariables',
        'GOESData', 'GOESStatus', 'GOESSetup', 'GOESGPS', 'GOESTable',
        'GOESField', 'GPS', 'Hex', 'HexToDec', 'Histogram', 'Histogram4D',
        'HydraProbe', 'HTTPGet', 'HTTPPost', 'HTTPPut', 'HTTPOut',
        'TimeIntoInterval', 'IfTime', 'INSATSetup', 'INSATStatus', 'INSATData',
        'Int', 'INTDV', 'InStr', 'InstructionTimes', 'IPInfo', 'IPRoute',
        'IPTrace', 'IMP', 'Len', 'LevelCrossing', 'LI7200', 'LI7700',
        'LineNum', 'Log', 'LN', 'Log10', 'LowerCase', 'Maximum', 'MaxSpa',
        'Median', 'MemoryTest', 'MenuItem', 'MenuPick', 'MenuRecompile', 'Mid',
        'Minimum', 'MinSpa', 'ModemCallback', 'ModemHangup', 'EndModemHangup',
        'Moment', 'MonitorComms', 'Move', 'MoveBytes', 'MovePrecise', 'Mod',
        'ModbusMaster', 'ModbusSlave', 'MuxSelect', 'NewFile', 'Not',
        'OmniSatData', 'OmniSatSTSetup', 'OmniSatRandomSetup', 'OmniSatStatus',
        'OpenInterval', 'Optional', 'PanelTemp', 'PeakValley', 'PeriodAvg',
        'PingIP', 'PipeLineMode', 'PreserveVariables', 'PPPOpen', 'PPPClose',
        'PortBridge', 'PortGet', 'PortSet', 'PortsConfig', 'PortPairConfig',
        'PRT', 'PRTCalc', 'PulseCount', 'PulseCountReset', 'PulsePort', 'PWM',
        'PWR', 'RainFlow', 'RainFlowSample', 'Randomize', 'Resistance',
        'Resistance3W', 'Read', 'ReadIO', 'ReadOnly', 'RealTime', 'RectPolar',
        'ResetTable', 'Restore', 'Replace', 'Right', 'Left', 'RMSSpa', 'RND',
        'Route', 'Routes', 'RoutersNeighbors', 'Round', 'Floor', 'Ceiling',
        'RunProgram', 'Sample', 'SampleMaxMin', 'SatVP', 'SDI12Recorder',
        'SDI12SensorSetup', 'SDI12SensorResponse', 'SDMAO4', 'SDMAO4A',
        'SDMBeginPort', 'SDMCAN', 'SDMCD16AC', 'SDMCD16Mask', 'SDMCVO4',
        'SDMGeneric', 'SDMINT8', 'SDMSpeed', 'SDMSW8A', 'SDMTrigger', 'SDMX50',
        'SecsSince1990', 'SemaphoreGet', 'SemaphoreRelease', 'SendData',
        'SendFile', 'SendTableDef', 'SendGetVariables', 'SendVariables',
        'SerialOpen', 'SerialClose', 'SerialFlush', 'SerialIn',
        'SerialInBlock', 'SerialInChk', 'SerialInRecord', 'SerialOut',
        'SerialOutBlock', 'SerialBrk', 'SetSettings', 'SetSecurity',
        'SetStatus', 'SetSetting', 'ShutDownBegin', 'ShutDownEnd', 'Signature',
        'SNMPVariable', 'StaticRoute', 'StdDev', 'StdDevSpa', 'Sgn', 'Sin',
        'Sinh', 'SDMSIO4', 'SDMIO16', 'SplitStr', 'Sprintf', 'SolarPosition',
        'SortSpa', 'Sqr', 'StrainCalc', 'StrComp', 'SW12', 'TCSe', 'TCDiff',
        'TCPClose', 'TCPOpen', 'TCPsyc', 'TGA', 'Therm109', 'Therm108',
        'Therm107', 'Thermistor', 'TimedControl', 'TimeIsBetween', 'Timer',
        'Totalize', 'TableFile', 'TableHide', 'Tan', 'Tanh', 'TDR100',
        'TDR200', 'TimerInput', 'TimeUntilTransmit', 'TotalRun', 'MinRun',
        'MaxRun', 'Trim', 'LTrim', 'RTrim', 'UDPDataGram', 'UDPOpen', 'Until',
        'UpperCase', 'PakBusClock', 'VaporPressure', 'VibratingWire',
        'VoiceSetup', 'VoiceSpeak', 'VoiceBeg', 'EndVoice', 'VoiceKey',
        'VoiceNumber', 'VoicePhrases', 'VoiceHangup', 'VoltSE', 'VoltDiff',
        'WaitDigTrig', 'WaitTriggerSequence', 'TriggerSequence',
        'WebPageBegin', 'WebPageEnd', 'WetDryBulb', 'WorstCase', 'WriteIO',
        'WindVector', 'Network', 'NetworkTimeProtocol', 'XMLParse', 'TypeOf',
        'CurrentSE', 'Matrix', 'Gzip', 'GOESCommand', 'GOESCommand',
        'StructureType', 'Quadrature', 'SMSRecv', 'SMSSend',
        'TCPActiveConnections', 'WatchdogTimer', 'MQTTConnect',
        'MQTTPublishTable', 'MQTTPublishConstTable',
    )

    _numeric_suffix = r'(L|l|UL|ul|u|U|F|f|ll|LL|ull|ULL)?'

    tokens = {
        'root': [
            # Line continuation
            (r'(\.\.)(\n)', bygroups(token.Text, token.Whitespace)),
            # Keywords
            (
                r'(NULL|true|false|TRUE|FALSE|True|False)',
                token.Keyword.Constant,
            ),
            (r'(Dim|Public|Function|Const)\s+', token.Keyword.Declaration),
            (
                r'(Include)(\s+)("([^"\\]|\\.)*")',
                bygroups(
                    token.Keyword.Namespace,
                    token.Whitespace, token.String.Double,
                ),
            ),
            # Keyword Types
            (
                r'(Float|Double|Long|Boolean|String|FP2|IEEE4|IEEE8|UINT1|'
                r'UINT2|UINT4|Bool8|NSEC)',
                token.Keyword.Type,
            ),
            (
                r'(Const)(\s+)([a-zA-Z_])',
                bygroups(
                    token.Keyword.Declaration,
                    token.Whitespace,
                    token.Name.Constant,
                ),
            ),
            # a unit definition has no operators that need to be highlighted
            (
                r'(Units)(\s*)([a-zA-Z_]+)(\s*)(=)(\s*)(.+)',
                bygroups(
                    token.Keyword,
                    token.Whitespace,
                    token.Name.Variable,
                    token.Whitespace,
                    token.Operator,
                    token.Whitespace,
                    token.Text,
                ),
            ),
            (
                fr"({'|'.join(sorted(KEYWORDS, reverse=True))})(?=[\(|\s|\=])",
                token.Keyword,
            ),
            # Names
            (
                fr"({'|'.join(sorted(BUILTINS, reverse=True))})(?=[\(|\s|\=])",
                token.Name.Builtin,
            ),
            (r'[a-zA-Z_]\w*', token.Name.Variable),
            # strings
            (r'"([^"\\]|\\.)*"', token.String.Double),
            (r'\s+', token.Whitespace),
            (r'\\.', token.String.Escape),
            # Numeric
            (fr'((\+|\-)?[0-9]+){_numeric_suffix}', token.Number.Integer),
            (fr'(&(b|B)[0-1]*){_numeric_suffix}', token.Number.Bin),
            (fr'(&(h|H)[0-9a-fA-F]*{_numeric_suffix})', token.Number.Hex),
            (
                fr'((\+|\-)?([0-9]+\.?[0-9]*)|(\+|\-)?(\.[0-9]+))((e|E)(\+|\-)?[0-9]+)?{_numeric_suffix}',  # noqa: E501
                token.Number.Float,
            ),
            # operators
            (
                r'(\^|\/|\*|\+|\-|=|<>|>|<|>=|<=|&|>>|<<|&=|@|!)',
                token.Operator,
            ),
            (r'(AND|OR|NOT)', token.Operator.Word),
            # punctuation
            (r'[\(\),;{}]', token.Punctuation),
            # comment
            (r"'.*?\n", token.Comment.Single),
        ],
    }


def setup(app: Any) -> dict[str, object]:
    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
