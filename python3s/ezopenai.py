import dataclasses
from typing import Any, Dict, List, Optional,Callable,T
import openai
import json
from openai.types.chat.chat_completion import ChatCompletion

untypemap:dict[type,str] = {
    str: "string",
    list: "object",
    dict: "object",
}

FUNCTION_CALLING_COMPATIBLE = Callable[[dict[str,str],],T]

class registera:
    """
    openai function calling用関数テーブル管理
    """
    _lst: List[str] = None
    _map: Dict[str, FUNCTION_CALLING_COMPATIBLE] = None

    def __init__(self) -> None:
        self._lst = []
        self._map = dict()

    def register(self, method: FUNCTION_CALLING_COMPATIBLE) -> FUNCTION_CALLING_COMPATIBLE:
        """
        デコーレタによる登録。__doc__と__annotations__をそのまま使う
        """
        paramdict = {}
        retype = None
        for kk, vv in method.__annotations__.items():
            if kk == "return":
                retype = untypemap[vv]
            else:
                paramdict[kk] = {"type": untypemap[vv], "descriptions": kk}

        # print(paramdict, retype)
        assert len(
            paramdict) > 0, f"{method.__name__} must argument with typehint."

        datum = {
            "type": "function",
            "function": {
                "name": method.__name__,
                "description": method.__doc__ or method.__name__,
                "parameters": {
                    "type": retype,
                    "properties": paramdict,
                    "required": tuple(paramdict.keys()),
                } 
            }
        }
        ##breakpoint()
        print(json.dumps(datum))
        self._lst.append(datum)
        self._map.update({method.__name__: method})
        return method

    def call(self, name, args: dict[str,str])->Any:
        return self._map[name](**args)


functions = registera()

@dataclasses.dataclass(kw_only=True)
class apiauthconfig:
    api_key: str
    organization: str
    OPENAI_MODEL: str


class requester:
    _config : apiauthconfig = None
    session_query :list[dict] = None
    latestresponse : Optional["ChatCompletion"] = None
    # functions = register
    stopped :bool = None
    ##client :openai.OpenAI = None
    finalcontent: Optional[str] = None

    @property
    def client(self): # もしや毎回つくったほうが安全なのでは？
        return openai.OpenAI(
            api_key = self._config.api_key,
            organization=self._config.organization,
            max_retries=0
        )

    def __init__(self, dto:apiauthconfig = None, **config):
        self._config = dto or apiauthconfig(**config)
        #openai.organization = self._config.organization
        self.session_query = []
        self.stopped = False

    def setfirstquery(self, q):
        self.session_query.append({"role": "user", "content": q})

    #@pypersist.persist(pickle=yaml.dump_all,unpickle=yaml.safe_load)
    def requestonce(self)-> "ChatCompletion":
        ###import openai.types.chat
        ###self.latestresponse = yaml.unsafe_load(open("backup.yaml").read())
        ####breakpoint()
        ###return self.latestresponse
        self.latestresponse = self.client.chat.completions.create(
            model=self._config.OPENAI_MODEL,
            messages=self.session_query,
            tools=functions._lst,
            tool_choice="auto",
        )
        return self.latestresponse

    def perform_functions_calling(self):
        ###breakpoint()
        for iichoose in self.latestresponse.choices:
            ####breakpoint()
            reason = iichoose.finish_reason
            if reason == "stop":
                self.stopped = True
                self.finalcontent = iichoose.message.content
                break
            if reason == "tool_calls":
                # if "function_call" in iichoose.message:
                self.session_query.append(iichoose.message)
                for call1 in iichoose.message.tool_calls:
                    ###breakpoint()
                    becallname = call1.function.name
                    arguments = json.loads(call1.function.arguments)

                    _funcresult = functions.call(becallname, arguments)
                    if type(_funcresult) != str:
                        ##breakpoint()
                        _funcresult = json.dumps(_funcresult)
                    ###self.session_query.append(iichoose.message)
                    self.session_query.append(
                        {"role": "tool", "name": becallname, "content": _funcresult, "tool_call_id": call1.id })
                    ###breakpoint()
